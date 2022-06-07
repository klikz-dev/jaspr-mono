#!/bin/bash

. ../set_env.sh

# Terraform
echo "Starting terraform destroy..."

cd ../../terraform/base

TERRAFORM_COMMAND="destroy"
. ../../scripts/base/terraform_command.sh

echo "Finished terraform destroy"