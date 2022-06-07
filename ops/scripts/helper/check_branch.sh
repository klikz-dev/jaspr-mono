#!/bin/bash

####
# This script errors out if the first argument provided does not match the current git branch
####

if [ "$BITBUCKET_BRANCH" != "$1" ];
then
  echo "Not on $1. Exiting."
  exit 1;
else
  echo "On $1. Continuing."
  exit 0;
fi