
resource "aws_iam_access_key" "django_user" {
  user    = aws_iam_user.django_user.name
}

resource "aws_iam_user" "django_user" {
  name = "django_user"
}

resource "aws_iam_user_policy" "django_policy" {
  name = "django_policy"
  user = aws_iam_user.django_user.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "elastictranscoder:*",
        "cloudfront:*",
        "s3:List*",
        "s3:Put*",
        "s3:Get*",
        "s3:Delete*",
        "s3:*MultipartUpload*",
        "iam:CreateRole",
        "iam:PutRolePolicy",
        "iam:GetRolePolicy",
        "iam:List*",
        "sns:CreateTopic",
        "sns:List*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["sns:ConfirmSubscription"],
      "Resource": ["arn:aws:sns:*:*:*"]
    },
    {
      "Effect":"Allow",
      "Action":[
        "ses:*"
      ],
      "Resource":"*"
    }
  ]
}
EOF
}