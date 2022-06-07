
# Constants
locals {
  AWS_VPC_NETWORK_MODE = "awsvpc"
  FARGATE = "FARGATE"
}

resource "aws_ecs_task_definition" "task_definition" {
  family = var.family_name
  task_role_arn = var.task_role_arn
  execution_role_arn = var.execution_role_arn
  network_mode = local.AWS_VPC_NETWORK_MODE
  container_definitions = var.container_definition
  requires_compatibilities = [local.FARGATE]
  cpu = var.cpu
  memory = var.memory
  tags = var.task_definition_tags
}

resource "aws_ecs_cluster" "ecs_cluster" {
  name = var.ecs_cluster_name
}

# There is two versions of the ECS Service
# One with and one without a load balancer
resource "aws_ecs_service" "ecs_service_w_lb" {
  count           = var.load_balancer == null ? 0 : 1
  name            = var.ecs_service_name
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.task_definition.arn
  desired_count   = var.instance_count
  launch_type = local.FARGATE
  force_new_deployment = true

  network_configuration {
    subnets          = var.subnets
    security_groups  = var.security_groups
    assign_public_ip = var.assign_public_ip
  }

  load_balancer {
    target_group_arn = var.load_balancer.target_group_arn
    container_name   = var.load_balancer.container_name
    container_port   = var.load_balancer.container_port
  }
}

resource "aws_ecs_service" "ecs_service_wo_lb" {
  count           = var.load_balancer == null ? 1 : 0
  name            = var.ecs_service_name
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.task_definition.arn
  desired_count   = var.instance_count
  launch_type = local.FARGATE
  force_new_deployment = true

  network_configuration {
    subnets          = var.subnets
    security_groups  = var.security_groups
    assign_public_ip = var.assign_public_ip
  }
}
