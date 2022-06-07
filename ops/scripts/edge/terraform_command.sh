. ../../scripts/edge/terraform_init.sh

AWS_PROFILE=$AWS_PROFILE terraform "${TERRAFORM_COMMAND}" \
-var "environment=${ENVIRONMENT}" \
-var="git_branch=${GIT_BRANCH}" \
-var="git_hash=${GIT_HASH}" \
-var="git_branch=${GIT_BRANCH}" \
-auto-approve
