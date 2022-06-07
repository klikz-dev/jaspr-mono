
// Don't remove this yet. We need to remove it from the base state.
// It is under management by the edge deployment.
resource "aws_iam_role" "app_security_headers" {
  name = var.environment == local.DEVELOPMENT ? "dev-cloudfront-origin-redirect-lambda-edge" : "cloudfront-origin-redirect-lambda-edge"
  path = "/service-role/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
     {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "edgelambda.amazonaws.com",
          "lambda.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}
