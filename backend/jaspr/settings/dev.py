"""
Settings for production (and integration).

Ordering/Derivation Chart:
- root --> base --> sentry_mixin (if specified) --> storages_mixin --> dev
"""

from .mixins.base import *  # isort:skip  # noqa

if USE_SENTRY:
    from .mixins.sentry_mixin import *  # isort:skip  # noqa

from .mixins.storages_mixin import *  # isort:skip  # noqa

SHOW_DEVADMIN = True

# General
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = True

# Databases
# ------------------------------------------------------------------------------
DATABASES["default"] = env.db("DATABASE_URL")  # noqa F405
# * NOTE/TODO: See comment on `ATOMIC_REQUESTS` in `base.py`.
DATABASES["default"]["ATOMIC_REQUESTS"] = False  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=0)  # noqa F405


# Fixtures
# ------------------------------------------------------------------------------
# By including the `bootstrap` app, can not only load fixtures, but can get access to
# the management commands for dumping specific fixtures (putting something like
# `FIXTURE_DIRS += [str(APPS_DIR / "bootstrap" / "fixtures")]` makes it so that you can
# only load the fixtures).
INSTALLED_APPS += ["jaspr.apps.bootstrap.apps.BootstrapConfig"]


# Caches
# ------------------------------------------------------------------------------
# REDIS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
from .mixins.redis import * # noqa

# Templates
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# Email
# ------------------------------------------------------------------------------
from .mixins.email import *

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL  # noqa F405
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True  # Offline compression is required when using Whitenoise
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_FILTERS
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": ["compressor.filters.jsmin.JSMinFilter"],
}

# Logging
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# NOTE/TODO: Refactor during settings refactor.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

################################################################
# On Fargate we're serving an IP address for the load balancer
################################################################
ALLOWED_HOSTS = ["*"]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405

# Security
# ------------------------------------------------------------------------------
# Content-Security-Policy -- needs to be set after storages mixin
# Using https://github.com/mozilla/django-csp
CSP_DEFAULT_SRC = ["'self'", AWS_S3_CUSTOM_DOMAIN]
