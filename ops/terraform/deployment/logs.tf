# API Server
resource "aws_cloudwatch_log_group" "app_log_group" {
  name              = "/ecs/${local.deployment_name}/app"
  retention_in_days = local.LOG_RETENTION_TIME

  tags = {
    Deployment = local.deployment_name
  }
}

resource "aws_cloudwatch_log_stream" "app_log_stream" {
  name           = "app-log-stream-${local.deployment_name}"
  log_group_name = aws_cloudwatch_log_group.app_log_group.name
}

# Worker
resource "aws_cloudwatch_log_group" "worker_log_group" {
  name              = "/ecs/${local.deployment_name}/worker"
  retention_in_days = local.LOG_RETENTION_TIME

  tags = {
    Deployment = local.deployment_name
  }
}

resource "aws_cloudwatch_log_stream" "worker_log_stream" {
  name           = "worker-log-stream-${local.deployment_name}"
  log_group_name = aws_cloudwatch_log_group.worker_log_group.name
}

# Scheduler
resource "aws_cloudwatch_log_group" "scheduler_log_group" {
  name              = "/ecs/${local.deployment_name}/scheduler"
  retention_in_days = local.LOG_RETENTION_TIME

  tags = {
    Deployment = local.deployment_name
  }
}

resource "aws_cloudwatch_log_stream" "scheduler_log_stream" {
  name           = "scheduler-log-stream-${local.deployment_name}"
  log_group_name = aws_cloudwatch_log_group.scheduler_log_group.name
}