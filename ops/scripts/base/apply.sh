#!/bin/bash

. ../set_env.sh

cd ../../terraform/base

TERRAFORM_COMMAND="apply"
. ../../scripts/base/terraform_command.sh

