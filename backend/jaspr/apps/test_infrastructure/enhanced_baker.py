"""
`enhanced_baker.py` provides an importable baker with the ability
to handle some of the custom fields in this project. Extra fields
here can be added/removed as necessary.
"""
import random

from django.contrib.postgres.fields import ArrayField
from django.db.models import FileField, JSONField
from django.db.models.fields import BooleanField, CharField, DateTimeField, TextField
from fernet_fields import EncryptedCharField, EncryptedDateTimeField, EncryptedTextField
from model_bakery import baker
from model_bakery.generators import default_mapping

from jaspr.apps.awsmedia.fields import PrimaryFileField
from jaspr.apps.common.fields import (
    EncryptedArrayField,
    EncryptedBooleanField,
    EncryptedJSONField,
    EncryptedPhoneNumberField,
)


def generate_phone_number() -> str:
    """
    Generate a valid looking phone number.
    (example numbers taken from Twilio: https://www.twilio.com/docs/glossary/what-e164)
    """
    # NOTE: These numbers are in the E.164 format.
    return random.choice(["+14155552671", "+442071838750", "+551155256325"])


baker.generators.add(EncryptedCharField, default_mapping[CharField])
baker.generators.add(EncryptedDateTimeField, default_mapping[DateTimeField])
baker.generators.add(EncryptedTextField, default_mapping[TextField])
baker.generators.add(EncryptedBooleanField, default_mapping[BooleanField])
baker.generators.add(EncryptedArrayField, default_mapping[ArrayField])
baker.generators.add(EncryptedJSONField, default_mapping[JSONField])
baker.generators.add(PrimaryFileField, default_mapping[FileField])
# NOTE: If `unique=True` is ever needed for a phone number, will probably have to take
# a different approach here, or make sure in tests that a unique phone number is passed
# in. Currently it is never the case that `unique=True` is needed, so we're fine for
# now.
baker.generators.add(EncryptedPhoneNumberField, generate_phone_number)
