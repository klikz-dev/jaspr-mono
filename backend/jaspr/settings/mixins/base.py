"""
Base settings to build other settings files upon.

Ordering/Derivation Chart:
- root --> base
"""
import base64
from datetime import timedelta
from urllib.parse import urlparse
from cryptography.hazmat.primitives import serialization

from .environment_and_versioning_mixin import *  # isort:skip  # noqa

# General
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Allowing /devadmin/ login to exist
SHOW_DEVADMIN = False
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "US/Central"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# Databases
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
# * NOTE/TODO: Jaspr, at the time of writing, does not have atomic requests turned on
# * (so I set this to `False` when refactoring settings). Should we turn it on by
# * default?
DATABASES["default"]["ATOMIC_REQUESTS"] = False

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# URLs
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "jaspr.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "jaspr.wsgi.application"

# Apps
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "simple_history",
    "rest_framework",
    "taggit",
    "session_security",
    "phonenumber_field",
    "django_rq",
    "scheduler",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "knox",
    "django_twilio",
    "django_filters",
    "corsheaders",
    "compressor",
    # * NOTE/TODO: Do we want this? Or just in dev?
    "crispy_forms",
    "colorful",
    "netfields",
    "django_better_admin_arrayfield",
    "adminsortable2",
    "django_json_widget",
]

LOCAL_APPS = [
    "jaspr.apps.accounts.apps.AccountsConfig",
    "jaspr.apps.api.apps.APIConfig",
    "jaspr.apps.awsmedia.apps.AWSMediaConfig",
    "jaspr.apps.clinics.apps.ClinicsConfig",
    "jaspr.apps.common.apps.CommonConfig",
    "jaspr.apps.jah.apps.JAHConfig",
    "jaspr.apps.kiosk.apps.KioskConfig",
    "jaspr.apps.message_logs.apps.MessageLogsConfig",
    "jaspr.apps.stability_plan.apps.StabilityPlanConfig",
    "jaspr.apps.epic.apps.EpicConfig"
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Migrations
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "jaspr.apps.contrib.sites.migrations"}

# Authentication
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "accounts.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
# NOTE: Setting to "/" since we're not using Django template-style views or
# functionality outside of the admin.
LOGIN_REDIRECT_URL = "/"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
# NOTE: Setting to "/" since we're not using Django template-style views or
# functionality outside of the admin.
LOGIN_URL = "/"

# Passwords
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# No Validation at this time.
AUTH_PASSWORD_VALIDATORS = []

# Password reset links are valid for this many days
PASSWORD_RESET_TIMEOUT = 15 * 3600 * 24

# Middleware
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_feature_policy.FeaturePolicyMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "session_security.middleware.SessionSecurityMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    # "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django_otp.middleware.OTPMiddleware",
]

