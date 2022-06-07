
locals {
  react_env_vars = {
    AWS_PROFILE               = local.AWS_PROFILE[var.environment]
    REACT_APP_VERSION         = jsondecode(file("../../../frontend/package.json")).version
    REACT_APP_BUILD_NUMBER    = var.git_build_number
    REACT_APP_ENVIRONMENT     = var.environment
    REACT_APP_FRONTEND_TLD    = local.ROOT_DOMAIN[var.environment]
    REACT_APP_API_ROOT        = "https://${local.API_DOMAIN[var.environment]}/v1"
    REACT_APP_SENTRY_DSN      = nonsensitive(data.aws_secretsmanager_secret_version.sentry_frontend_dsn.secret_string)
    REACT_APP_SEGMENT_ID      = local.SEGMENT_WEB_ID[var.environment]
    REACT_APP_EXPO_SEGMENT_ID = local.REACT_APP_EXPO_SEGMENT_ID[var.environment]
    SKIP_PREFLIGHT_CHECK      = true
    INLINE_RUNTIME_CHUNK      = false
    IMAGE_INLINE_SIZE_LIMIT   = 0
    SENTRY_URL                = local.SENTRY_URL[var.environment]
    SENTRY_AUTH_TOKEN         = local.SENTRY_AUTH_TOKEN[var.environment]
    SENTRY_SET_COMMITS        = true
    SENTRY_LOG_LEVEL          = "info"
    SENTRY_PROJECT            = local.SENTRY_PROJECT[var.environment]
  }
}


resource "null_resource" "frontend-web-exec" {
  provisioner "local-exec" {
    working_dir = "../../../frontend/"
    command     = "yarn && yarn build && aws s3 sync ./build ${local.FE_BUCKET_NAME[var.environment]} --cache-control 'no-cache' --delete && aws s3 cp ./build/static ${local.FE_BUCKET_NAME[var.environment]}/static --recursive --cache-control 'max-age=31536000, immutable'"
    environment = local.react_env_vars
  }
  triggers = {
    always_run = timestamp()
  }
}


resource "null_resource" "frontend-expo-login" {
  provisioner "local-exec" {
    working_dir = "../../../jah/"
    command     = "yarn && yarn expo login --username=jasprhealth --password=Passw0rd! --non-interactive"
    environment = local.react_env_vars
  }
  triggers = {
    always_run = timestamp()
  }
  depends_on = [null_resource.frontend-web-exec]
}

resource "null_resource" "frontend-expo-publish" {
  # We DO NOT want this to run on Production
  count = var.environment == local.PRODUCTION ? 0 : 1
  provisioner "local-exec" {
    working_dir = "../../../jah/"
    command     = "yarn expo publish --release-channel=${local.EXPO_CHANNELS[var.environment]}"
    environment = local.react_env_vars
  }
  triggers = {
    always_run = timestamp()
  }
  depends_on = [null_resource.frontend-expo-login]
}

resource "null_resource" "frontend-expo-android-build" {
  # We DO want this to run on Production
  count = var.environment == local.PRODUCTION ? 1 : 0
  provisioner "local-exec" {
    working_dir = "../../../jah/"
    command     = "yarn expo build:android --no-wait -t app-bundle --release-channel=${local.EXPO_CHANNELS[var.environment]}"
    environment = local.react_env_vars
  }
  triggers = {
    always_run = timestamp()
  }
  depends_on = [null_resource.frontend-expo-login]
}

resource "null_resource" "frontend-expo-ios-build" {
  # We DO want this to run on Production
  count = var.environment == local.PRODUCTION ? 1 : 0
  provisioner "local-exec" {
    working_dir = "../../../jah/"
    command     = "yarn expo build:ios --no-wait --release-channel=${local.EXPO_CHANNELS[var.environment]}"
    environment = local.react_env_vars
  }
  triggers = {
    always_run = timestamp()
  }
  depends_on = [null_resource.frontend-expo-login]
}

