resource "aws_iam_role" "app_security_headers" {
  name               = "cloudfront-lambda-edge"
  path               = "/service-role/"
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

data "archive_file" "security_headers_lambda_source_package" {
  type        = "zip"
  source_dir  = "../../lambda/fe_content_headers"
  output_path = "security_headers.zip"
}

resource "aws_lambda_function" "security_headers" {
  #checkov:skip=CKV_AWS_116:No dead letter queue functionality at this time
  #checkov:skip=CKV_AWS_50:X-Ray tracing not needed at this time
  #checkov:skip=CKV_AWS_117:Lambda does not need to be in a VPC
  #checkov:skip=CKV_AWS_115:concurrent execution limits not required
  function_name    = "security-headers"
  description      = "Applies security headers to frontend resource requests"
  role             = aws_iam_role.app_security_headers.arn
  filename         = data.archive_file.security_headers_lambda_source_package.output_path
  runtime          = "nodejs12.x" #Lambda supports nodejs14.x but lambdaedge only supports nodejs12.x
  handler          = "index.handler"
  publish          = true
  source_code_hash = data.archive_file.security_headers_lambda_source_package.output_base64sha256

  # NOTE Lambda Edge does not support environment variables: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-requirements-limits.html#lambda-requirements-lambda-function-configuration
  # We use custom origin headers instead to act as environment variables

  depends_on = [
    data.archive_file.security_headers_lambda_source_package
  ]
}
