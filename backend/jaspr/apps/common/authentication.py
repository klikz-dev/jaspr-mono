from typing import Tuple

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.validators import ValidationError
from django.utils.http import urlsafe_base64_decode
from jaspr.apps.accounts.models import User
from rest_framework import authentication, serializers
from rest_framework.request import Request


class UidAndTokenAuthentication(authentication.BaseAuthentication):
    """
    Authentication scheme that authenticates based on provided
    `uid` and `token` in the request's `kwargs`. Assumes `uid`
    is base 64 encoded, and that `token_generator` is an instance
    of `PasswordResetTokenGenerator`. Will use `token_generator().check_token(...)`
    to check for a valid token, and authenticate to the `User` corresponding
    to the `uid` if so.

    NOTE: At the time of writing, all errors raise a `serializers.ValidationError`,
    which results in a 400 status code. This currently makes it easier potentially
    for the frontend to display the invalid link error message if desired.
    """

    token_generator: PasswordResetTokenGenerator = PasswordResetTokenGenerator

    error_messages = {
        "no_uid": "A User ID is required.",
        "no_token": "A token is required.",
        "invalid": (
            "The link is invalid. Please get a new link sent to you or "
            "contact support. Be aware that links currently expire after "
            f"{int(settings.PASSWORD_RESET_TIMEOUT / 3600 / 24)} days."
        ),
    }

    @classmethod
    def fail(cls, error_key: str) -> None:
        raise serializers.ValidationError(cls.error_messages[error_key])

    def get_token(self, request: Request) -> str:
        token = request.data.get("token")
        if token is None:
            self.fail("no_token")
        return token

    @classmethod
    def user_from_b64_encoded_id(cls, uidb64: str) -> User:
        """Thanks to: https://github.com/django/django/blob/aeb8c381789ad93866223f8bd07d09ae5e2edd9e/django/contrib/auth/views.py#L284"""
        try:
            # `urlsafe_base64_decode` decodes to bytestring.
            uid = urlsafe_base64_decode(uidb64)
            return User._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            cls.fail("invalid")

    def get_user(self, request: Request) -> User:
        uidb64 = request.data.get("uid")
        if uidb64 is None:
            self.fail("no_uid")
        return self.user_from_b64_encoded_id(uidb64)

    def authenticate(self, request: Request) -> Tuple[User, None]:
        token = self.get_token(request)
        user = self.get_user(request)
        if not self.token_generator().check_token(user, token):
            self.fail("invalid")
        return (user, None)
