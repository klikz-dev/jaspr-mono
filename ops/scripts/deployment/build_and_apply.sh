#!/bin/bash
#set -e

####################################
# Setup Variables
####################################
. ../set_env.sh

DEFAULT_FIXTURE_LIST_DEV="./jaspr/apps/bootstrap/fixtures/jaspr_root.json;./jaspr/apps/bootstrap/fixtures/jaspr_content.json;./jaspr/apps/bootstrap/fixtures/jaspr_dev_only.json;./jaspr/apps/bootstrap/fixtures/jaspr_user.json"

if [ $# -lt 2 ];
  then
    LOAD_FIXTURES="False"
  else
    LOAD_FIXTURES=$2

    if [ $LOAD_FIXTURES = "True" ];
    then
      if [ $# -lt 3 ]
        then
          echo "Provide list of fixtures to load."
          exit
        else
          FIXTURE_LIST=$3
      fi
    fi
fi

. vars.sh

cd ../../terraform/deployment || exit
. ../../scripts/deployment/terraform_init_deployment.sh || exit
cd ../../scripts/deployment || exit

####################################
# Build
####################################
echo "Starting build..."
cd ../../docker || exit

SCHEDULER_DOCKER_TAG="${SCHEDULER_DOCKER_TAG}" WORKER_DOCKER_TAG="${WORKER_DOCKER_TAG}" API_DOCKER_TAG="${API_DOCKER_TAG}" docker-compose -f deployment.yml build || exit

echo "Build complete."

####################################
# Test
####################################
echo "Starting testing..."

echo "SCHEDULER_DOCKER_TAG=${SCHEDULER_DOCKER_TAG} WORKER_DOCKER_TAG=${WORKER_DOCKER_TAG} API_DOCKER_TAG=${API_DOCKER_TAG} docker-compose -f deployment.yml up -d"
SCHEDULER_DOCKER_TAG="${SCHEDULER_DOCKER_TAG}" WORKER_DOCKER_TAG="${WORKER_DOCKER_TAG}" API_DOCKER_TAG="${API_DOCKER_TAG}" docker-compose -f deployment.yml up -d

# Check that the test server starts up and exit if it doesn't
source ../scripts/deployment/health_check.sh || exit

echo "Shutting down test server"
SCHEDULER_DOCKER_TAG="${SCHEDULER_DOCKER_TAG}" WORKER_DOCKER_TAG="${WORKER_DOCKER_TAG}" API_DOCKER_TAG="${API_DOCKER_TAG}" docker-compose -f deployment.yml down

cd ../scripts/deployment || exit
echo "Testing complete."

####################################
# Tag
####################################
echo "Starting tagging..."

# Tag API Server and Push to ECR
docker tag "$API_DOCKER_TAG" "$API_ECR_TAG"

# Tag Worker and Push to ECR
docker tag "$WORKER_DOCKER_TAG" "$WORKER_ECR_TAG"

# Tag Scheduler and Push to ECR
docker tag "$SCHEDULER_DOCKER_TAG" "$SCHEDULER_ECR_TAG"

echo "Tagging complete."

####################################
# Upload to ECR
####################################
echo "Starting Push to ECR..."

# Login to ECR via Docker
aws ecr get-login-password --region "${REGION}" | docker login --username AWS --password-stdin "${REGISTRY}"

# Push API Server to ECR
docker push "$API_ECR_TAG"

# Push Worker to ECR
docker push "$WORKER_ECR_TAG"

# Push Scheduler to ECR
docker push "$SCHEDULER_ECR_TAG"

echo "Push to ECR complete."

####################################
# Run Terraform
####################################
echo "Starting terraform build..."

cd ../../terraform/deployment || exit

TERRAFORM_COMMAND="apply"
. ../../scripts/deployment/terraform_command.sh

# They store references to the bucket and keys here. Nuke the folder!
rm -rf .terraform

echo "Terraform build complete."

if [ "${ENVIRONMENT}" = "development" ];
then
  echo "Deployed to..."
  echo "Web FE: https://jaspr-test--${GIT_BRANCH}.app.jaspr-development.com/"
  echo "Storybook: https://storybook.jaspr-development.com/${GIT_BRANCH}/index.html"
  echo "Django Admin: https://${GIT_BRANCH}.api.jaspr-development.com/ebpiadmin/"
  echo "Expo Channel: https://expo.io/@jasprhealth/jah?release-channel=aws-development-${GIT_BRANCH}"
fi
