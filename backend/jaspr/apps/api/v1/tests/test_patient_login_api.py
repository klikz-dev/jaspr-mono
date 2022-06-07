import random
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from freezegun import freeze_time
from jaspr.apps.api.v1.serializers import MePatientSerializer
from jaspr.apps.kiosk.authentication import JasprTokenAuthentication
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from knox.models import AuthToken
from rest_framework import status

from .helpers import assert_patient_logged_in, patient_before_login_setup_kwargs


class TestPatientLoginAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/patient/login"
        self.now = timezone.now()

    def setup_patient(self, **kwargs):
        self.user = self.create_patient(**kwargs).user
        self.data = {
            "email": self.user.email,
            "password": "password",
        }

    def login(self, time=None, long_lived=True, data_overrides=None):
        with freeze_time(time or self.now):
            return self.client.post(
                self.uri,
                data={
                    **getattr(self, "data", {}),
                    "long_lived": long_lived,
                    **(data_overrides or {}),
                },
            )

    def assert_valid_token_and_response(
        self, token, response, time=None, long_lived=True
    ):
        self.assertEqual(token.created, time or self.now)
        if long_lived:
            timediff = settings.AT_HOME_PATIENT_LONG_LIVED_TOKEN_EXPIRES_AFTER
        else:
            timediff = settings.AT_HOME_PATIENT_DEFAULT_TOKEN_EXPIRES_AFTER
        self.assertEqual(token.expiry, (time or self.now) + timediff)
        # Sanity check on the token length.
        token_string = response.data["token"]
        self.assertGreater(len(token_string), 20)
        self.assertEqual(parse_datetime(response.data["expiry"]), token.expiry)
        self.assertFalse(response.data["session"]["in_er"])
        self.assertTrue(response.data["session"]["from_native"])
        self.assertIs(response.data["session"]["long_lived"], long_lived)
        self.assertEqual(
            response.data["patient"],
            # TODO: Remove `in_er` from context once `in_er` is removed from the
            # `MePatientSerializer`.
            MePatientSerializer(
                self.user.patient, context={"in_er": response.data["session"]["in_er"]},
            ).data,
        )

        # Now make sure setting the token string as the authorization works on a
        # protected endpoint, which helps validate that `token_string` is the correctly
        # returned value.
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_string}")
        me_response = self.client.get("/v1/me")
        # If this has a successful status code, we know we have authentiated correctly,
        # and the token we used is valid.
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        # Extra check to make sure that the "patient" data is the exact same as the
        # '/me/' endpoint response data.
        self.assertEqual(response.data["patient"], me_response.data)

    def test_patient_login_all_records_created_and_fields_updated(self):
        """
        Test that if a `Patient` logs in, all the different records that should be
        created are created and that specific fields on the `Patient` are reset.
        """
        self.setup_patient(**patient_before_login_setup_kwargs())
        response = self.login()

        self.user.patient.refresh_from_db()
        assert_patient_logged_in(
            self, self.user.patient, False, self.now, from_native=True
        )

    def test_login_from_native_without_long_lived(self):
        """
        If a `Patient` logs in with `from_native` set to `True` without `long_lived`
        set to `True`, does everything work as intended (I.E. the correct session
        data being set and expiry set on the token, etc.)?
        """
        self.setup_patient()
        response = self.login(long_lived=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = AuthToken.objects.get(user=self.user)
        self.assert_valid_token_and_response(token, response, long_lived=False)

    def test_login_from_native_with_long_lived(self):
        """
        If a `Patient` logs in with `from_native` set to `True` with `long_lived`
        also set to `True`, does everything work as intended (I.E. the correct
        session data being set and expiry set on the token, etc.)?
        """
        self.setup_patient()
        response = self.login(long_lived=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = AuthToken.objects.get(user=self.user)
        self.assert_valid_token_and_response(token, response, long_lived=True)

    def test_patient_cannot_currently_manually_specify_from_native(self):
        """
        Does `from_native` always show up as `True`, regardless of what is specified?
        """
        self.setup_patient()
        response = self.login(data_overrides={"from_native": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = AuthToken.objects.get(user=self.user)
        self.assertTrue(token.jaspr_session.from_native)
        self.assert_valid_token_and_response(token, response)

    def test_login_by_patient_from_native_app_without_existing_token(self):
        """
        Can a `Patient` without existing token log in from native_app and get a
        token?
        """
        self.setup_patient()
        response = self.login()
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        token = AuthToken.objects.get(user=self.user)
        self.assert_valid_token_and_response(token, response)

    def test_login_by_patient_with_multiple_non_expired_tokens_already_present(self):
        """
        Test that logging in with multiple non-expired tokens already present in the
        database creates a new token and returns it (meaning we have multiple token
        support).
        """
        self.setup_patient()
        now = timezone.now()
        one_second_ago = now - timedelta(seconds=1)
        two_seconds_ago = now - timedelta(seconds=2)
        first_response = self.login(time=two_seconds_ago)
        second_response = self.login(time=one_second_ago)
        third_response = self.login(time=now)
        tokens = list(AuthToken.objects.filter(user=self.user).order_by("-created"))
        self.assertEqual(len(tokens), 3)
        token_string = third_response.data["token"]
        # Now check that the token successfully authenticates.
        authentication = JasprTokenAuthentication()
        (
            authenticated_user,
            authenticated_token,
        ) = authentication.authenticate_credentials(token_string.encode())
        self.assertEqual(authenticated_user, self.user)
        self.assertEqual(authenticated_token, tokens[0])
        self.assert_valid_token_and_response(tokens[0], third_response, time=now)

    def test_login_by_patient_and_next_request_with_expired_token_in_database(self):
        """
        Test that logging in with an expired token already present in the database
        creates a new token, resulting in a total of two tokens present. Then, make a
        request to an endpoint that uses `JasprTokenAuthentication`, and verify that
        the expired token is removed from the database.
        """
        self.setup_patient()
        now = timezone.now()
        # If a `long_lived=True` (the current default) token is not used for `40` days,
        # it should be expired.
        forty_one_days_ago = now - timedelta(days=41)
        first_response = self.login(time=forty_one_days_ago)
        self.assertEqual(AuthToken.objects.filter(user=self.user).count(), 1)
        second_response = self.login(time=now)
        tokens = list(AuthToken.objects.filter(user=self.user).order_by("-created"))
        self.assertEqual(len(tokens), 2)
        token_string = second_response.data["token"]
        # Now check that the token successfully authenticates.
        authentication = JasprTokenAuthentication()
        (
            authenticated_user,
            authenticated_token,
        ) = authentication.authenticate_credentials(token_string.encode())
        self.assertEqual(authenticated_user, self.user)
        self.assertEqual(authenticated_token, tokens[0])
        self.assert_valid_token_and_response(tokens[0], second_response, time=now)
        token_that_should_still_be_present = tokens[0]
        # NOTE: `assert_valid_token_and_response` above makes a request to '/me' and
        # verifies it succeeds. That should delete the expired token. Let's check.
        latest_tokens = list(AuthToken.objects.filter(user=self.user))
        self.assertEqual(len(latest_tokens), 1)
        self.assertEqual(latest_tokens[0], token_that_should_still_be_present)

    def test_login_with_wrong_password(self):
        """
        Tests that logging in with the wrong password returns the proper response and
        does not generate a token.

        NOTE: At the time of writing, `test_technician_login_workflow.py` has a lot
        of tests that handle cases like this so just doing a simple case here for
        now.
        """
        self.setup_patient()
        response = self.login(data_overrides={"password": "wrong_password"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "Credentials invalid.")
        self.assertIsNone(AuthToken.objects.first())

    def test_login_with_technician_forbidden(self):
        """Test that logging in with a `Technician` is forbidden."""
        technician = self.create_technician(user__password="random_password")
        response = self.login(
            data_overrides={
                "email": technician.user.email,
                "password": "random_password",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_login_with_user_with_group_but_without_associated_instance(self):
        """
        Even if a `User` has the "Patient" group, is the `User` still prevented from
        logging in if no associated `patient` reverse one-to-one instance is found on
        the `User`?
        """
        user = self.create_underlying_user(settings.PATIENT_GROUP_NAME)
        response = self.login(
            data_overrides={"email": user.email, "password": "password"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
