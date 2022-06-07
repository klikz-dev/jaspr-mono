#!/bin/bash

. ../set_env.sh

cd ../../terraform/base

. ../../scripts/base/terraform_init.sh

AWS_PROFILE=$AWS_PROFILE terraform import "${2}" "${3}"
