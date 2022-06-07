import django
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class JasprExtraSecurityTokenGenerator(PasswordResetTokenGenerator):
    key_salt: str = "jaspr.apps.kiosk.tokens.JasprExtraSecurityTokenGenerator"
    security_string_start: int = 0
    security_string_end: int = 25

    # !INSPECT_WHEN_UPGRADING_DJANGO!
    def _make_hash_value(self, user, timestamp):
        """
        # !INSPECT_WHEN_UPGRADING_DJANGO!
        # SEE EBPI-888
        """
        assert django.VERSION[0] <= 4
        if django.VERSION[0] == 4:
            assert django.VERSION[1] < 1
        assert (
            user.pk is not None
        ), "`User` should have primary key (and have been saved) at this point."
        security_string = user.current_security_chars[
            self.security_string_start: self.security_string_end
        ]
        assert isinstance(security_string, str) and len(security_string) == 25
        return security_string + str(user.pk) + user.password + str(timestamp)


class JasprToolsToGoSetupTokenGenerator(JasprExtraSecurityTokenGenerator):
    key_salt = "jaspr.apps.kiosk.tokens.JasprToolsToGoSetupTokenGenerator"
    security_string_start: int = 25
    security_string_end: int = 50


class JasprPasswordResetTokenGenerator(JasprExtraSecurityTokenGenerator):
    key_salt = "jaspr.apps.kiosk.tokens.JasprPasswordResetTokenGenerator"
    security_string_start: int = 50
    security_string_end: int = 75


class JasprSetPasswordTokenGenerator(JasprExtraSecurityTokenGenerator):
    key_salt = "jaspr.apps.kiosk.tokens.JasprSetPasswordTokenGenerator"
    security_string_start: int = 75
    security_string_end: int = 100
