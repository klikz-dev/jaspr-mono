#!/bin/bash

. ../set_env.sh

# Terraform
echo "Starting terraform destroy..."

cd ../../terraform/edge

TERRAFORM_COMMAND="destroy"
. ../../scripts/edge/terraform_command.sh

echo "Finished terraform destroy"