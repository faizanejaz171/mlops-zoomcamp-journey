variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
  default     = "faizan-mlops-bucket-v2"
}

variable "project_id" {
  description = "The unique identifier for the machine learning project"
  type        = string
  default     = "mlops-ride-prediction"
}
