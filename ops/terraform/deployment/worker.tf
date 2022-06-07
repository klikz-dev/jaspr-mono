
data "template_file" "worker_task_definition_json"{
  template = file("${path.module}/templates/rq_task_definition.tpl")
  vars = {
    erc_image_url = var.worker_erc_image_url
    container_name = local.WORKER_FAMILY
    environment_vars = data.template_file.environment_variables_json.rendered
    region = var.aws_region
    awslog_group = aws_cloudwatch_log_group.worker_log_group.name
    aws_access_key_arn = var.aws_access_key_arn
    aws_secret_key_arn = var.aws_secret_key_arn
    twilio_auth_token_arn = var.twilio_auth_token_arn
    django_secret_key_arn = var.django_secret_key_arn
    fernet_keys_arn = var.fernet_keys_arn
    epic_client_id_arn = var.epic_client_id_arn
    epic_backend_client_id_arn = var.epic_backend_client_id_arn
    epic_private_key_arn = var.epic_private_key_arn
    sentry_dsn_arn = var.sentry_backend_dsn_arn
    database_url_arn = aws_secretsmanager_secret.jaspr_postgres_connection_secret.arn
    redis_url_arn = aws_secretsmanager_secret.jaspr_redis_connection_secret.arn
    stream_prefix = local.WORKER_STREAM_PREFIX
    pid_name = local.WORKER_PID_NAME
    cpu = local.WORKER_CPU[var.environment]
    memory = local.WORKER_MEMORY[var.environment]
  }
}

module "worker_fargate" {
  source = "../modules/fargate-service"

  cpu = local.WORKER_CPU[var.environment]
  memory = local.WORKER_MEMORY[var.environment]
  execution_role_arn = aws_iam_role.jaspr_app_task_execution_role.arn
  task_role_arn = aws_iam_role.jaspr_app_container_role.arn
  family_name = local.WORKER_FAMILY
  security_groups = [aws_security_group.background_worker_sg.id]
  subnets = local.private_subnet_ids
  assign_public_ip = false
  ecs_cluster_tags = local.STANDARD_TAGS
  ecs_service_tags = local.STANDARD_TAGS
  task_definition_tags = local.STANDARD_TAGS
  ecs_cluster_name = "worker-cluster-${local.deployment_name}"
  ecs_service_name = "worker-${local.deployment_name}"
  instance_count = local.WORKER_INSTANCE_COUNT[var.environment]
  container_definition = data.template_file.worker_task_definition_json.rendered
}
