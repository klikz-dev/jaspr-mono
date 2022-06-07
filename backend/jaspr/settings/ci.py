"""
Settings for running tests on CI.

Ordering/Derivation Chart:
- root --> base --> ci

With these settings, tests run faster (thanks to `cookiecutter-django` for the base
version/configuration here).
"""

import re

from .mixins.base import *  # isort:skip  # noqa

# General
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="PV3AXPD2eQWDtEYbYIFMrbMXFC3Oc7z6btzfhaPJNko60H7sj4Waej45oo782HAm",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# REDIS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
from .mixins.redis import * # noqa
# Override the CACHES setup to use local memory for testing
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# Passwords
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Templates
# ------------------------------------------------------------------------------
# Django doesn't let you specify `'APP_DIRS': True|False` as of 2.2 when the
# `'loaders'` key is present in `'OPTIONS'`. Hence we pop it, and just include the
# loaders to make the templates render faster (due to caching, etc.) in the tests. This
# was mostly taken from Cookiecutter Django's default test settings.
TEMPLATES[-1].pop("APP_DIRS", None)
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]
# Allow template debugging if `DEBUG` is `True` (`coverage` needs this to measure
# django template coverage).
TEMPLATES[-1]["OPTIONS"]["debug"] = DEBUG

# Email
# ------------------------------------------------------------------------------
from .mixins.email import *


# Migrations In Tests
# ------------------------------------------------------------------------------
#
DATABASES["default"].setdefault("TEST", {})  # noqa F405
# Disable migrations for the tests.
# https://docs.djangoproject.com/en/4.0/ref/settings/#migrate
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-MIGRATION_MODULES
DATABASES["default"]["TEST"]["MIGRATE"] = False  # noqa F405

# Django RQ
# ------------------------------------------------------------------------------
# NOTE: Override this from any other setting. Right now, During the tests, we default
# to `RQ_ASYNC=False` and handle things differently in the tests when need be.
RQ_ASYNC = False
for queue_config in RQ_QUEUES.values():
    queue_config["ASYNC"] = RQ_ASYNC

# Necessary to test admin pages.
SHOW_DEVADMIN = True

# Sentry
# ------------------------------------------------------------------------------
# Disable sentry when running tests.
USE_SENTRY = False

# Clinic Subdomains
# ------------------------------------------------------------------------------
# NOTE: Setting to a URL that will cause tests to break properly when not properly
# redirecting to a clinic subdomain.
FRONTEND_URL_BASE = "*.cicd-or-local-testing-app.jaspr-integration.com"

# Epic
# Note, this key is for testing only.  Do not use a production key here
EPIC_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC9VC3jVUqEtqoA\ntuvNZRA23cSDQ5eN1q0F7ciDzI9J+F6Gd1d3MgIeQcjfhF8YhopKLRFvfIvzak30\n4mvfd/08deG1LKZgxOpbOeBt9gQTaXmK4dq4Me0EL6nD9XcSMlT/Rphn/PUSa01W\nHUYcQ4A922i5rteaopandxkCS/D71QT8i28F03t+AC9gsfnpv1rCzEgVySLBVkFr\nHYh6jTY+Gi0x4HiVDFiqLMwFCpY+EV4+9V+v6IxUuyUXUK9QFWkTQICygghcCJ+V\nYyv+DP3mYm/ls05bHNhwaX1DP8dp3vcFdJm6NkqFFhwdow4XBNlaIH7ukBZY3f01\n+gXiYvepAgMBAAECggEAGDevUvfy+zzeTA8Z5ID77Pi7DUtVFHiUU0DSOEGvRnf1\np1+WmZGVAcfKaQTmoR18jPZs14Tn5fAAHsXjpIcVpmkxwNoAQjqN+7NQiOBCLzV7\nrY8sSglg1vs9zOoWHAbCJpEiJ5MMyhldoBlIgY8E1WS+ZZn+zDHl8W/jjA6ouZ2S\nRbj1WFjT6J2AUQY0Y03icDIPbRg3Ek7cstVYmrb0Cep0pFNofMgVjezoxVrmT+D/\n+Y/klmQLTuV3hRG01EEVi6nEQcGi2yTwygVyMxRrJnXBhH7Q3RLBvpPXT5Ry5N6h\n4hilCTEFHLtuwn9CHlkNAx2e8cimUDZsjg/dzJfcrQKBgQD18lf7nsU7E5wNZ6hF\np9YbhnO01Hjg8N+uPiOXHyd2aRlZgkVZ0AUFVhpBykuJtC5vmPizFIu5pQX1q+xt\ngdm7jTFsoFQFyvbjV3NBZXlmTYssE0YTN6ozJQESMZvcKTQusGkA2hWqAMLQHrIV\nK6dxYlaZwGnIejmB2uPIOeGC9wKBgQDFEV7QC6Zx9xkC5k1dHfWnPuVd7lpMjDZ5\nt1+Hgq7NwujeOm4c5qn9uukEftsncwjVlw7W/CYT2zNi1ECPrb5LgSH73nOeMetK\nPqmz6rxDArA88XlAhDv8/U3qJ7oDlOfGQ4+7JOW1v5U+cGuApGuA8WMKm4TBVort\nvH1+efISXwKBgHXL3cIBOFvkN4DgHeNG0LCcQ/zfKwoptCiDUI6H+GGpUt/hGhA7\nJrx4kdji6C0LJJaEwNEczRNca69P6cxFPiCrLnnljHi9zmPytZwj2vJZv4ebr5ty\ntM0MMyggpJLdFUYrbg9fZLLo7GW73fVv1CHlRK8dTk0b5UFBsolq14zfAoGBAIOE\nESt06vLZvjZiLjU7nkqsPfSO8nJtjJl0WGueOjyVnEVa50ugYMg1afcXFfjg2393\n3W56Pos32bZWAnQgtoO7PUvS7IQhum4FHco1mMh7zdQOLyZwWXyAK/Rd6NUlFf0J\n760sdaTyo45VBlmG4TvfXIKiwVkqAXOhPHsgtP2vAoGAEsofcoyU/sLqsoKWtrwm\nDNY9cs6zB5sRF4AEUII/dAdoH3w5OJNLCSTgzUyjnkGmujzkgCCigbOUl5jRkGu1\n0opRrjqEoiGTFcAmJ9If4V6yduMRR+ccrMTbBFQOfSzZeBpXeJHHWY/cXbTJXSua\nUEPtcz8lZs3ecjWUFCwsZqM=\n-----END PRIVATE KEY-----"
