#!/bin/bash

echo "Starting up..."
. ../set_env.sh

echo "Assigning vars..."
. vars.sh

cd ../../terraform/edge

TERRAFORM_COMMAND="apply"
. ../../scripts/edge/terraform_command.sh

