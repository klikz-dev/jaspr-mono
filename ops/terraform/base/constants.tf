
locals {

  # Log Retention Time in Days
  LOG_RENTENTION = 90

  # Environments
  PRODUCTION = "production"
  DEVELOPMENT = "development"
  INTEGRATION = "integration"

  # Cloudfront CSP Default Src
  CLOUDFRONT_DEFAULT_SRC = {
    production = "*.jasprhealth.com *.app.jasprhealth.com *.segment.com api.segment.io"
    integration = "*.jaspr-integration.com *.app.jaspr-integration.com *.segment.com api.segment.io"
    development = "*.jaspr-development.com *.app.jaspr-development.com *.segment.com api.segment.io"
  }
}