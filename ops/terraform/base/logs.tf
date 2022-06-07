
resource "aws_flow_log" "vpc_traffic" {
  iam_role_arn    = aws_iam_role.vpc_traffic.arn
  log_destination = aws_cloudwatch_log_group.vpc_traffic.arn
  traffic_type    = "ALL"
  vpc_id          = module.vpc.vpc_id
}

resource "aws_cloudwatch_log_group" "vpc_traffic" {
  name = "/vpc/all-traffic"
  retention_in_days = local.LOG_RENTENTION
}

resource "aws_iam_role" "vpc_traffic" {
  name = "vpc_traffic"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "vpc-flow-logs.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "vpc_traffic" {
  name = "vpc_traffic"
  role = aws_iam_role.vpc_traffic.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}