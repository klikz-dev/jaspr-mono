#!/bin/bash
set -e

# AWS Dev ECR Repo
REGISTRY="128206503653.dkr.ecr.us-west-1.amazonaws.com"
REPO="jaspr-base-server"
TAG="latest"
LOCAL_TAG="${REPO}:${TAG}"
REMOTE_TAG="${REGISTRY}/${REPO}:${TAG}"
ACCESS_KEY=$(aws configure --profile=dev get aws_access_key_id)
SECRET_KEY=$(aws configure --profile=dev get aws_secret_access_key)

# Build
cd ../../../docker/base-server
docker build -t "${LOCAL_TAG}" .

# Test
CONTAINER_ID=$(docker create --env-file ../envs/build.env -e AWS_ACCESS_KEY_ID=$ACCESS_KEY -e AWS_SECRET_ACCESS_KEY=$SECRET_KEY "${LOCAL_TAG}")
docker start "${CONTAINER_ID}"

echo "Checking tools"
#docker exec -it "${CONTAINER_ID}" pipenv --version
echo "Done."

docker stop "${CONTAINER_ID}"

echo "Upload image"

# Upload
../../scripts/docker/shared/ecr_tag.sh "dev" "us-west-1" "${REGISTRY}" "${LOCAL_TAG}" "${REMOTE_TAG}"

echo "Complete."
