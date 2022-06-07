#!/bin/bash

. ../set_env.sh
. vars.sh

cd ../../terraform/cdn

TERRAFORM_COMMAND="apply"
. ../../scripts/cdn/terraform_command.sh

