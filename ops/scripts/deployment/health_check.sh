#!/bin/bash

TEST_ENDPOINT="http://localhost:5000/health-check"
i=0
timeout=210 # 3.5 minutes
while : ; # Loop until broken

do
  ((i += 5))

  HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" "${TEST_ENDPOINT}")

  if [ $HTTP_STATUS != "" ]; then
    echo "Status Code: $HTTP_STATUS" 
  fi
  

  # Stop checking if health check passes
  if [ $HTTP_STATUS == "200" ]; then
    break
  fi

  # Exit (1) if health check times out
  # after logging failure information to stdout
  if [ "${i}" -gt $timeout ]; then
        echo "HTTP Status: ${HTTP_STATUS}"
        RES=$(curl -sb -H "Accept: application/json" "${TEST_ENDPOINT}")
        ERROR=$(curl -o /dev/null -s -w "%{json}\n%{errormsg}\n" "${TEST_ENDPOINT}")
        echo "API Server responded with Non-200 Response"
        echo "---------"
        echo "${RES}"
        echo "${ERROR}"
        echo "---------"
        exit 1
    fi

    # Update stdout every 30 seconds
    if [[ $(($i % 30)) == 0 ]]; then
        echo "Checking health..."
    fi

    # Check once every 5 seconds
    sleep 5
done

echo "Health Check passed after "$((i-5))" seconds"
