import random
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from freezegun import freeze_time
from knox.models import AuthToken
from rest_framework import status

from jaspr.apps.api.v1.serializers import MeTechnicianSerializer
from jaspr.apps.kiosk.authentication import JasprTokenAuthentication
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestTechnicianLoginAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/technician/login"
        self.now = timezone.now()

    def setup_technician(self, **kwargs):
        technician = self.create_technician(**kwargs)
        self.user = technician.user
        self.data = {
            "email": self.user.email,
            "password": "password",
            "organization_code": technician.system.organization_code,
        }

    def login(self, time=None, data_overrides=None, **request_kwargs):
        with freeze_time(time or self.now):
            return self.client.post(
                self.uri,
                data={**getattr(self, "data", {}), **(data_overrides or {})},
                **request_kwargs,
            )

    def assert_valid_token_and_response(
        self, token, response, time=None, **request_kwargs
    ):
        self.assertEqual(token.created, time or self.now)
        timediff = settings.IN_ER_TECHNICIAN_DEFAULT_TOKEN_EXPIRES_AFTER
        self.assertEqual(token.expiry, (time or self.now) + timediff)
        # Sanity check on the token length.
        token_string = response.data["token"]
        self.assertGreater(len(token_string), 20)
        self.assertEqual(parse_datetime(response.data["expiry"]), token.expiry)
        self.assertTrue(response.data["session"]["in_er"])
        self.assertFalse(response.data["session"]["from_native"])
        self.assertFalse(response.data["session"]["long_lived"])
        response.data["technician"].pop("support_url")
        me_tech_data = MeTechnicianSerializer(self.user.technician).data
        me_tech_data.pop("support_url")
        self.assertEqual(
            response.data["technician"],
            me_tech_data,
        )

        # Now make sure setting the token string as the authorization works on a
        # protected endpoint, which helps validate that `token_string` is the correctly
        # returned value.
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_string}")
        me_response = self.client.get("/v1/me", **request_kwargs)
        me_response.data.pop("support_url")
        # If this has a successful status code, we know we have authentiated correctly,
        # and the token we used is valid.
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        # Extra check to make sure that the "technician" data is the exact same as the
        # '/me/' endpoint response data.
        self.assertEqual(response.data["technician"], me_response.data)

    def test_login_by_technician_from_web_app_without_existing_token(self):
        """
        Can a `Technician` without existing token log in and create a token from the
        web app?
        """
        self.setup_technician()
        response = self.login()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = AuthToken.objects.get(user=self.user)
        self.assert_valid_token_and_response(token, response)

    def test_login_by_technician_with_multiple_non_expired_tokens_already_present(self):
        """
        Test that logging in with multiple non-expired tokens already present in the
        database creates a new token and returns it (meaning we have multiple token
        support).
        """
        self.setup_technician()
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

    def test_login_by_technician_and_next_request_with_expired_token_in_database(self):
        """
        Test that logging in with an expired token already present in the database
        creates a new token, resulting in a total of two tokens present. Then, make a
        request to an endpoint that uses `JasprTokenAuthentication`, and verify that
        the expired token is removed form the database.
        """
        self.setup_technician()
        now = timezone.now()
        eight_days_ago = now - timedelta(days=8)
        first_response = self.login(time=eight_days_ago)
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

    def test_technician_cannot_currently_manually_specify_from_native_or_long_lived(
        self,
    ):
        """
        Do `from_native` and `long_lived` always show up as `False`, regardless of
        what is specified?
        """
        self.setup_technician()
        response = self.login(data_overrides={"from_native": True, "long_lived": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = AuthToken.objects.get(user=self.user)
        self.assertFalse(token.jaspr_session.from_native)
        self.assertFalse(token.jaspr_session.long_lived)
        self.assert_valid_token_and_response(token, response)

    def test_login_with_wrong_password(self):
        """
        Tests that logging in with the wrong password returns the proper response and
        does not generate a token.

        NOTE: At the time of writing, `test_technician_login_workflow.py` has a lot
        of tests that handle cases like this so just doing a simple case here for
        now.
        """
        self.setup_technician()
        response = self.login(data_overrides={"password": "wrong_password"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "Credentials invalid.")
        self.assertIsNone(AuthToken.objects.first())

    def test_login_not_permitted_if_ip_not_satisfied(self):
        system, clinic, department = self.create_full_healthcare_system(
            name="Login IP Test System",
            clinic_kwargs={"name":"Whitelist Clinic", "ip_addresses_whitelist": ["123.231.124.241"]},
        )
        technician = self.create_technician(
            system=system, department=department
        )
        self.user = technician.user
        self.data = {
            "email": self.user.email,
            "password": "password",
            "organization_code": technician.system.organization_code,
        }
        response = self.login(REMOTE_ADDR="193.123.234.122")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            ["You are not permitted to login from this location."],
        )

    def test_login_permitted_if_ip_satisfied(self):
        system, clinic, department = self.create_full_healthcare_system(
            name="Login IP Test System",
            clinic_kwargs={"ip_addresses_whitelist": ["123.231.124.241"]},
        )
        technician = self.create_technician(
            system=system, department=department
        )
        self.user = technician.user
        self.data = {
            "email": self.user.email,
            "password": "password",
            "organization_code": technician.system.organization_code,
        }
        response = self.login(REMOTE_ADDR="123.231.124.241")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = AuthToken.objects.get()
        self.assert_valid_token_and_response(
            token, response, REMOTE_ADDR="123.231.124.241"
        )

    def test_login_with_patient_forbidden(self):
        """Test that logging in with a `Patient` is forbidden."""
        patient = self.create_patient(user__password="random_password")
        response = self.login(
            data_overrides={
                "email": patient.user.email,
                "password": "random_password",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_login_with_user_with_group_but_without_associated_instance(self):
        """
        Even if a `User` has the "Technician" group, is the `User` still prevented
        from logging in if no associated `technician` reverse one-to-one instance is
        found on the `User`?
        """
        user = self.create_underlying_user(settings.TECHNICIAN_GROUP_NAME)
        response = self.login(
            data_overrides={"email": user.email, "password": "password"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
