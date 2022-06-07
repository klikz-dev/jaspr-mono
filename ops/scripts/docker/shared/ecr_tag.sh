#!/bin/bash

# Arguments
# 1) AWS Profile Name
# 2) AWS Region Name
# 3) Registry Url
# 4) Local Tag
# 5) ECR Tag

# Login to ECR via Docker
AWS_PROFILE="${1}" aws ecr get-login-password --region "${2}" | docker login --username AWS --password-stdin "${3}"

# Tag API Server and Push to ECR
docker tag "${4}" "${5}"

# Push API Server to ECR
docker push "${5}"
exit 0