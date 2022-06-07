#!/bin/bash

. ../set_env.sh

# Terraform
echo "Starting terraform destroy..."

cd ../../terraform/cdn

TERRAFORM_COMMAND="destroy"
. ../../scripts/cdn/terraform_command.sh

echo "Finished terraform destroy"