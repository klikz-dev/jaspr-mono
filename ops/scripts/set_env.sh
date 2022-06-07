#!/bin/bash

AWS_PROFILE=$1
export AWS_PROFILE

if [ "$1" == "prod" ]; then
  ENVIRONMENT="production"
  TERRAFORM_STATE_BUCKET="jaspr-production-terraform-state"
  TERRAFORM_STATE_KEY="default.tfstate"
elif [ "$1" == "int" ]; then
  ENVIRONMENT="integration"
  TERRAFORM_STATE_BUCKET="jaspr-terraform-state-integration"
  TERRAFORM_STATE_KEY="default.tfstate"
elif [ "$1" == "dev" ]; then
  ENVIRONMENT="development"
  TERRAFORM_STATE_BUCKET="jaspr-terraform-state-development"
  TERRAFORM_STATE_KEY="$(git rev-parse --abbrev-ref HEAD).tfstate"
else
  echo "Please specify the environment with the first variable. Either prod, int, or dev."
  exit
fi
