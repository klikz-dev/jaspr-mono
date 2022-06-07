CONFIG_FILE="/tmp/edge-${ENVIRONMENT}.config"
rm -f "$CONFIG_FILE"

export AWS_ACCESS_KEY_ID="$(aws configure get aws_access_key_id --profile $ENVIRONMENT)"
export AWS_SECRET_ACCESS_KEY="$(aws configure get aws_secret_access_key --profile $ENVIRONMENT)"
export AWS_DEFAULT_REGION="us-east-1"

# Create a backend config file
# with the bucket and key where the tf state is stored
# These are set in the set_env.sh file
cat > "$CONFIG_FILE" <<- EOM
bucket = "${TERRAFORM_STATE_BUCKET}"
key = "EDGE_${TERRAFORM_STATE_KEY}"
EOM

# They store references to the bucket and keys here. Nuke the folder!
rm -rf .terraform

terraform init -backend-config="${CONFIG_FILE}"
rm -f "$CONFIG_FILE"