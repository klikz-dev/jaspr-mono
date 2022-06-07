
resource "aws_iam_role" "jaspr_app_container_role" {
  name = "jaspr_app_container_role_${local.deployment_name}"

  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "Service": "ecs-tasks.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy" "jaspr_app_container_policy" {
  name = "jaspr_app_container_policy_${local.deployment_name}"
  role = aws_iam_role.jaspr_app_container_role.id

  policy = file("${path.module}/templates/iam_app_container.tpl")
}

resource "aws_iam_role" "jaspr_app_task_execution_role" {
  name = "jaspr_app_task_execution_role_${local.deployment_name}"

  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "Service": [
            "ecs.amazonaws.com",
            "ec2.amazonaws.com",
            "ecs-tasks.amazonaws.com"
          ]
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = aws_iam_role.jaspr_app_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "jaspr_app_task_execution_policy" {
  name = "jaspr_app_task_policy_${local.deployment_name}"
  role = aws_iam_role.jaspr_app_task_execution_role.id

  policy = templatefile("${path.module}/templates/iam_task_execution.tpl", {
    vpc_id: local.vpc_id,
    base_arn: var.aws_secret_manager_base_arn
  })
}

resource "aws_iam_role" "jaspr_ecs_service_role" {
  name = "jaspr_ecs_service_role_${local.deployment_name}"

  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "Service": [
            "ecs.amazonaws.com",
            "ec2.amazonaws.com",
            "ecs-tasks.amazonaws.com"
          ]
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  EOF
}

resource "aws_iam_role_policy" "jaspr_ecs_service_role_policy" {
  name = "jaspr_ecs_service_role_policy_${local.deployment_name}"
  role = aws_iam_role.jaspr_ecs_service_role.id
  policy = file("${path.module}/templates/iam_role_policy_ecs_service.json")
}