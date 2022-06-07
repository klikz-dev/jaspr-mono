# AWS

variable "aws_region" {
  type = string
  default = "us-west-1"
}

# Environment

variable "environment" {
  type = string
  default = "development"
}

variable "git_hash" {
  type = string
}

variable "git_branch" {
  type = string
}

variable "git_build_number" {
  type = string
}

variable "load_fixtures" {
  type = string
  default = "False"
}

variable "fixture_list" {
  type = string
  default = ""
}

# Network

variable "vpc_id" {
  type = string
}

# ECR Vars

variable "api_erc_image_url" {
  type = string
}

variable "worker_erc_image_url" {
  type = string
}

variable "scheduler_erc_image_url" {
  type = string
}

# Database Vars

variable "postgres_db_name" {
  type = string
  default = "jaspr_postgres"
}

variable "postgres_admin_user" {
  type = string
  default = "jaspr_admin"
}

variable "postgres_instance_type" {
  type = string
  default = "db.t2.small"
}

# Secret Manager

variable "aws_secret_manager_base_arn" {
  type = string
}

variable "aws_secret_key_arn" {
  type = string
}

variable "aws_access_key_arn" {
  type = string
}

variable "twilio_auth_token_arn" {
  type = string
}

variable "django_secret_key_arn" {
  type = string
}

variable "fernet_keys_arn" {
  type = string
}

variable "epic_client_id_arn" {
  type = string
}

variable "epic_backend_client_id_arn" {
  type = string
}

variable "epic_private_key_arn" {
  type = string
}

variable "redis_token_arn" {
  type = string
}

variable "postgres_admin_password_arn" {
  type = string
}

variable "segment_io_postgres_admin_password_arn" {
  type = string
}

# Sentry Vars

variable "sentry_frontend_dsn_arn" {
  type = string
}

variable "sentry_backend_dsn_arn" {
  type = string
}