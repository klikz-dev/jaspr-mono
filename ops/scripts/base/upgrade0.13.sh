#!/bin/bash

. ../set_env.sh

cd ../../terraform/base

# TERRAFORM_COMMAND="0.13upgrade"
# . ../../scripts/base/terraform_init.sh

AWS_PROFILE=$AWS_PROFILE terraform "0.13upgrade"