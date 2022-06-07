from datetime import datetime, timedelta
from typing import Optional, Tuple, Type

import django
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from freezegun import freeze_time
from rest_framework.response import Response

from jaspr.apps.accounts.models import User
from jaspr.apps.common.authentication import UidAndTokenAuthentication

TokenGeneratorType = Type[PasswordResetTokenGenerator]


class UidAndTokenTestMixin:
    token_generator: TokenGeneratorType

    @staticmethod
    def uidb64_for(user: User) -> str:
        return urlsafe_base64_encode(force_bytes(user.pk))

    @staticmethod
    def invalid_uidb64_for(user: User) -> str:
        # NOTE: 10001 was chosen because it's both a large number that is unlikely to
        # even be a `User` ID given we're using Postgres (and it doesn't even really
        # matter if it's an valid `User` ID, since it's invalid for the given `user`
        # which is all we want) and also because it looks cool and is a palindrome.
        return urlsafe_base64_encode(force_bytes(user.pk + 10001))

    def valid_token_for(
        self, user: User, token_generator: TokenGeneratorType = None
    ) -> str:
        generator = token_generator or self.token_generator
        return generator().make_token(user)

    def invalid_token_for(
        self, user: User, token_generator: TokenGeneratorType = None
    ) -> str:
        token = self.valid_token_for(user, token_generator)
        return token[:-1] + ("1" if token[-1] == "0" else "0")

    def expired_token_for(
        self,
        user: User,
        time: Optional[datetime] = None,
        token_generator: TokenGeneratorType = None,
    ) -> str:
        time = time or timezone.now()
        days = settings.PASSWORD_RESET_TIMEOUT / 3600 / 24
        # NOTE: Due to how Django's internal mechanisms function for checking the
        # token, we say `days=days + 2` to be certain that it has expired.
        with freeze_time(time - timedelta(days=days + 2, minutes=1)):
            return self.valid_token_for(user, token_generator)

    def uidb64_and_token(
        self, user: User, token_generator: TokenGeneratorType = None
    ) -> Tuple[str, str]:
        uidb64 = self.uidb64_for(user)
        token = self.valid_token_for(user, token_generator)
        return uidb64, token

    def post_with_creds(
        self,
        uri: str,
        user: User,
        data: dict,
        token_generator: TokenGeneratorType = None,
    ) -> Response:
        uidb64, token = self.uidb64_and_token(user, token_generator)
        data = {"uid": uidb64, "token": token, **data}

        return self.client.post(uri, data=data)
