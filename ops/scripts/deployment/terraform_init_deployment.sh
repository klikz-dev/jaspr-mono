CONFIG_FILE="/tmp/${ENVIRONMENT}.config"
rm -f "$CONFIG_FILE"

export AWS_ACCESS_KEY_ID="$(aws configure get aws_access_key_id --profile $AWS_PROFILE)"
export AWS_SECRET_ACCESS_KEY="$(aws configure get aws_secret_access_key --profile $AWS_PROFILE)"
export AWS_DEFAULT_REGION="us-west-1"

# Create a backend config file
# with the bucket and key where the tf state is stored
# These are set in the set_env.sh file
cat > "$CONFIG_FILE" <<- EOM
bucket = "${TERRAFORM_STATE_BUCKET}"
key = "${TERRAFORM_STATE_KEY}"
EOM

terraform init -backend-config="${CONFIG_FILE}"

rm -f "$CONFIG_FILE"
