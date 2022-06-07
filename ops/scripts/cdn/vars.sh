#!/bin/bash

cd ../../terraform/cdn

# Make sure base is initialized before pulling values from it.
#. ../../scripts/base/terraform_init.sh

AWS_SECRET_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output aws_secret_key_arn)
AWS_ACCESS_ARN=$(AWS_PROFILE=$AWS_PROFILE terraform output aws_access_key_arn)

REGION="us-east-1"
GIT_HASH=$(git rev-parse HEAD | cut -c35-40)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
GIT_REF="${GIT_BRANCH}-${GIT_HASH}"
