
locals {
  create_segment_db = var.environment == local.PRODUCTION
  segment_snapshot = var.environment == local.PRODUCTION ? "first-segment-snapshot" : null
}

module "segment_io" {
  source = "../modules/aws_rds"

  create_db_instance = local.create_segment_db
  create_db_option_group = local.create_segment_db
  create_db_parameter_group = local.create_segment_db
  create_db_subnet_group = local.create_segment_db
  create_monitoring_role = local.create_segment_db

  identifier = "jaspr-segment-io-db"

  engine = "postgres"
  engine_version = local.POSTGRES_VERSION

  instance_class = local.postgres_instance_type
  allocated_storage = 10
  max_allocated_storage = 500

  snapshot_identifier = local.segment_snapshot

  name = "segment"
  username = "jaspr_segment_admin"
  password = var.environment == local.PRODUCTION ? data.aws_secretsmanager_secret_version.segment_io_postgres_admin_password[0].secret_string : "Not-used"
  port = local.postgres_port

  iam_database_authentication_enabled = false
  vpc_security_group_ids = var.environment == local.PRODUCTION ? [aws_security_group.segment_postgres_sg[0].id] : []
  publicly_accessible = true

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window = "03:00-06:00"
  storage_encrypted = true

  # DB subnet group
  subnet_ids = local.public_subnet_ids

  # DB parameter group
  family = "postgres11"

  # DB option group
  major_engine_version = "11"

  auto_minor_version_upgrade = true
  allow_major_version_upgrade = false

  skip_final_snapshot = false
  copy_tags_to_snapshot = true
  final_snapshot_identifier = "postgres-backup-segment-io"

  tags = {
    Environment = var.environment
  }
}