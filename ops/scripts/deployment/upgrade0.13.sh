#!/bin/bash

. ../set_env.sh

cd ../../terraform/deployment

AWS_PROFILE=$AWS_PROFILE terraform "0.13upgrade"