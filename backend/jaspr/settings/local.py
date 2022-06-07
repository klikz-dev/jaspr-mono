"""
Settings for Django for local development.

Ordering/Derivation Chart:
- root --> local_mixin --> base -> storages_mixin -> local
"""
import sys
import logging
from .mixins.local_mixin import *  # isort:skip  # noqa
from .dev import *  # isort:skip  # noqa

DEBUG = True

# General
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        BACKEND_SITE_DOMAIN,
        "localhost",
        "0.0.0.0",
        "127.0.0.1",
    ],
)

# django-debug-toolbar
# ------------------------------------------------------------------------------
# NOTE: Will need to have `django-debug-toolbar` installed
# (https://github.com/jazzband/django-debug-toolbar). It's intentionally not listed in
# `requirements/local.txt`.
if DEBUG and env.bool("DJANGO_RUN_DEBUG_TOOLBAR", default=False):
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
    INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# django-silk (profiling)
# ------------------------------------------------------------------------------
# NOTE: Will need to have `django-silk` installed
# (https://github.com/jazzband/django-silk). It's intentionally not listed in
# `requirements/local.txt`.
if DEBUG and env.bool("DJANGO_RUN_PROFILING", default=False):
    MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")
    INSTALLED_APPS.append("silk")
    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True

# Extra Configuration for Docker
# ------------------------------------------------------------------------------
if env.bool("USE_DOCKER", default=False) == "yes":
    import socket  # isort:skip

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

    # NOTE: If we're running Django from outside of docker, we may need to specify
    # Docker's IP (useful on docker toolbox for windows, for example) in order to make
    # sure we're connecting to the right spot.
    DOCKER_IP = env("DOCKER_IP", default="")
    if DOCKER_IP:
        if DOCKER_IP not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(DOCKER_IP)
        if DOCKER_IP not in INTERNAL_IPS:
            INTERNAL_IPS.append(DOCKER_IP)

# Static
# ------------------------
# NOTE: Use the default Django staticfiles for local development.
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405

# CORS
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Email
# ------------------------------------------------------------------------------
from .mixins.email import *

# NOTE/TODO: Refactor during settings refactor.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
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

# Security
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
#CSRF_TRUSTED_ORIGINS = "localhost"
#CSRF_COOKIE_DOMAIN = "localhost"
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')

CSP_DEFAULT_SRC = ["'self'", AWS_S3_CUSTOM_DOMAIN, "'unsafe-inline'"] + ALLOWED_HOSTS

# Note, this key is for testing only.  Do not use a production key here
#EPIC_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC9VC3jVUqEtqoA\ntuvNZRA23cSDQ5eN1q0F7ciDzI9J+F6Gd1d3MgIeQcjfhF8YhopKLRFvfIvzak30\n4mvfd/08deG1LKZgxOpbOeBt9gQTaXmK4dq4Me0EL6nD9XcSMlT/Rphn/PUSa01W\nHUYcQ4A922i5rteaopandxkCS/D71QT8i28F03t+AC9gsfnpv1rCzEgVySLBVkFr\nHYh6jTY+Gi0x4HiVDFiqLMwFCpY+EV4+9V+v6IxUuyUXUK9QFWkTQICygghcCJ+V\nYyv+DP3mYm/ls05bHNhwaX1DP8dp3vcFdJm6NkqFFhwdow4XBNlaIH7ukBZY3f01\n+gXiYvepAgMBAAECggEAGDevUvfy+zzeTA8Z5ID77Pi7DUtVFHiUU0DSOEGvRnf1\np1+WmZGVAcfKaQTmoR18jPZs14Tn5fAAHsXjpIcVpmkxwNoAQjqN+7NQiOBCLzV7\nrY8sSglg1vs9zOoWHAbCJpEiJ5MMyhldoBlIgY8E1WS+ZZn+zDHl8W/jjA6ouZ2S\nRbj1WFjT6J2AUQY0Y03icDIPbRg3Ek7cstVYmrb0Cep0pFNofMgVjezoxVrmT+D/\n+Y/klmQLTuV3hRG01EEVi6nEQcGi2yTwygVyMxRrJnXBhH7Q3RLBvpPXT5Ry5N6h\n4hilCTEFHLtuwn9CHlkNAx2e8cimUDZsjg/dzJfcrQKBgQD18lf7nsU7E5wNZ6hF\np9YbhnO01Hjg8N+uPiOXHyd2aRlZgkVZ0AUFVhpBykuJtC5vmPizFIu5pQX1q+xt\ngdm7jTFsoFQFyvbjV3NBZXlmTYssE0YTN6ozJQESMZvcKTQusGkA2hWqAMLQHrIV\nK6dxYlaZwGnIejmB2uPIOeGC9wKBgQDFEV7QC6Zx9xkC5k1dHfWnPuVd7lpMjDZ5\nt1+Hgq7NwujeOm4c5qn9uukEftsncwjVlw7W/CYT2zNi1ECPrb5LgSH73nOeMetK\nPqmz6rxDArA88XlAhDv8/U3qJ7oDlOfGQ4+7JOW1v5U+cGuApGuA8WMKm4TBVort\nvH1+efISXwKBgHXL3cIBOFvkN4DgHeNG0LCcQ/zfKwoptCiDUI6H+GGpUt/hGhA7\nJrx4kdji6C0LJJaEwNEczRNca69P6cxFPiCrLnnljHi9zmPytZwj2vJZv4ebr5ty\ntM0MMyggpJLdFUYrbg9fZLLo7GW73fVv1CHlRK8dTk0b5UFBsolq14zfAoGBAIOE\nESt06vLZvjZiLjU7nkqsPfSO8nJtjJl0WGueOjyVnEVa50ugYMg1afcXFfjg2393\n3W56Pos32bZWAnQgtoO7PUvS7IQhum4FHco1mMh7zdQOLyZwWXyAK/Rd6NUlFf0J\n760sdaTyo45VBlmG4TvfXIKiwVkqAXOhPHsgtP2vAoGAEsofcoyU/sLqsoKWtrwm\nDNY9cs6zB5sRF4AEUII/dAdoH3w5OJNLCSTgzUyjnkGmujzkgCCigbOUl5jRkGu1\n0opRrjqEoiGTFcAmJ9If4V6yduMRR+ccrMTbBFQOfSzZeBpXeJHHWY/cXbTJXSua\nUEPtcz8lZs3ecjWUFCwsZqM=\n-----END PRIVATE KEY-----"
