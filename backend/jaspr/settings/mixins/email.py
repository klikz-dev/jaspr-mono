from .base import (
    env,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    INSTALLED_APPS,
    ENVIRONMENT,
    CI_ENVIRONMENT,
    TEST_ENVIRONMENT,
    LOCAL_ENVIRONMENT,
    DEV_ENVIRONMENT,
    INT_ENVIRONMENT,
    PROD_ENVIRONMENT,
)

# BASE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Jaspr Health <noreply@jasprhealth.com>"
)
SERVER_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Jaspr Health <noreply@jasprhealth.com>"
)
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[Jaspr Health]"
)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# Environment Config
# We have an email configuration blocks for each environment below
###################

#if ENVIRONMENT in (CI_ENVIRONMENT, TEST_ENVIRONMENT):
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

if ENVIRONMENT is LOCAL_ENVIRONMENT:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST", default="127.0.0.1")
    EMAIL_PORT = env.int("EMAIL_PORT", default=1039)

if ENVIRONMENT in (DEV_ENVIRONMENT, INT_ENVIRONMENT, PROD_ENVIRONMENT):
    # We use SES in us-west-1 for Production but us-west-2 for dev and integration
    # It would be nice to make this consistent in the future
    EMAIL_AWS_REGION = "us-west-1"
    if ENVIRONMENT in (DEV_ENVIRONMENT, INT_ENVIRONMENT):
        EMAIL_AWS_REGION = "us-west-2"

    INSTALLED_APPS += ["anymail"]  # noqa F405
    EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
    ANYMAIL = {
        "AMAZON_SES_CLIENT_PARAMS": {
            # example: override normal Boto credentials specifically for Anymail
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            "region_name": EMAIL_AWS_REGION,
            # override other default options
            "config": {"connect_timeout": 30, "read_timeout": 30,},
        },
    }
