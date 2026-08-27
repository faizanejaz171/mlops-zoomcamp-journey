# ------------------------------------------------------
# 1. Terraform Backend (Storing State in S3)
# ------------------------------------------------------
terraform {
  backend "s3" {
    bucket                      = "faizan-mlops-bucket-v2"
    key                         = "mlops-zoomcamp/terraform.tfstate"
    region                      = "us-east-1"
    access_key                  = "test"
    secret_key                  = "test"
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
    use_path_style              = true

    endpoints = {
      s3      = "http://localhost:4566"
      sts     = "http://localhost:4566"
      kinesis = "http://localhost:4566"
      iam     = "http://localhost:4566"
      ecr     = "http://localhost:4566"
      lambda  = "http://localhost:4566"
    }
  }
}

# ------------------------------------------------------
# 2. AWS Provider Configuration (LocalStack Setup)
# ------------------------------------------------------
provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3      = "http://localhost:4566"
    sts     = "http://localhost:4566"
    kinesis = "http://localhost:4566"
    iam     = "http://localhost:4566"
    ecr     = "http://localhost:4566"
    lambda  = "http://localhost:4566"
  }
}

# ------------------------------------------------------
# 3. MLOps Pipeline Resources (End-to-End Setup)
# ------------------------------------------------------

# Input Stream: Receives incoming raw ride events
module "source_kinesis_stream" {
  source           = "./modules/kinesis"
  stream_name      = "ride-events-input"
  shard_count      = 1
  retention_period = 24
}

# Output Stream: Stores the final predictions from the ML model
module "output_kinesis_stream" {
  source           = "./modules/kinesis"
  stream_name      = "ride-predictions-output"
  shard_count      = 1
  retention_period = 24
}

# S3 Bucket: Stores the MLFlow trained model artifacts
resource "aws_s3_bucket" "model_bucket" {
  bucket = "faizan-mlflow-models-bucket"
}

# ------------------------------------------------------
# 4. Elastic Container Registry (ECR)
# ------------------------------------------------------

# ECR Repository: Stores the Docker image for the Lambda function
resource "aws_ecr_repository" "lambda_repo" {
  name                 = "${var.project_id}-repo"
  image_tag_mutability = "MUTABLE"

  # We disable scanning for local development to save time
  image_scanning_configuration {
    scan_on_push = false
  }
}

# ------------------------------------------------------
# 5. IAM Role and Policies (Security Pass for Lambda)
# ------------------------------------------------------

# IAM Role: Grants AWS Lambda permission to run (Assume Role)
resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.project_id}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# IAM Policy: Defines exactly what the Lambda function is allowed to do
resource "aws_iam_policy" "lambda_policy" {
  name        = "${var.project_id}-lambda-policy"
  description = "Permissions for Lambda to access Kinesis, S3, and CloudWatch logs"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        # Permission to read from input stream and write to output stream
        Effect = "Allow"
        Action = [
          "kinesis:GetRecords",
          "kinesis:GetShardIterator",
          "kinesis:DescribeStream",
          "kinesis:ListStreams",
          "kinesis:PutRecord",
          "kinesis:PutRecords"
        ]
        Resource = [
          module.source_kinesis_stream.stream_arn,
          module.output_kinesis_stream.stream_arn
        ]
      },
      {
        # Permission to read the ML model from the S3 bucket
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.model_bucket.arn,
          "${aws_s3_bucket.model_bucket.arn}/*"
        ]
      },
      {
        # Permission to write logs (so we can debug if something fails)
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Attach the Policy to the Role (Binding them together)
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# ------------------------------------------------------
# 6. AWS Lambda Function (TEMPORARILY COMMENTED)
# ------------------------------------------------------

# resource "aws_lambda_function" "kinesis_lambda" {
#   function_name = "${var.project_id}-prediction-lambda"
#
#   # 1. Linking the IAM Role (Giving the Security Pass to Lambda)
#   role = aws_iam_role.lambda_exec_role.arn
#
#   # 2. Linking the ECR Repository (Telling Lambda where its Software/Code is)
#   image_uri    = "${aws_ecr_repository.lambda_repo.repository_url}:latest"
#   package_type = "Image"
#   timeout      = 60 # Lambda can run for maximum 60 seconds
#
#   # 3. Environment Variables (Passing addresses to the Python code inside Lambda)
#   environment {
#     variables = {
#       PREDICTIONS_STREAM_NAME = module.output_kinesis_stream.stream_name
#       MODEL_BUCKET_NAME       = aws_s3_bucket.model_bucket.bucket
#     }
#   }
# }

# ------------------------------------------------------
# 7. Kinesis Trigger (TEMPORARILY COMMENTED)
# ------------------------------------------------------

# resource "aws_lambda_event_source_mapping" "kinesis_mapping" {
#   event_source_arn  = module.source_kinesis_stream.stream_arn
#   function_name     = aws_lambda_function.kinesis_lambda.arn
#
#   # TRIM_HORIZON means "Read data from the oldest unread record"
#   starting_position = "TRIM_HORIZON"
# }
