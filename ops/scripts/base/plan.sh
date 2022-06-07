#!/bin/bash

. ../set_env.sh

cd ../../terraform/base

TERRAFORM_COMMAND="plan"
. ../../scripts/base/terraform_command.sh

