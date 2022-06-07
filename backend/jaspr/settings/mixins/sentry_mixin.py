"""
Settings mixin for Django for Sentry.

Ordering/Derivation Chart:
- root --> environment_and_versioning_mixin --> sentry_mixin
"""
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.rq import RqIntegration

from .environment_and_versioning_mixin import *  # isort:skip  # noqa


SENTRY_DSN = env("SENTRY_DSN")
SENTRY_SEND_PII = env.bool("SENTRY_SEND_PII", ENVIRONMENT != "production")

if ENVIRONMENT == "production":
    release = VERSION
elif ENVIRONMENT == "development":
    release = f"{env('GIT_BRANCH')}@{env('GIT_HASH')}"
elif ENVIRONMENT == "local":
    release = None
else:
    release = env("GIT_HASH")

if SENTRY_DSN:
    SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)
    SENTRY_EVENT_LEVEL = env.int("DJANGO_SENTRY_EVENT_LEVEL", logging.WARNING)

    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs (default)
        event_level=SENTRY_EVENT_LEVEL,  # Send errors as events (default)
    )
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        debug=True,
        integrations=[
            sentry_logging,
            DjangoIntegration(),
            RedisIntegration(),
            RqIntegration(),
        ],
        release=release,
        send_default_pii=SENTRY_SEND_PII,
    )
