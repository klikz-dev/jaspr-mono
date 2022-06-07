#!/bin/bash

mkdir ~/.aws
touch ~/.aws/credentials
touch ~/.aws/config

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
