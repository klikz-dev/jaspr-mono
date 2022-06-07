locals {

  # Environment Names
  PRODUCTION  = "production"
  INTEGRATION = "integration"
  DEVELOPMENT = "development"

  # Root Domain for Each Environment
  ROOT_DOMAIN = {
    production  = "jasprhealth.com"
    integration = "jaspr-integration.com"
    development = "jaspr-development.com"
  }

  MEDIA_CDN_SUBDOMAIN = {
    production  = "media"
    integration = "media"
    development = var.git_branch == "release" ? "release-media" : "media"
  }

  MEDIA_BUCKET_NAME = {
    production  = "589623662327-media"
    integration = "jaspr-integration-media"
    development = var.git_branch == "release" ? "jaspr-production-media" : "jaspr-development-media"
  }

  S3_MEDIA_CDN_ORIGIN_ID = {
    production  = "S3-jaspr-production-media"
    integration = "S3-jaspr-integration-media"
    development = var.git_branch == "release" ? "S3-jaspr-release-media" : "S3-jaspr-development-media"
  }
}
