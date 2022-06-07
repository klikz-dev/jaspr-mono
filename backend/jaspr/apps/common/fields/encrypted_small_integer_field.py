from django.db import models
from fernet_fields import EncryptedField


class EncryptedSmallIntegerField(EncryptedField, models.SmallIntegerField):
    pass
