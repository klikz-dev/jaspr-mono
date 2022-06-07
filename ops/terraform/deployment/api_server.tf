
data "template_file" "api_server_task_definition_json"{
  template = file("${path.module}/templates/task_definition.tpl")
  vars = {
    erc_image_url = var.api_erc_image_url

    # Environment
    container_name = local.API_FAMILY
    environment_vars = data.template_file.environment_variables_json.rendered
    region = var.aws_region
    awslog_group = aws_cloudwatch_log_group.app_log_group.name

    # Secrets
    aws_secret_key_arn = var.aws_secret_key_arn
    aws_access_key_arn = var.aws_access_key_arn
    twilio_auth_token_arn = var.twilio_auth_token_arn
    django_secret_key_arn = var.django_secret_key_arn
    fernet_keys_arn = var.fernet_keys_arn
    sentry_dsn_arn = var.sentry_backend_dsn_arn
    epic_client_id_arn = var.epic_client_id_arn
    epic_backend_client_id_arn = var.epic_backend_client_id_arn
    epic_private_key_arn = var.epic_private_key_arn
    database_url_arn = aws_secretsmanager_secret.jaspr_postgres_connection_secret.arn
    redis_url_arn = aws_secretsmanager_secret.jaspr_redis_connection_secret.arn

    cpu = local.API_SERVER_CPU[var.environment]
    memory = local.API_SERVER_MEMORY[var.environment]
  }
}

module "api_server_fargate" {
  source = "../modules/fargate-service"

  cpu = local.API_SERVER_CPU[var.environment]
  memory = local.API_SERVER_MEMORY[var.environment]
  execution_role_arn = aws_iam_role.jaspr_app_task_execution_role.arn
  task_role_arn = aws_iam_role.jaspr_app_container_role.arn
  family_name = local.API_FAMILY
  security_groups = [aws_security_group.api_server_sg.id]
  subnets = local.public_subnet_ids
  assign_public_ip = true
  ecs_cluster_tags = local.STANDARD_TAGS
  ecs_service_tags = local.STANDARD_TAGS
  task_definition_tags = local.STANDARD_TAGS
  ecs_cluster_name = "api-cluster-${local.deployment_name}"
  ecs_service_name = "api-${local.deployment_name}"
  instance_count = local.API_SERVER_INSTANCE_COUNT[var.environment]
  container_definition = data.template_file.api_server_task_definition_json.rendered
  load_balancer = {
    target_group_arn = aws_lb_target_group.api-server-lb-target-group.arn
    container_name   = local.API_FAMILY
    container_port   = 5000
  }
}
