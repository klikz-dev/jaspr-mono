#!/bin/bash

echo "Intializing base project to get values out..."
# Make sure base is initialized before pulling values from it.
cd ../../scripts/base
. ./init.sh

cd ../../terraform/base

AWS_SECRET_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq .aws_secret_key_arn.value)
AWS_ACCESS_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output -json | jq .aws_access_key_arn.value)

echo "Got what we needed from base project."

REGION="us-east-1"
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

cd ../../scripts/edge
