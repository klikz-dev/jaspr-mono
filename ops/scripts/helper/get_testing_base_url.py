import sys

"""
Convert the git branch name into the deployment URL.
Used for UI Testing.

production: https://qa.app.jasprhealth.com
integration: https://qa.app.jaspr-integration.com
development: https://jaspr-test--{git_branch}.app.jaspr-development.com
"""

environment = sys.argv[1]
branch = sys.argv[2]

if branch is None or len(branch) == 0:
    print("Branch name not supplied")
    sys.exit(1)

if environment is None or len(environment) == 0:
    print("Environment name not supplied")
    sys.exit(1)

PRODUCTION = "production"
INTEGRATION = "integration"
DEVELOPMENT = "development"

PRODUCTION_URL = "https://qa.app.jasprhealth.com"
INTEGRATION_URL = "https://qa.app.jaspr-integration.com"
DEVELOPMENT_URL = f"https://jaspr-test--{branch}.app.jaspr-development.com"

if environment == PRODUCTION:
    print(PRODUCTION_URL)
elif environment == INTEGRATION:
    print(INTEGRATION_URL)
elif environment == DEVELOPMENT:
    print(DEVELOPMENT_URL)
else:
    print(f"Invalid environment provided: {environment}")
    sys.exit(1)

sys.exit(0)