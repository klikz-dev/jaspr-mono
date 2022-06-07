from django.db import models
from fernet_fields import EncryptedField


class EncryptedPositiveSmallIntegerField(
    EncryptedField, models.PositiveSmallIntegerField
):
    pass
