#!/bin/bash

########
# Deprecated script. This is not used anymore since we've moved to using a custom docker build environment.
# Keeping it around for reference for a few more weeks. -TPC 9/16/2020
# This script is built to run on Bitbucket and install build dependencies
########

# Install lsb_release command
apt-get update
apt-get install -y lsb-release
apt-get install -y software-properties-common
apt-get clean all

# Install Terraform Repo
curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
apt-get update
apt-get install -y terraform=0.12.29
echo "Terraform installed."

# Install Docker-Compose
curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install AWS CLI
apt-get install -y python3-pip
pip3 install -U awscli

mkdir ~/.aws
echo "Made dir"
touch ~/.aws/credentials
touch ~/.aws/config
echo "made files"

cat <<EOT >> ~/.aws/credentials
[default]
aws_access_key_id=$AWS_ACCESS_KEY_ID
aws_secret_access_key=$AWS_SECRET_ACCESS_KEY

[$ENVIRONMENT]
aws_access_key_id=$AWS_ACCESS_KEY_ID
aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
EOT

cat <<EOT >> ~/.aws/config
[profile default]
region = $AWS_REGION
output = json

[profile $ENVIRONMENT]
region = $AWS_REGION
output = json
EOT
