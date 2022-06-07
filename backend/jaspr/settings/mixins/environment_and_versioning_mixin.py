"""
Settings mixin for Django for environment and versioning.

Ordering/Derivation Chart:
- root --> environment_and_versioning_mixin
"""
from .root import *  # isort:skip  # noqa

ENVIRONMENT = env("ENVIRONMENT", default="development").lower()
GIT_BRANCH = env("GIT_BRANCH")

CI_ENVIRONMENT = "ci"
TEST_ENVIRONMENT = "test"
LOCAL_ENVIRONMENT = "local"
DEV_ENVIRONMENT = "development"
INT_ENVIRONMENT = "integration"
PROD_ENVIRONMENT = "production"

ENVIRONMENTS = (
    CI_ENVIRONMENT,
    TEST_ENVIRONMENT,
    LOCAL_ENVIRONMENT,
    DEV_ENVIRONMENT,
    INT_ENVIRONMENT,
    PROD_ENVIRONMENT
)

if ENVIRONMENT not in ENVIRONMENTS:
    raise Exception(
        f"Environment is not set to one of the allowed options. Value: {ENVIRONMENT} Options: {ENVIRONMENTS}"
    )

VERSION = "v1.0.6"
