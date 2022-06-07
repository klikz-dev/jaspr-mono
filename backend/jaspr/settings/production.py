"""
Settings for production (and integration).

Ordering/Derivation Chart:
- root --> base --> storages_mixin --> sentry_mixin -->  --> production
"""

# Note: storage mixin imports base
from .mixins.storages_mixin import *  # isort:skip  # noqa
if USE_SENTRY:
    from .mixins.sentry_mixin import *  # isort:skip  # noqa

# General
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# Don't allow `DEBUG = True` in production.
DEBUG = False

# Databases
# ------------------------------------------------------------------------------
DATABASES["default"] = env.db("DATABASE_URL")  # noqa F405
# * NOTE/TODO: See comment on `ATOMIC_REQUESTS` in `base.py`.
DATABASES["default"]["ATOMIC_REQUESTS"] = False  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=30)  # noqa F405


# Fixtures
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS += [str(APPS_DIR / "bootstrap" / "fixtures")]


# Caches
# ------------------------------------------------------------------------------
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
# NOTE/TODO: Logging settings refactor
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
        "EPIC": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        }
    },
}

################################################################
# On Fargate we're serving an IP address for the load balancer
################################################################
ALLOWED_HOSTS = ["*"]

# Security
# ------------------------------------------------------------------------------
# Content-Security-Policy -- needs to be set after storages mixin
# Using https://github.com/mozilla/django-csp
# NOTE/TODO: Refactor in settings refactor.
CSP_DEFAULT_SRC = ["'self'", AWS_S3_CUSTOM_DOMAIN]

# Deprecated URLs
# ------------------------------------------------------------------------------
INCLUDE_DEPRECATED_URLS = True
