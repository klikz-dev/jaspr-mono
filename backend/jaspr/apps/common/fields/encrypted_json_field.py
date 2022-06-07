import json

from django.db.models import JSONField
from fernet_fields import EncryptedField


class EncryptedJSONField(EncryptedField, JSONField):
    def db_type(self, connection):
        # NOTE: Don't call `super()`, we want to ignore the `JSONField` inheritance and
        # explicitly use the `db_type` from `EncryptedField`, not taking `JSONField`
        # into account.
        return EncryptedField.db_type(self, connection)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return value
        return json.dumps(value)

    def from_db_value(self, value, expression, connection):
        value = super().from_db_value(value, expression, connection)
        if value is None:
            return value
        return json.loads(value)
