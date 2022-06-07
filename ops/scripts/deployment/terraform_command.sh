#!/bin/bash
set -e

AWS_PROFILE=$AWS_PROFILE terraform "$TERRAFORM_COMMAND" \
-var="vpc_id=${VPC_ID}" \
-var="api_erc_image_url=${API_ECR_TAG}" \
-var="worker_erc_image_url=${WORKER_ECR_TAG}" \
-var="scheduler_erc_image_url=${SCHEDULER_ECR_TAG}" \
-var="git_hash=${GIT_HASH}" \
-var="git_branch=${GIT_BRANCH}" \
-var="git_build_number=${BITBUCKET_BUILD_NUMBER}" \
-var="aws_secret_key_arn=${AWS_SECRET_ARN}" \
-var="aws_access_key_arn=${AWS_ACCESS_ARN}" \
-var="django_secret_key_arn=${DJANGO_SECRET_ARN}" \
-var="fernet_keys_arn=${FERNET_KEYS_ARN}" \
-var="twilio_auth_token_arn=${TWILIO_AUTH_TOKEN_ARN}" \
-var="aws_secret_manager_base_arn=${AWS_SECRETS_MANAGER_BASE_ARN}" \
-var="environment=${ENVIRONMENT}" \
-var="load_fixtures=${LOAD_FIXTURES}" \
-var="fixture_list=${FIXTURE_LIST}" \
-var="redis_token_arn=${REDIS_TOKEN_ARN}" \
-var="postgres_admin_password_arn=${POSTGRES_ADMIN_PW_ARN}" \
-var="segment_io_postgres_admin_password_arn=${SEGMENT_IO_POSTGRES_ADMIN_PW_ARN}" \
-var="sentry_frontend_dsn_arn=${SENTRY_FRONTEND_DSN_ARN}" \
-var="sentry_backend_dsn_arn=${SENTRY_BACKEND_DSN_ARN}" \
-var="epic_client_id_arn=${EPIC_CLIENT_ID_ARN}" \
-var="epic_backend_client_id_arn=${EPIC_BACKEND_CLIENT_ID_ARN}" \
-var="epic_private_key_arn=${EPIC_PRIVATE_KEY_ARN}" \
-auto-approve
