
data "aws_vpc" "default" {
  id = local.vpc_id

  tags = {
    Namespace = "jaspr"
  }
}

data "aws_subnet_ids" "private" {
  vpc_id = local.vpc_id

  tags = {
    tier = "private"
    Namespace = "jaspr"
  }
}

data "aws_subnet_ids" "public" {
  vpc_id = local.vpc_id

  tags = {
    tier = "public"
    Namespace = "jaspr"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_acm_certificate" "api_cert" {
  domain = local.API_CERTIFICATE[var.environment]
}

data "aws_secretsmanager_secret" "postres_admin_password"{
  arn = var.postgres_admin_password_arn
}

data "aws_secretsmanager_secret_version" "postres_admin_password" {
  secret_id = data.aws_secretsmanager_secret.postres_admin_password.id
}

data "aws_secretsmanager_secret" "sentry_frontend_dsn" {
  arn = var.sentry_frontend_dsn_arn
}

data "aws_secretsmanager_secret_version" "sentry_frontend_dsn" {
  secret_id = data.aws_secretsmanager_secret.sentry_frontend_dsn.id
}

data "aws_secretsmanager_secret" "segment_io_postgres_admin_password" {
  count = var.environment == local.PRODUCTION ? 1 : 0
  arn = var.segment_io_postgres_admin_password_arn
}

data "aws_secretsmanager_secret_version" "segment_io_postgres_admin_password" {
  count = var.environment == local.PRODUCTION ? 1 : 0
  secret_id = data.aws_secretsmanager_secret.segment_io_postgres_admin_password[count.index].id
}
