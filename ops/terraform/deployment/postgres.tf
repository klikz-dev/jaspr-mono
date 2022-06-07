locals {
  postgres_port = 5432
  postgres_instance_type = var.environment == local.PRODUCTION ? "db.m5.xlarge" : "db.t3.small"
  production_postgres_snapshot = local.POSTGRES_SNAPSHOT[var.environment]
}

module "postgres" {
  source = "../modules/aws_rds/"

  identifier = "jaspr-${local.deployment_name}"

  engine = "postgres"
  engine_version = local.POSTGRES_VERSION
  instance_class = local.postgres_instance_type
  allocated_storage = 10
  max_allocated_storage = 500

  name = var.postgres_db_name
  username = var.postgres_admin_user
  password = data.aws_secretsmanager_secret_version.postres_admin_password.secret_string
  port = local.postgres_port

  iam_database_authentication_enabled = false

  vpc_security_group_ids = [
    aws_security_group.postgres_sg.id
  ]

  snapshot_identifier = local.production_postgres_snapshot

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window = "03:00-06:00"
  backup_retention_period = local.POSTGRES_BACKUP_RETENTION[var.environment]

  storage_encrypted = true

  # DB subnet group
  subnet_ids = local.private_subnet_ids

  # DB parameter group
  family = "postgres11"

  # DB option group
  major_engine_version = "11"

  auto_minor_version_upgrade = false
  allow_major_version_upgrade = false

  skip_final_snapshot = var.environment == local.DEVELOPMENT
  copy_tags_to_snapshot = true
  final_snapshot_identifier = "postgres-backup-${local.deployment_name}"

  tags = {
    Environment = var.environment
    GitBranch = var.git_branch
  }

  parameters = [
    {
      name  = "tcp_keepalives_count"
      value = 10
      apply_method = "immediate"
    },
    {
      name  = "tcp_keepalives_idle"
      value = 600
      apply_method = "immediate"
    },
    {
      name  = "tcp_keepalives_interval"
      value = 30
      apply_method = "immediate"
    }
  ]
}

resource "aws_secretsmanager_secret" "jaspr_postgres_connection_secret" {
  name_prefix = "jaspr_postgres_connection_${local.deployment_name}"
}

resource "aws_secretsmanager_secret_version" "jaspr_postgres_connection_secret_version" {
  secret_id = aws_secretsmanager_secret.jaspr_postgres_connection_secret.id
  secret_string = "postgres://${module.postgres.this_db_instance_username}:${module.postgres.this_db_instance_password}@${module.postgres.this_db_instance_address}:${module.postgres.this_db_instance_port}/${module.postgres.this_db_instance_name}"
}
