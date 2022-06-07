"""
Settings mixin for Django for storing static + media files (currently with whitenoise
+ django-storages).

Intended to be used for:
- Production and integration
- Feature branch development
- Local development

Not intended to be used for:
- CI testing
- Local testing

Ordering/Derivation Chart:
- root --> base --> storages_mixin
"""
from .base import *  # isort:skip  # noqa

# Storages
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ["storages"]  # noqa F405
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"
}
#  https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_DEFAULT_ACL = None
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME", default="us-west-2")
# NOTE: Added in for now because of EBPI-829 and
# (https://github.com/jschneier/django-storages/issues/692#issuecomment-538914619).
# Will definitely be needed regardless once we switch to putting everything behind
# # cloudfront.
CDN_DOMAIN = env("CDN_DOMAIN")
AWS_S3_CUSTOM_DOMAIN = CDN_DOMAIN#  f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Static
# ------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "jaspr.apps.common.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
