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
