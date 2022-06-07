resource "aws_iam_role" "app_dev_redirect" {
  count = 1
  name               = "cloudfront-dev-redirect-lambda-edge"
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

data "archive_file" "dev_redirect_lambda_source_package" {
  count = 1
  type        = "zip"
  source_dir  = "../../lambda/dev_redirect"
  output_path = "dev_redirect.zip"
}

resource "aws_lambda_function" "dev_redirect" {
  count = 1
  #checkov:skip=CKV_AWS_116:No dead letter queue functionality at this time
  #checkov:skip=CKV_AWS_50:X-Ray tracing not needed at this time
  #checkov:skip=CKV_AWS_117:Lambda does not need to be in a VPC
  #checkov:skip=CKV_AWS_115:concurrent execution limits not required
  function_name    = "dev-redirect"
  description      = "Redirects requests to the correct feature branch"
  role             = aws_iam_role.app_dev_redirect[0].arn
  filename         = data.archive_file.dev_redirect_lambda_source_package[0].output_path
  runtime          = "nodejs12.x" #Lambda supports nodejs14.x but lambdaedge only supports nodejs12.x
  handler          = "index.handler"
  publish          = true
  source_code_hash = data.archive_file.dev_redirect_lambda_source_package[0].output_base64sha256

  depends_on = [
    data.archive_file.dev_redirect_lambda_source_package
  ]
}
