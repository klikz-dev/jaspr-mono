
locals {
  PRODUCTION  = "production"
  INTEGRATION = "integration"
  DEVELOPMENT = "development"

  # Root Domain for Each Environment
  ROOT_DOMAIN = {
    production  = "jasprhealth.com"
    integration = "jaspr-integration.com"
    development = "jaspr-development.com"
  }

  EDGE_SUBDOMAIN = {
    production  = "*.app"
    integration = "*.app"
    development = "*.app"
  }
  BUCKET_NAME = {
    production  = "589623662327-frontend"
    integration = "616471802661-frontend"
    development = "128206503653-frontend"
  }

  S3_EDGE_ORIGIN_ID = {
    production  = "S3-jaspr-production-media"
    integration = "S3-jaspr-integration-media"
    development = "S3-jaspr-development-media"
  }

  SENTRY_ROOT = {
    production  = "sentry.jasprhealth.com"
    integration = "sentry.jaspr-development.com"
    development = "sentry.jaspr-development.com"
  }

  SENTRY_REPORT = {
    production  = "https://sentry.jasprhealth.com/api/3/security/?sentry_key=4322982521d245ebbd7780c3e06663ba"
    integration = "https://sentry.jaspr-development.com/api/2/security/?sentry_key=9fc33a471bb34e719920b70b3a155f49"
    development = "https://sentry.jaspr-development.com/api/2/security/?sentry_key=9fc33a471bb34e719920b70b3a155f49"
  }

}
