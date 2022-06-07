import json
from django.contrib.postgres.fields import ArrayField
from fernet_fields import EncryptedField


class EncryptedArrayField(EncryptedField, ArrayField):

    def db_type(self, connection):
        # NOTE: Don't call `super()`, we want to ignore the `ArrayField` inheritance
        # and explicitly use the `db_type` from `EncryptedField`, not taking
        # `ArrayField` into account.
        return EncryptedField.db_type(self, connection)

    def get_db_prep_value(self, value, connection, prepared=False):
        # NOTE: `EncryptedField` does not define `get_db_prep_value`, so it's only
        # assumed right now that we're dealing with `ArrayField`.
        prepped = super().get_db_prep_value(value, connection, prepared=prepared)
        if isinstance(prepped, list):
            # NOTE: Due to this line, if the db-prepped value for the base field for
            # the `ArrayField` is not serializable to a string by `json.dumps`, then it
            # won't be supported at this time for `EncryptedArrayField`. However, it
            # seems like db-prepped values for most/all standard base fields would be
            # supported by `json.dumps` at this time.
            return json.dumps(prepped)
        return prepped

