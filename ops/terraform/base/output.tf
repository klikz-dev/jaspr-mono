/*************************
 * SECRETS
 *************************/
output "aws_secret_key_arn" {
  value = aws_secretsmanager_secret.aws_secret_key.arn
}

output "aws_access_key_arn" {
  value = aws_secretsmanager_secret.aws_access_key.arn
}

output "twilio_auth_token_arn" {
  value = aws_secretsmanager_secret.twilio_auth_token.arn
}

output "django_secret_key_arn" {
  value = aws_secretsmanager_secret.django_secret_key.arn
}

output "fernet_keys_arn" {
  value = aws_secretsmanager_secret.fernet_keys.arn
}

output "redis_token_arn" {
  value = aws_secretsmanager_secret.redis_token.arn
}

output "postgres_admin_password_arn" {
  value = aws_secretsmanager_secret.postgres_admin_password.arn
}

output "sentry_frontend_dsn_arn" {
  value = aws_secretsmanager_secret.sentry_frontend_dsn.arn
}

output "sentry_backend_dsn_arn" {
  value = aws_secretsmanager_secret.sentry_backend_dsn.arn
}

output "epic_client_id_arn" {
  value = aws_secretsmanager_secret.epic_client_id.arn
}

output "epic_backend_client_id_arn" {
  value = aws_secretsmanager_secret.epic_backend_client_id.arn
}

output "epic_private_key_arn" {
  value = aws_secretsmanager_secret.epic_private_key.arn
}

output "segment_io_postgres_admin_password_arn" {
  # If this seems strange, it is.
  # This output is only used on production. Its an empty string on development.
  # Syntax Explainer: https://github.com/hashicorp/terraform/issues/23222
  value = join("", aws_secretsmanager_secret.segment_io_postgres_admin_password.*.arn)
}

/*************************
 * NETWORK
 *************************/

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "subnets" {
  value = module.subnets.private_subnet_ids
}

/*************************
 * ECR
 *************************/

output "api_server_registry_url" {
  value = module.api_server_registry.repository_url
}

output "worker_registry_url" {
  value = module.worker_registry.repository_url
}

output "scheduler_registry_url" {
  value = module.scheduler_registry.repository_url
}
