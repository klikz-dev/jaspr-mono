#!/bin/bash

. ../set_env.sh

cd ../../terraform/cdn

. ../../scripts/cdn/terraform_init.sh

AWS_PROFILE=$AWS_PROFILE terraform state rm "${2}"
