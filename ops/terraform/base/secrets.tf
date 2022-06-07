
resource "aws_secretsmanager_secret" "aws_secret_key" {
  name_prefix = "aws_secret_access_key"
}

resource "aws_secretsmanager_secret_version" "aws_secret_key" {
  secret_id     = aws_secretsmanager_secret.aws_secret_key.id
  secret_string = aws_iam_access_key.django_user.secret
}

resource "aws_secretsmanager_secret" "aws_access_key" {
  name_prefix = "aws_access_key"
}

resource "aws_secretsmanager_secret_version" "aws_access_key" {
  secret_id     = aws_secretsmanager_secret.aws_access_key.id
  secret_string = aws_iam_access_key.django_user.id
}

resource "aws_secretsmanager_secret" "twilio_auth_token" {
  name_prefix = "twilio_auth_token"
}

resource "aws_secretsmanager_secret" "django_secret_key" {
  name_prefix = "django_secret_key"
}

resource "aws_secretsmanager_secret" "epic_client_id" {
  name_prefix = "epic_client_id"
}

resource "aws_secretsmanager_secret" "epic_backend_client_id" {
  name_prefix = "epic_backend_client_id"
}

resource "aws_secretsmanager_secret" "epic_private_key" {
  name_prefix = "epic_private_key"
}

resource "aws_secretsmanager_secret" "fernet_keys" {
  name_prefix = "fernet_keys"
}

resource "aws_secretsmanager_secret" "sentry_frontend_dsn" {
  name_prefix = "sentry_frontend_dsn"
}

resource "aws_secretsmanager_secret" "sentry_backend_dsn" {
  name_prefix = "sentry_backend_dsn"
}

resource "aws_secretsmanager_secret" "redis_token" {
  name_prefix = "redis_token"
}

resource "aws_secretsmanager_secret" "postgres_admin_password" {
  name_prefix = "postgres_admin_password"
}

resource "aws_secretsmanager_secret" "segment_io_postgres_admin_password" {
  count = var.environment == local.PRODUCTION ? 1 : 0
  name_prefix = "segment_io_postgres_admin_password"
}
