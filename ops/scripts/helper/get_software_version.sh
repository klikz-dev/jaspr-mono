#!/bin/bash

###########
# Pull the current software version off the last commit.
# This is assumed to be run only on the production branch
# where the last commit will be in the form: Release 1.0.8
###########

COMMIT_MSG=$(git log -1)

if [[ $COMMIT_MSG =~ ([0-9]+)\.([0-9]+)\.([0-9]+) ]]; then
  # echo "Found version: ${BASH_REMATCH}"
  echo $BASH_REMATCH
  exit 0
else
  exit 1
fi
