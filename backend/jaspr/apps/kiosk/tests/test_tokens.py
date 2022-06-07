from datetime import timedelta

from django.conf import settings
from django.test import SimpleTestCase
from django.utils import timezone
from freezegun import freeze_time
from jaspr.apps.accounts.security import generate_multiple_unique_secure_random_strings
from jaspr.apps.kiosk.models import Patient
from jaspr.apps.kiosk.tokens import (
    JasprExtraSecurityTokenGenerator,
    JasprPasswordResetTokenGenerator,
    JasprSetPasswordTokenGenerator,
    JasprToolsToGoSetupTokenGenerator,
)
from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestPasswordResetTokenExpirationDays(SimpleTestCase):
    def test_password_reset_timeout(self):
        self.assertEqual(settings.PASSWORD_RESET_TIMEOUT, 15 * 3600 * 24)


class JasprTokenGenerationTestMixin:
    # NOTE: Subclasses should provide this.
    token_generator: JasprExtraSecurityTokenGenerator

    @classmethod
    def make_token(cls, patient: Patient) -> str:
        return cls.token_generator().make_token(patient.user)

    def _test_token_generation(self, security_start: int, security_end: int) -> None:
        now = timezone.now()
        patient = self.create_patient()
        with freeze_time(now):
            first_token = self.make_token(patient)
            # Make sure once that we at least got something.
            self.assertTrue(bool(first_token))
            patient.user.date_joined = patient.user.date_joined - timedelta(seconds=1)
            patient.user.save()
            second_token = self.make_token(patient)
            # Check that the token is not dependent on `patient.user.date_joined`.
            self.assertEqual(first_token, second_token)
            patient.user.set_password("Goo00se785#$")
            patient.user.save()
            third_token = self.make_token(patient)
            # Check that the token is dependent on `patient.user.password`.
            self.assertNotEqual(second_token, third_token)
            last_login = patient.user.last_login
            patient.user.last_login = (
                now if last_login is None else last_login - timedelta(seconds=1)
            )
            patient.user.save()
            fourth_token = self.make_token(patient)
            # Check that the token is not dependent on `patient.user.last_login`.
            self.assertEqual(third_token, fourth_token)
            password_changed = patient.user.password_changed
            patient.user.password_changed = (
                now + timedelta(seconds=2)
                if password_changed is None
                else password_changed + timedelta(seconds=200)
            )
            patient.user.save()
            fifth_token = self.make_token(patient)
            # Check that the token is not dependent on `patient.user.password_changed`.
            self.assertEqual(fourth_token, fifth_token)
            start_index = self.token_generator.security_string_start
            end_index = self.token_generator.security_string_end
            new_security_string = generate_multiple_unique_secure_random_strings(1, 25)[
                0
            ]
            patient.user.current_security_chars = (
                patient.user.current_security_chars[0:start_index]
                + new_security_string
                + patient.user.current_security_chars[end_index:100]
            )
            patient.user.save()
            sixth_token = self.make_token(patient)
            # Check that the token is dependent on
            # `patient.user.current_security_chars` in its range.
            self.assertNotEqual(fifth_token, sixth_token)
        with freeze_time(now + timedelta(days=1, seconds=1)):
            seventh_token = self.make_token(patient)
            # Check that the token is dependent on time (Django 1.11 implementation
            # uses days, but Django 3.1+ implementation uses seconds, using `days=1`
            # and `seconds=1` should theoretically cover both).
            self.assertNotEqual(sixth_token, seventh_token)


class TestJasprExtraSecurityTokenGenerator(
    JasprTokenGenerationTestMixin, JasprTestCase
):
    token_generator = JasprExtraSecurityTokenGenerator

    def test_token_generation(self):
        self._test_token_generation(security_start=0, security_end=25)


class TestJasprToolsToGoSetupTokenGenerator(
    JasprTokenGenerationTestMixin, JasprTestCase
):
    token_generator = JasprToolsToGoSetupTokenGenerator

    def test_token_generation(self):
        self._test_token_generation(security_start=25, security_end=50)


class TestJasprPasswordResetTokenGenerator(
    JasprTokenGenerationTestMixin, JasprTestCase
):
    token_generator = JasprPasswordResetTokenGenerator

    def test_token_generation(self):
        self._test_token_generation(security_start=50, security_end=75)


class TestJasprPasswordResetTokenGenerator(
    JasprTokenGenerationTestMixin, JasprTestCase
):
    token_generator = JasprSetPasswordTokenGenerator

    def test_token_generation(self):
        self._test_token_generation(security_start=75, security_end=100)


class TestJasprTokensTogether(JasprTestCase):
    def test_token_generator_indices_and_unique_values_produced(self):
        base_class = JasprExtraSecurityTokenGenerator
        subclasses = JasprExtraSecurityTokenGenerator.__subclasses__()
        classes = [base_class] + subclasses
        self.assertEqual(len(classes), 4)
        salts = [klass.key_salt for klass in classes]
        start_and_ends = [
            (klass.security_string_start, klass.security_string_end)
            for klass in classes
        ]
        self.assertEqual(len(set(salts)), 4)
        self.assertEqual(len(set(start_and_ends)), 4)
        self.assertEqual(set(start_and_ends), {(0, 25), (25, 50), (50, 75), (75, 100)})

        user = self.create_user()
        now = timezone.now()
        hash_values = [klass()._make_hash_value(user, now) for klass in classes]
        # Make sure all of the generated values to hash are different, even if
        # theoretically run at the exact same time!
        self.assertEqual(len(set(hash_values)), len(hash_values))
