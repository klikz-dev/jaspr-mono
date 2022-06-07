from django.db import models
from fernet_fields import EncryptedField


class EncryptedBooleanField(EncryptedField, models.BooleanField):
    pass
