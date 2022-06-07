CONFIG_FILE="/tmp/${ENVIRONMENT}.config"
rm -f "$CONFIG_FILE"

# Create a backend config file
# with the bucket and key where the tf state is stored
# These are set in the set_env.sh file
cat > "$CONFIG_FILE" <<- EOM
bucket = "${TERRAFORM_STATE_BUCKET}"
key = "CDN_${TERRAFORM_STATE_KEY}"
EOM

# They store references to the bucket and keys here. Nuke the folder!
rm -rf .terraform

AWS_PROFILE=$AWS_PROFILE terraform init -backend-config="${CONFIG_FILE}"
