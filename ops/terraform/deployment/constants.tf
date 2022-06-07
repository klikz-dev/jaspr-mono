
locals {

  # Deployment Name
  short_git_name = length(var.git_branch) > 15 ? substr(var.git_branch, 0, 15) : var.git_branch
  deployment_name = var.environment != local.DEVELOPMENT ? var.environment : trimsuffix("${var.environment}-${local.short_git_name}", "-")

  # Environment Names
  PRODUCTION = "production"
  INTEGRATION = "integration"
  DEVELOPMENT = "development"

  # Environment Variables
  ENVIRONMENT_VAR_FILE = {
    production = "production.json"
    integration = "integration.json"
    development = var.git_branch == "release" ? "release.json" : "development.json"
  }

  # Namespace used for tagging resources controlled by TF
  NAMESPACE = "jaspr-tf"

  # AWS PROFILE
  AWS_PROFILE = {
    production = "prod"
    integration = "int"
    development = "dev"
  }

  # Root Domain for Each Environment
  ROOT_DOMAIN = {
    production = "jasprhealth.com"
    integration = "jaspr-integration.com"
    development = "jaspr-development.com"
  }

  API_DOMAIN = {
    # Need to change this after DNS crossover on production
    production = "api.${local.ROOT_DOMAIN[var.environment]}" # Need to change this
    integration = "api.${local.ROOT_DOMAIN[var.environment]}"
    development = "${var.git_branch}.api.${local.ROOT_DOMAIN[var.environment]}"
  }

  FE_WEB_DOMAIN = {
    development = "*--${var.git_branch}.app.jaspr-development.com"
    integration = "*.app.jaspr-integration.com"
    production = "*.app.jasprhealth.com"
  }

  # ACM Certificates

  APP_CERTIFICATE = {
    production = "*.${local.ROOT_DOMAIN[var.environment]}"
    integration = "*.${local.ROOT_DOMAIN[var.environment]}"
    development = "*.app.${local.ROOT_DOMAIN[var.environment]}"
  }

  API_CERTIFICATE = {
    production = "*.${local.ROOT_DOMAIN[var.environment]}"
    integration = "*.${local.ROOT_DOMAIN[var.environment]}"
    development = "*.api.${local.ROOT_DOMAIN[var.environment]}"
  }

  # Frontend Bucket Names
  FE_BUCKET_NAME = {
    production = "s3://589623662327-frontend" #"s3://jaspr-production-frontend/"
    integration = "s3://616471802661-frontend"
    development = "s3://128206503653-frontend/${var.git_branch}"
  }

  # Storybook Bucket Names
  STORYBOOK_BUCKET_NAME = {
    production = "589623662327-storybook"
    integration = "616471802661-storybook"
    development = "128206503653-storybook/${var.git_branch}"
  }

  # Access Log Bucket Names
  ACCESS_LOG_S3_BUCKET_NAME = {
    production = "589623662327-access-logs-us-west-1"
    integration = "jaspr-integration-access-logs"
    development = "jaspr-development-access-logs"
  }

  LOG_RETENTION_TIME = 90

  POSTGRES_VERSION = "11.15"

  #
  EXPO_CHANNELS = {
    production = "production"
    integration = "aws-integration"
    development = "aws-development-${var.git_branch}"
  }

  REACT_APP_EXPO_SEGMENT_ID = {
    production = "vdbWG8QHsvd5wk7KA46nDtQCcoRrUY1y"
    integration = "C2HfaHuy13IF6hFE1p0wtj14zSmrVJyj"
    development = "C2HfaHuy13IF6hFE1p0wtj14zSmrVJyj"
  }

  SENTRY_URL = {
    production = "https://sentry.jasprhealth.com"
    integration = "https://sentry.jaspr-development.com"
    development = "https://sentry.jaspr-development.com"
  }

  SENTRY_AUTH_TOKEN = {
    production = "f89dde8c82f0431692d7fb07ef5c3906444bf3677f574197a5b5488d9b973a95"
    integration = "50b4567a1a6a4f3f98aae1d802fc1f331e6ffbac047041f29fb2d088edfb63e1"
    development = "50b4567a1a6a4f3f98aae1d802fc1f331e6ffbac047041f29fb2d088edfb63e1"
  }

  SENTRY_PROJECT = {
    production = "jaspr-frontend"
    integration = "jaspr-fe"
    development = "jaspr-fe"
  }

  EXPO_USERNAME = "jasprhealth"

  # Network
  vpc_id = var.vpc_id
  public_subnet_ids = data.aws_subnet_ids.public.ids
  private_subnet_ids = data.aws_subnet_ids.private.ids
  availability_zone_1 = data.aws_availability_zones.available.names[0]
  availability_zone_2 = data.aws_availability_zones.available.names[1]
  availability_zones = [local.availability_zone_1, local.availability_zone_2]

  # Cluster Families
  API_FAMILY = "jaspr-api-server"
  WORKER_FAMILY = "jaspr-worker"
  SCHEDULER_FAMILY = "jaspr-scheduler"

  # API Server Settings
  API_SERVER_CPU = {
    development = 1024
    integration = 1024
    production = 1024
  }
  API_SERVER_MEMORY = {
    development = 2048
    integration = 4096
    production = 4096
  }
  API_SERVER_INSTANCE_COUNT = {
    development = 1
    integration = 2
    production = 2
  }

  # Scheduler Settings
  SCHEDULER_CPU = {
    development = 512
    integration = 1024
    production = 1024
  }
  SCHEDULER_MEMORY = {
    development = 1024
    integration = 2048
    production = 2048
  }
  SCHEDULER_INSTANCE_COUNT = {
    development = 1
    integration = 1
    production = 1
  }

  # Worker Settings
  WORKER_CPU = {
    development = 512
    integration = 1024
    production = 1024
  }
  WORKER_MEMORY = {
    development = 1024
    integration = 2048
    production = 2048
  }
  WORKER_INSTANCE_COUNT = {
    development = 1
    integration = 2
    production = 2
  }

  # Log Stream Prefixes
  SCHEDULER_STREAM_PREFIX = "scheduler"
  SCHEDULER_PID_NAME = "scheduler"
  WORKER_STREAM_PREFIX = "worker"
  WORKER_PID_NAME = "worker"

  # Tags
  STANDARD_TAGS = {
    Deployment = local.deployment_name,
    Environment = var.environment
  }

  # CloudFront
  ClOUDFRONT_DISTRIBUTION = {
    production = "E3UB0WZ048EGBH"
    integration = "EQFH2AYVAFVWP"
    development = "E2AQ48F6W14YUX"
  }

  CLOUDFRONT_INVALIDATION_PATH = {
    production = "/*"
    integration = "/*"
    development = "/${var.git_branch}/*"
  }

  SEGMENT_WEB_ID = {
    production = "fi9Y3VbO9Ma29LsRxEqqsGIqeiLFtfHm"
    integration = "DcvCgOMyOkPHp8KWpm461XblMd0ROUIq"
    development = "DcvCgOMyOkPHp8KWpm461XblMd0ROUIq"
  }

  SEGMENT_EXPO_ID = {
    production = "vdbWG8QHsvd5wk7KA46nDtQCcoRrUY1y"
    integration = "C2HfaHuy13IF6hFE1p0wtj14zSmrVJyj"
    development = "C2HfaHuy13IF6hFE1p0wtj14zSmrVJyj"
  }

  POSTGRES_SNAPSHOT = {
    production = "first-production-postgres-snapshot"
    integration = null
    development = var.git_branch == "release" ? "integration-snapshot-8-11" : null
  }

  POSTGRES_BACKUP_RETENTION = {
    production = 35
    integration = 35
    development = var.git_branch == "release" ? 35 : 1
  }

}
