variable "registry_name" {
  type = string
}

resource "aws_ecr_repository" "default" {
  name                 = var.registry_name
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_repository_policy" "default" {
  repository = aws_ecr_repository.default.name

  policy = <<EOF
  {
      "Version": "2008-10-17",
      "Statement": [
          {
              "Sid": "new policy",
              "Effect": "Allow",
              "Principal": "*",
              "Action": [
                  "ecr:GetDownloadUrlForLayer",
                  "ecr:BatchGetImage",
                  "ecr:BatchCheckLayerAvailability",
                  "ecr:PutImage",
                  "ecr:InitiateLayerUpload",
                  "ecr:UploadLayerPart",
                  "ecr:CompleteLayerUpload",
                  "ecr:DescribeRepositories",
                  "ecr:GetRepositoryPolicy",
                  "ecr:ListImages",
                  "ecr:DescribeImages",
                  "ecr:DeleteRepository",
                  "ecr:BatchDeleteImage",
                  "ecr:SetRepositoryPolicy",
                  "ecr:DeleteRepositoryPolicy",
                  "ecr:GetLifecyclePolicy",
                  "ecr:PutLifecyclePolicy",
                  "ecr:DeleteLifecyclePolicy",
                  "ecr:GetLifecyclePolicyPreview",
                  "ecr:StartLifecyclePolicyPreview"
              ]
          }
      ]
  }
  EOF
}

output "arn" {
  value = aws_ecr_repository.default.arn
}

output "name"{
  value = aws_ecr_repository.default.name
}

output "repository_url" {
  value = aws_ecr_repository.default.repository_url
}