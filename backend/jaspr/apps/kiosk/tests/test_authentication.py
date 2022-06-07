from datetime import datetime, timedelta
from typing import Tuple
from unittest import SkipTest

from django.utils import timezone
from freezegun import freeze_time
from knox.models import AuthToken
from rest_framework import status
from rest_framework.response import Response

from jaspr.apps.accounts.models import User
from jaspr.apps.api.v1.views import (
    PatientCheckPhoneNumberCodeView,
    PatientResetPasswordCheckPhoneNumberCodeView,
)
from jaspr.apps.common.tests.mixins import UidAndTokenTestMixin
from jaspr.apps.kiosk.authentication import (
    JasprResetPasswordUidAndTokenAuthentication,
    JasprToolsToGoUidAndTokenAuthentication,
)
from jaspr.apps.kiosk.models import (
    Encounter,
    JasprSession,
    JasprUserTypeString,
    Patient,
)
from jaspr.apps.kiosk.tests.helpers import (
    JasprSessionParametrizationTestMixin,
    Parametrizer,
)
from jaspr.apps.test_infrastructure.mixins.common_mixins import (
    TwilioClientTestCaseMixin,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestJasprTokenAuthentication(
    JasprSessionParametrizationTestMixin, JasprApiTestCase
):
    def create_jaspr_session_overriding_checks(
        self,
        user: User,
        user_type: JasprUserTypeString,
        in_er: bool,
        from_native: bool,
        long_lived: bool,
        encounter: Encounter = None,
    ) -> Tuple[JasprSession, str]:
        # Use `timedelta(minutes=17)` for the expiry since that's not a value it would
        # be for any of the regular different `expiry` combinations.
        auth_token, token = AuthToken.objects.create(
            user=user, expiry=timedelta(minutes=17)
        )
        # NOTE: We use `JasprSession.objects.create` instead of `JasprSession.create`
        # because we want to intentionally bypass the validation logic and just create
        # a session that could potentially be invalid (allows us to create various
        # sessions, valid or invalid, and make sure that, for example, refresh logic
        # works properly in all those cases).
        jaspr_session = JasprSession.objects.create(
            user_type=user_type,
            in_er=in_er,
            from_native=from_native,
            long_lived=long_lived,
            auth_token=auth_token,
            encounter=encounter,
            technician_operated=False
        )
        return jaspr_session, token

    def set_token_and_get_me(self, token: str, time_to_freeze_at: datetime) -> Response:
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        with freeze_time(time_to_freeze_at):
            # The `/me/` endpoint is accessible by both `Technician`s and
            # `Patient`s and is protected by `JasprTokenAuthentication` so it's
            # suitable for checking the refresh mechanism in `JasprTokenAuthentication`
            # and other authentication logic.
            return self.client.get("/v1/me")

    def test_renew_token_technician_combinations(self):
        technician = self.create_technician()
        parametrizer = Parametrizer(
            self.jaspr_session_params_valid_value_mapping, self.technician_combinations
        )
        result = parametrizer.result
        now = timezone.now()
        for (
            in_er,
            from_native,
            long_lived,
        ) in parametrizer.all_mapping_parametrizations:
            with self.subTest(
                in_er=in_er, from_native=from_native, long_lived=long_lived
            ):
                create_session_at = timezone.now()
                with freeze_time(create_session_at):
                    session, token = self.create_jaspr_session_overriding_checks(
                        technician.user, "Technician", in_er, from_native, long_lived
                    )
                auth_token = session.auth_token
                # Make sure the token has the datetimes we expect before we
                # continue.
                self.assertEqual(auth_token.created, create_session_at)
                self.assertEqual(
                    auth_token.expiry, create_session_at + timedelta(minutes=17)
                )
                freeze_at = create_session_at + timedelta(seconds=301)
                response = self.set_token_and_get_me(token, freeze_at)
                expected = result[(in_er, from_native, long_lived)]
                if isinstance(expected[0], timedelta):
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                    session.refresh_from_db()
                    auth_token.refresh_from_db()
                    self.assertEqual(auth_token.created, create_session_at)
                    self.assertEqual(auth_token.expiry, freeze_at + expected[0])

                    # Make sure the minimum refresh interval seconds are honored (next
                    # two sections).

                    before_min_interval_freeze_at = (
                        freeze_at + expected[1] - timedelta(seconds=1)
                    )
                    before_min_interval_response = self.set_token_and_get_me(
                        token, before_min_interval_freeze_at
                    )
                    self.assertEqual(
                        before_min_interval_response.status_code, status.HTTP_200_OK
                    )
                    session.refresh_from_db()
                    auth_token.refresh_from_db()
                    self.assertEqual(auth_token.created, create_session_at)
                    self.assertEqual(auth_token.expiry, freeze_at + expected[0])

                    after_min_interval_freeze_at = (
                        freeze_at + expected[1] + timedelta(seconds=1)
                    )
                    after_min_interval_response = self.set_token_and_get_me(
                        token, after_min_interval_freeze_at
                    )
                    self.assertEqual(
                        after_min_interval_response.status_code, status.HTTP_200_OK
                    )
                    session.refresh_from_db()
                    auth_token.refresh_from_db()
                    self.assertEqual(auth_token.created, create_session_at)
                    self.assertEqual(
                        auth_token.expiry,
                        after_min_interval_freeze_at + expected[0],
                    )
                else:
                    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                    self.assertEqual(
                        response.data["detail"],
                        "Token parameters invalid for refresh. Please get a new token.",
                    )
                    with self.assertRaises(AuthToken.DoesNotExist):
                        auth_token.refresh_from_db()
                    with self.assertRaises(JasprSession.DoesNotExist):
                        session.refresh_from_db()

    def test_renew_token_patient_combinations(self):
        patient = self.create_patient()
        encounter = self.create_patient_encounter(patient=patient)
        parametrizer = Parametrizer(
            self.jaspr_session_params_valid_value_mapping,
            self.patient_combinations,
        )
        result = parametrizer.result
        now = timezone.now()
        for (
            in_er,
            from_native,
            long_lived,
        ) in parametrizer.all_mapping_parametrizations:
            with self.subTest(
                in_er=in_er, from_native=from_native, long_lived=long_lived
            ):
                create_session_at = timezone.now()
                with freeze_time(create_session_at):
                    session, token = self.create_jaspr_session_overriding_checks(
                        patient.user,
                        "Patient",
                        in_er,
                        from_native,
                        long_lived,
                        encounter,
                    )
                auth_token = session.auth_token
                # Make sure the token has the datetimes we expect before we
                # continue.
                self.assertEqual(auth_token.created, create_session_at)
                self.assertEqual(
                    auth_token.expiry, create_session_at + timedelta(minutes=17)
                )
                freeze_at = create_session_at + timedelta(seconds=91)
                response = self.set_token_and_get_me(token, freeze_at)
                expected = result[(in_er, from_native, long_lived)]
                if isinstance(expected[0], timedelta):
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                    session.refresh_from_db()
                    auth_token.refresh_from_db()
                    self.assertEqual(auth_token.created, create_session_at)
                    self.assertEqual(auth_token.expiry, freeze_at + expected[0])
                else:
                    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                    self.assertEqual(
                        response.data["detail"],
                        "Token parameters invalid for refresh. Please get a new token.",
                    )
                    with self.assertRaises(AuthToken.DoesNotExist):
                        auth_token.refresh_from_db()
                    with self.assertRaises(JasprSession.DoesNotExist):
                        session.refresh_from_db()


class TestJasprUidAndTokenBase(
    UidAndTokenTestMixin, TwilioClientTestCaseMixin, JasprApiTestCase
):
    """
    Base test class for testing uid and token authentication in Jaspr. There are
    `test_` methods in this class, but they will only be run in subclasses.
    """

    valid_mobile_phone = "+15005550006"

    @classmethod
    def setUpClass(cls):
        if cls is TestJasprUidAndTokenBase:
            raise SkipTest("Skip `TestJasprUidAndTokenBase` tests; it's a base class.")
        super().setUpClass()

    def post_data(self, data: dict) -> Response:
        with self.patched_twilio_verifications_create():
            return self.client.post(self.uri, data=data)

    def test_no_token_provided(self):
        """
        If no `token` is provided in the request, is the correct
        error message returned with the correct status code?
        """
        self.setup_patient()
        response = self.post_data({"mobile_phone": self.valid_mobile_phone})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            JasprToolsToGoUidAndTokenAuthentication.error_messages["no_token"],
        )

    def test_no_uid_provided(self):
        """
        If no `uid` is provided in the request, is the correct
        error message returned with the correct status code?
        """
        self.setup_patient()
        token = self.valid_token_for(self.patient.user)
        response = self.post_data(
            {"mobile_phone": self.valid_mobile_phone, "token": token}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            JasprToolsToGoUidAndTokenAuthentication.error_messages["no_uid"],
        )

    def test_invalid_uid(self):
        """
        If the the provided `uid` is invalid, is the correct invalid result returned?
        """
        self.setup_patient()
        uid = self.invalid_uidb64_for(self.patient.user)
        token = self.valid_token_for(self.patient.user)
        response = self.post_data(
            {"mobile_phone": self.valid_mobile_phone, "uid": uid, "token": token}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            JasprToolsToGoUidAndTokenAuthentication.error_messages["invalid"],
        )

    def test_invalid_token(self):
        """
        If the the provided `uid` is valid, but the `token` is invalid
        for that `uid`, is the correct invalid result returned?
        """
        self.setup_patient()
        uid = self.uidb64_for(self.patient.user)
        token = self.invalid_token_for(self.patient.user)
        response = self.post_data(
            {"mobile_phone": self.valid_mobile_phone, "uid": uid, "token": token}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            JasprToolsToGoUidAndTokenAuthentication.error_messages["invalid"],
        )

    def test_expired_token(self):
        """
        If the the provided `uid` is valid, but the `token` is expired
        for that `uid`, is the correct invalid/expired result returned?
        """
        self.setup_patient()
        uid = self.uidb64_for(self.patient.user)
        token = self.expired_token_for(self.patient.user)
        response = self.post_data(
            {"mobile_phone": self.valid_mobile_phone, "uid": uid, "token": token}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            JasprToolsToGoUidAndTokenAuthentication.error_messages["invalid"],
        )

    def test_valid_uidb64_and_token(self):
        """
        If the provided `uid` is valid and the provided `token`
        for that `uid` is valid, does the regular request proceed
        as normal?
        """
        self.setup_patient()
        uid, token = self.uidb64_and_token(self.patient.user)
        response = self.post_data(
            {"mobile_phone": self.valid_mobile_phone, "uid": uid, "token": token}
        )

        self.assertTrue(str(response.status_code).startswith("20"))

    def test_user_type_other_than_patient_forbidden(self):
        """
        Since this type of authentication is different/unusual compared to other types
        of authentication, it was difficult to use the standard permissions testing
        framework here. Hence we add one test to make sure that a `Technician`, even
        if authenticated successfully with a `uid` and `token`, hits a `403` forbidden
        response code.
        """
        technician = self.create_technician()
        uid, token = self.uidb64_and_token(technician.user)
        response = self.post_data(
            {"mobile_phone": self.valid_mobile_phone, "uid": uid, "token": token}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestJasprToolsToGoUidAndTokenAuthentication(TestJasprUidAndTokenBase):
    """
    NOTE: We use the `verify-phone-number` endpoint because that is an endpoint where
    this authentication scheme is in use, and we want to do more of an integration
    test where we check that the correct response is returned with status and data
    currently. If that endpoint changes or gets removed, we'll want/need to use a
    different endpoint to test with and change these tests around to accomodate that.
    """

    token_generator = JasprToolsToGoUidAndTokenAuthentication.token_generator

    def setUp(self):
        super().setUp()

        self.uri = "/v1/patient/verify-phone-number"

        self.assertEqual(
            PatientCheckPhoneNumberCodeView.authentication_classes,
            (JasprToolsToGoUidAndTokenAuthentication,),
            "Base assertion that needs to hold for these tests to run correctly.",
        )

    def setup_patient(self) -> Patient:
        self.patient = self.create_patient(
            user__mobile_phone=self.valid_mobile_phone,
            tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT,
        )


class TestResetPasswordUidAndTokenAuthentication(TestJasprUidAndTokenBase):
    """
    NOTE: We use the `reset-password/verify-phone-number` endpoint because that is an
    endpoint where this authentication scheme is in use, and we want to do more of an
    integration test where we check that the correct response is returned with status
    and data currently. If that endpoint changes or gets removed, we'll want/need to
    use a different endpoint to test with and change these tests around to accomodate
    that.
    """

    token_generator = JasprResetPasswordUidAndTokenAuthentication.token_generator

    def setUp(self):
        super().setUp()

        self.uri = "/v1/patient/reset-password/verify-phone-number"

        self.assertEqual(
            PatientResetPasswordCheckPhoneNumberCodeView.authentication_classes,
            (JasprResetPasswordUidAndTokenAuthentication,),
            "Base assertion that needs to hold for these tests to run correctly.",
        )

    def setup_patient(self) -> Patient:
        self.patient = self.create_tools_to_go_patient(
            user__mobile_phone=self.valid_mobile_phone
        )
