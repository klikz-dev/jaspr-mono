#!/bin/bash

. ../set_env.sh

cd ../../terraform/cdn

TERRAFORM_COMMAND="plan"
. ../../scripts/cdn/terraform_command.sh

