ENV_FILE="./.env"
rm -f "$ENV_FILE"

# Create a backend config file
# with the bucket and key where the tf state is stored
# These are set in the set_env.sh file
cat > "$ENV_FILE" <<- EOM
REACT_APP_VERSION=\$npm_package_version
REACT_APP_ENVIRONMENT="$1"
REACT_APP_API_ROOT="https://$2/v1"
EOM

#REACT_APP_SENTRY_DSN="$3"