# Static
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = []
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Media
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(ROOT_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# Templates
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [
            "templates",
            "jaspr/apps/kiosk/activities/intro/questions",
            "jaspr/apps/kiosk/activities/outro/questions",
            "jaspr/apps/kiosk/activities/lethal_means/questions",
            "jaspr/apps/kiosk/activities/stability_plan/questions",
            "jaspr/apps/kiosk/activities/suicide_assessment/questions",
            "jaspr/apps/kiosk/activities/comfort_and_skills/questions",
        ],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "jaspr.apps.common.context_processors.environment",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# * NOTE/TODO: Do we want this? Or just in dev? See comment higher up above too.
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Fixtures
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = []

# Security
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
#X_FRAME_OPTIONS = 'deny'
# * NOTE/TODO: Do we still want these settings (assuming it's really for Django-admin
# * since we're not using sessions outside of that).
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 300

SESSION_COOKIE_SAMESITE = False

# Admin
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = env("DJANGO_ADMIN_URL", default="ebpiadmin/")
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
# * NOTE/TODO: Set this up with the admin email(s) either hard coded or using settings.
ADMINS = [("""Jaspr Dev Admin""", "devadmin@jasprhealth.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# Logging
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# NOTE/TODO: Refactor in/during settings refactor.
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
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Sites and URLs
# ------------------------------------------------------------------------------
# NOTE: `BACKEND_URL_BASE` should not end with a "/"
BACKEND_URL_BASE = env("BACKEND_URL_BASE").rstrip("/")
assert BACKEND_URL_BASE.startswith("http"), "Must start with http(s)"

BACKEND_SITE_DOMAIN = urlparse(BACKEND_URL_BASE).hostname
assert BACKEND_SITE_DOMAIN, "Should be present."

# NOTE: `FRONTEND_URL_BASE` should not end with a "/"
FRONTEND_URL_BASE = env("FRONTEND_URL_BASE").rstrip("/")
assert FRONTEND_URL_BASE.startswith("http"), "Must start with http(s)"

# Allowed Hosts
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS", default=[BACKEND_SITE_DOMAIN, "127.0.0.1", "localhost"]
)

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

# django-rest-framework
# -------------------------------------------------------------------------------
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "EXCEPTION_HANDLER": "jaspr.apps.common.functions.custom_drf_exception_handler",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "JSON_UNDERSCOREIZE": {"no_underscore_before_number": True},
    "DATE_INPUT_FORMATS": ["iso-8601", "%m/%d/%Y", "%m/%d/%y"],
}

# CORS
# ------------------------------------------------------------------------------
REGEX_ESCAPE_CHARS = (
    ("-", "\-"),
    (".", "\\."),
    ("*", "[a-zA-Z0-9\-]+"),
)


def convert_static_url_to_regex(url):
    for replacement in REGEX_ESCAPE_CHARS:
        url = url.replace(replacement[0], replacement[1])
    return f"^{url}$"


# CORS WHITELIST CREATION
corw = []
corw.append(convert_static_url_to_regex(FRONTEND_URL_BASE))
if ENVIRONMENT == "production":
    corw.append(f"^https://epic.jasprhealth.com$")
elif ENVIRONMENT == "integration":
    corw.append(f"^https://epic.jaspr-integration.com$")

CORS_ORIGIN_REGEX_WHITELIST = corw
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["Has-Validation-Error", "Content-Disposition"]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "cache-control",
    "content-type",
    "dnt",
    "if-modified-since",
    "keep-alive",
    "origin",
    "user-agent",
    "x-mx-reqtoken",
    "x-csrftoken",
    "x-requested-with",
    "heartbeat",
]

# Security
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=False)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)  # 1 year
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)

#  add_header X-Frame-Options "SAMEORIGIN" always;
# X_FRAME_OPTIONS = "SAMEORIGIN"

# https://docs.djangoproject.com/en/3.0/ref/settings/#secure-browser-xss-filter
#     add_header X-Xss-Protection "1; mode=block" always;
SECURE_BROWSER_XSS_FILTER = True

# https://docs.djangoproject.com/en/3.0/ref/settings/#secure-referrer-policy
#    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

FEATURE_POLICY = {
    "accelerometer": "none",
    "ambient-light-sensor": "none",
    "autoplay": "none",
    "camera": "none",
    "encrypted-media": "none",
    "focus-without-user-activation": "none",
    "fullscreen": "none",
    "geolocation": "none",
    "gyroscope": "none",
    "magnetometer": "none",
    "microphone": "none",
    "midi": "none",
    "payment": "none",
    "picture-in-picture": "none",
    "usb": "none",
}
# Content-Security-Policy -- needs to be set after storages mixin

# Groups
# ------------------------------------------------------------------------------
TECHNICIAN_GROUP_NAME = "Technician"
PATIENT_GROUP_NAME = "Patient"

# Taggit
# ------------------------------------------------------------------------------
TAGGIT_CASE_INSENSITIVE = True

# Phone Numbers
# ------------------------------------------------------------------------------
PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_REGION = "US"

# Twilio
# ------------------------------------------------------------------------------
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_VERIFY_SID = env("TWILIO_VERIFY_SID")
TWILIO_PHONE_NUMBER = env("TWILIO_PHONE_NUMBER")

# Knox
# ------------------------------------------------------------------------------
REST_KNOX = {
    # NOTE: We never actually should be using this value, but we set it to this default
    # in order to be safe in the very small chance we actually missed setting it
    # somewhere, or something else happens, etc.
    "TOKEN_TTL": timedelta(minutes=10),
    "TOKEN_LIMIT_PER_USER": None,
    # Allow automatic token refresh (for Jaspr, since that's where we're using Knox
    # right now).
    "AUTO_REFRESH": True,
    # Only refresh the token if more than 30 seconds have passed (by default).
    # NOTE: At the time of writing, with the
    # `jaspr.apps.kiosk.authentication.JasprTokenAuthentication` class we're using,
    # we're not actually relying on this value. Setting in anyway though in case
    # something changes in the future and to have sensible/reasonable knox defaults
    # anyway. See the NOTE above `TOKEN_TTL` above. It's the same reasoning.
    "MIN_REFRESH_INTERVAL": 30,
}

