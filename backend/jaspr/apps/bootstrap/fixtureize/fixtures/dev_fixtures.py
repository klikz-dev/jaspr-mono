from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice

from jaspr.apps.accounts.models import User

from ..base import ModelFixture
from ..tags import Tags


class DevSuperuserFixture(ModelFixture):
    model = User
    tags = {Tags.USER, Tags.DEV}

    # NOTE: We assume right now that the dev superuser's device has a primary key of
    # `1`.
    pks = "1"

    @classmethod
    def get_key(cls) -> str:
        return f"{super().get_key()}::dev-superuser"


class DevSuperuserTOTPDeviceFixture(ModelFixture):
    model = TOTPDevice
    tags = {Tags.USER, Tags.DEV, Tags.THIRD_PARTY}

    # NOTE: We assume right now that the dev superuser's device has a primary key of
    # `1` (and that the dev superuser above also has a primary key of `1`).
    pks = "1"

    @classmethod
    def get_key(cls) -> str:
        return f"{super().get_key()}::dev-superuser-totp-device"


class DevSuperuserStaticDeviceFixture(ModelFixture):
    model = StaticDevice
    tags = {Tags.USER, Tags.DEV, Tags.THIRD_PARTY}

    # NOTE: We assume right now that the dev superuser's static device has a primary
    # key of `1` (and that the dev superuser above also has a primary key of `1`).
    pks = "1"

    @classmethod
    def get_key(cls) -> str:
        return f"{super().get_key()}::dev-superuser-static-device"


class DevSuperuserStaticTokenFixture(ModelFixture):
    model = StaticToken
    tags = {Tags.USER, Tags.DEV, Tags.THIRD_PARTY}

    # NOTE: We assume right now that the dev superuser's static token has a primary key
    # of `1` (and that the dev superuser above also has a primary key of `1`).
    pks = "1"

    @classmethod
    def get_key(cls) -> str:
        return f"{super().get_key()}::dev-superuser-static-token"
