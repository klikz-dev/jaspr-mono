. ../../scripts/base/terraform_init.sh

AWS_PROFILE=$AWS_PROFILE TF_LOG=debug terraform "${TERRAFORM_COMMAND}" \
-var "environment=${ENVIRONMENT}"