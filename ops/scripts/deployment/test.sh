#!/bin/bash

####################################
# Setup Variables
####################################
. ../set_env.sh
. vars.sh

####################################
# Build
####################################
echo "Starting build..."
cd ../../docker || exit

SCHEDULER_DOCKER_TAG="${SCHEDULER_DOCKER_TAG}" WORKER_DOCKER_TAG="${WORKER_DOCKER_TAG}" API_DOCKER_TAG="${API_DOCKER_TAG}" docker-compose -f deployment.yml build

echo "Build complete."

####################################
# Test
####################################
echo "Starting testing..."

echo "SCHEDULER_DOCKER_TAG=${SCHEDULER_DOCKER_TAG} WORKER_DOCKER_TAG=${WORKER_DOCKER_TAG} API_DOCKER_TAG=${API_DOCKER_TAG} docker-compose up -d"
SCHEDULER_DOCKER_TAG="${SCHEDULER_DOCKER_TAG}" WORKER_DOCKER_TAG="${WORKER_DOCKER_TAG}" API_DOCKER_TAG="${API_DOCKER_TAG}" docker-compose -f deployment.yml up -d

echo "Starting up..."
sleep 30
echo "..."
sleep 30
echo "..."
sleep 30
echo "checking..."

TEST_ENDPOINT="http://localhost:5000/health-check?auth=7qp6FnKJLYHa3F6y"
HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" "${TEST_ENDPOINT}")
echo "HTTP Status: ${HTTP_STATUS}"

echo "Down"
SCHEDULER_DOCKER_TAG="${SCHEDULER_DOCKER_TAG}" WORKER_DOCKER_TAG="${WORKER_DOCKER_TAG}" API_DOCKER_TAG="${API_DOCKER_TAG}" docker-compose -f deployment.yml down

if [ $HTTP_STATUS != "200" ]; then
  RES=$(curl -sb -H "Accept: application/json" "${TEST_ENDPOINT}")
  ERROR=$(curl -o /dev/null -s -w "%{json}\n%{errormsg}\n" "${TEST_ENDPOINT}")
  echo "API Server responded with Non-200 Response"
  echo "---------"
  echo "${RES}"
  echo "${ERROR}"
  echo "---------"
  exit 1
fi

cd ../scripts/deployment || exit
echo "Testing complete."