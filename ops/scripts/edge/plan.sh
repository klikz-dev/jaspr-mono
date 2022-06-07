#!/bin/bash

. ../set_env.sh

cd ../../terraform/edge

AWS_PROFILE=$AWS_PROFILE terraform "plan" \
-var "environment=${ENVIRONMENT}" \
-var="git_branch=${GIT_BRANCH}" \
-var="git_hash=${GIT_HASH}" \
-var="git_branch=${GIT_BRANCH}"

