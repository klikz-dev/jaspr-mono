#!/bin/bash

####################################
# Setup Variables
####################################
. ../set_env.sh
. vars.sh

####################################
# Terraform
####################################
echo "Starting terraform destroy..."

cd ../../terraform/deployment

. ../../scripts/deployment/terraform_init_deployment.sh
TERRAFORM_COMMAND="destroy"
. ../../scripts/deployment/terraform_command.sh

echo "Finished terraform destroy"