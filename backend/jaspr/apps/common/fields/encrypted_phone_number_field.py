from fernet_fields import EncryptedField
from phonenumber_field.modelfields import PhoneNumberField


class EncryptedPhoneNumberField(EncryptedField, PhoneNumberField):
    pass