# Jaspr Session Knox Integration (With Our Modifications)
# ------------------------------------------------------------------------------
IN_ER_TECHNICIAN_DEFAULT_TOKEN_EXPIRES_AFTER = timedelta(minutes=10)
IN_ER_PATIENT_DEFAULT_TOKEN_EXPIRES_AFTER = timedelta(hours=1)
AT_HOME_PATIENT_DEFAULT_TOKEN_EXPIRES_AFTER = timedelta(hours=24)
AT_HOME_PATIENT_LONG_LIVED_TOKEN_EXPIRES_AFTER = timedelta(days=30)

IN_ER_TECHNICIAN_DEFAULT_TOKEN_MIN_REFRESH_INTERVAL_SECONDS = 5  # 5 seconds
IN_ER_PATIENT_DEFAULT_TOKEN_MIN_REFRESH_INTERVAL_SECONDS = 30  # 30 seconds
AT_HOME_PATIENT_DEFAULT_TOKEN_MIN_REFRESH_INTERVAL_SECONDS = 180  # 3 minutes
AT_HOME_PATIENT_LONG_LIVED_TOKEN_MIN_REFRESH_INTERVAL_SECONDS = 3600  # 1 hour

# djfernet (previously django-fernet-fields)
# https://github.com/yourlabs/djfernet
# https://github.com/orcasgit/django-fernet-fields/issues/28#issuecomment-1035941383
# ------------------------------------------------------------------------------
FERNET_KEYS = env("FERNET_KEYS", cast=list)
# We will provide our own 32-bit url-safe base64 encoded secret keys generated using
# `cryptography.Fernet.generate_key()`. They are retrieved from the environment above
# assuming a comma separated list in the environment key if there is more than one.
FERNET_USE_HKDF = False

# AWS
# ------------------------------------------------------------------------------
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_TRANSCODE_PIPELINE_ID = env("AWS_TRANSCODE_PIPELINE_ID")

# Sentry
# ------------------------------------------------------------------------------
USE_SENTRY = env.bool("USE_SENTRY", default=True)
# Exposes an endpoint that explicitly throws an error, which can be helpful for testing
# Sentry. Disabled by default.
ALLOW_SENTRY_TEST = env.bool("ALLOW_SENTRY_TEST", default=False)

# EPIC
# ------------------------------------------------------------------------------
EPIC_CLIENT_ID = env("EPIC_CLIENT_ID")
EPIC_BACKEND_CLIENT_ID = env("EPIC_BACKEND_CLIENT_ID")

env_jaspr_private_key = env("EPIC_PRIVATE_KEY")
if env_jaspr_private_key.find("BEGIN") == -1 and env_jaspr_private_key.find("KEY") == -1:
    env_jaspr_private_key = base64.standard_b64decode(env_jaspr_private_key).decode("utf-8")

JASPR_PRIVATE_KEY = serialization.load_pem_private_key(
  bytes(env_jaspr_private_key, 'utf-8'),
  password=None,
)
JASPR_PUBLIC_KEY = JASPR_PRIVATE_KEY.public_key()

# Deprecated URLs
# ------------------------------------------------------------------------------
# Enable the toggling on/off of if deprecated URLs are included or not. Currently
# present for testing things on feature branches and/or release branch and making sure
# new URLs are being used and not old/deprecated ones.
INCLUDE_DEPRECATED_URLS = env.bool("INCLUDE_DEPRECATED_URLS", default=True)

# Freshdesk
# ------------------------------------------------------------------------------
# This is set to the base url for our fresh desk instance.
# e.g. https://jasprhealth.freshdesk.com/
FRESHDESK_SUPPORT_URL = env.str("FRESHDESK_SUPPORT_URL")
# This is set to the JWT SSO login URL for the freshdesk instance
# Only the account owner on Freshdesk can get this value
FRESHDESK_SSO_REDIRECT_URL = env.str("FRESHDESK_SSO_REDIRECT_URL")

