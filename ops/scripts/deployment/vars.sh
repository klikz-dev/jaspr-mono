#!/bin/bash

cd ../../terraform/base

# Make sure base is initialized before pulling values from it.
# tfenv use 1.0.2
. ../../scripts/base/terraform_init.sh

VPC_ID=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .vpc_id.value)
API_REGISTRY=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .api_server_registry_url.value)
SCHEDULER_REGISTRY=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .scheduler_registry_url.value)
WORKER_REGISTRY=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .worker_registry_url.value)

# Terraform will only return the full URLs of a repository
# We need to strip out the repository name to get the registry URL
REGISTRY=$(cut -d'/' -f1 <<<"$WORKER_REGISTRY")

AWS_SECRET_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .aws_secret_key_arn.value)
AWS_ACCESS_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .aws_access_key_arn.value)
DJANGO_SECRET_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .django_secret_key_arn.value)
FERNET_KEYS_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .fernet_keys_arn.value)
TWILIO_AUTH_TOKEN_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .twilio_auth_token_arn.value)
REDIS_TOKEN_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .redis_token_arn.value)
POSTGRES_ADMIN_PW_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .postgres_admin_password_arn.value)
SENTRY_FRONTEND_DSN_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .sentry_frontend_dsn_arn.value)
SENTRY_BACKEND_DSN_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .sentry_backend_dsn_arn.value)
SEGMENT_IO_POSTGRES_ADMIN_PW_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .segment_io_postgres_admin_password_arn.value)
EPIC_CLIENT_ID_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .epic_client_id_arn.value)
EPIC_BACKEND_CLIENT_ID_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .epic_backend_client_id_arn.value)
EPIC_PRIVATE_KEY_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq -r .epic_private_key_arn.value)

# All secret manager ARNs start with the same beginning portion.
# We need to extract that part for AWS Permissions Policy.
# Easier to do in bash than terraform
AWS_SECRETS_MANAGER_BASE_ARN="$(cut -d ':' -f 1,2,3,4,5,6 <<<"$AWS_SECRET_ARN"):"

cd ../../scripts/deployment

REGION="us-west-1"
GIT_HASH=$(git rev-parse HEAD | cut -c35-40)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
GIT_REF="${GIT_BRANCH}-${GIT_HASH}"

API_REPO="jaspr-api-server"
API_DOCKER_TAG="${API_REPO}:${GIT_REF}"
API_ECR_TAG="${API_REGISTRY}:${GIT_REF}"

WORKER_REPO="jaspr-worker"
WORKER_DOCKER_TAG="${WORKER_REPO}:${GIT_REF}"
WORKER_ECR_TAG="${WORKER_REGISTRY}:${GIT_REF}"

SCHEDULER_REPO="jaspr-scheduler"
SCHEDULER_DOCKER_TAG="${SCHEDULER_REPO}:${GIT_REF}"
SCHEDULER_ECR_TAG="${SCHEDULER_REGISTRY}:${GIT_REF}"

# tfenv use 0.13.7
# tfenv use 1.0.2