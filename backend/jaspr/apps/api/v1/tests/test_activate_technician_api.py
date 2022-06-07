from datetime import datetime, timedelta

from django.core import mail
from django.utils import timezone
from freezegun import freeze_time
from parameterized import parameterized
from rest_framework import status

from jaspr.apps.api.v1.serializers import (
    MeTechnicianSerializer,
    ReadOnlyJasprSessionSerializer,
)
from jaspr.apps.common.functions import resolve_frontend_url
from jaspr.apps.common.tests.mixins import UidAndTokenTestMixin
from jaspr.apps.kiosk.models import JasprSession, Patient, Technician
from jaspr.apps.kiosk.tokens import (
    JasprExtraSecurityTokenGenerator,
    JasprSetPasswordTokenGenerator,
)
from jaspr.apps.message_logs.models import EmailLog
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase

from .helpers import assert_auth_token_string_valid, assert_technician_logged_in


class TestActivateTechnicianRedirectAPI(UidAndTokenTestMixin, JasprApiTestCase):
    token_generator = JasprExtraSecurityTokenGenerator

    def setUp(self):
        super().setUp()

        self.url = "/v1/technician/activate/{uid}/{token}"

    def test_invalid_token_redirect(self):
        """
        If an invalid token is provided, is there a redirect to the appropriate
        frontend URL?
        """
        technician = self.create_technician()
        uid = self.uidb64_for(technician.user)
        token = self.invalid_token_for(technician.user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url,
            f"{resolve_frontend_url()}/technician/activate/?activate-technician-link=invalid",
        )

    def test_valid_token_user_not_technician_redirect(self):
        """
        If an valid token is provided but the `User` is not a `Technician`, is there
        a redirect to the appropriate frontend URL?
        """
        user = self.create_user()
        uid, token = self.uidb64_and_token(user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url,
            f"{resolve_frontend_url()}/technician/activate/?activate-technician-link=invalid",
        )

    def test_valid_token_user_is_technician_redirect(self):
        """
        If an valid token is provided and the `User` has a `Technician` is there a
        redirect to the appropriate frontend URL?
        """
        technician = self.create_technician()
        uid, token = self.uidb64_and_token(technician.user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url,
            f"{resolve_frontend_url(technician=technician)}/technician/activate/#uid={uid}&token={token}",
        )


class TestActivateTechnicianAPI(UidAndTokenTestMixin, JasprApiTestCase):
    token_generator = JasprExtraSecurityTokenGenerator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/technician/activate"
        self.system = self.create_healthcare_system(name="Activate System", activation_code="correct-code")
        self.clinic = self.create_clinic(name="Activate Clinic", system=self.system)

    @parameterized.expand([("case_insensitive_match", True), ("exact_match", False)])
    def test_technician_successfully_gets_code_for_next_stuff(
        self, _, case_insensitive_match
    ):
        email = "tech1@jasprhealth.com"
        technician = self.create_technician(
            user__email=email,
            system=self.system,
            activated=False,
        )
        now = timezone.now()
        if case_insensitive_match:
            post_email = "TeCh1@jasprhealth.com"
        else:
            post_email = email
        with freeze_time(now):
            response = self.post_with_creds(
                self.uri,
                technician.user,
                data={"email": post_email, "activation_code": "correct-code"},
            )
            set_password_token = self.valid_token_for(
                technician.user, token_generator=JasprSetPasswordTokenGenerator
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"set_password_token": set_password_token})
        technician.refresh_from_db()
        # Make sure this endpoint isn't doing the activation, the next one should.
        self.assertFalse(technician.activated)
        self.assertIsNone(technician.first_activated_at)
        self.assertIsNone(technician.last_activated_at)

    def test_email_mismatch(self):
        technician = self.create_technician(
            user__email="tech1@jasprhealth.com",
            system=self.system,
            activated=False,
        )
        response = self.post_with_creds(
            self.uri,
            technician.user,
            data={"email": "tech2@jasprhealth.com", "activation_code": "correct-code"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            ["Invalid email and/or activation code provided."],
        )

    def test_clinic_code_mismatch(self):
        technician = self.create_technician(
            user__email="tech1@jasprhealth.com",
            system=self.system,
            activated=False,
        )
        response = self.post_with_creds(
            self.uri,
            technician.user,
            data={
                "email": "tech1@jasprhealth.com",
                "activation_code": "incorrect-code",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            ["Invalid email and/or activation code provided."],
        )

    def test_user_type_other_than_technician_forbidden(self):
        """
        Since the authentication/permissions here are different/unusual compared to
        other types of authentication/permissions, it was difficult to use the
        standard permissions testing framework here. Hence we add one test to make
        sure that a `Patient`, even if authenticated successfully with a valid
        activation style token, hits a `403` forbidden response code.
        """
        department = self.create_department(clinic=self.clinic)
        patient = self.create_patient(
            user__email="patient1@jasprhealth.com"
        )

        self.set_patient_creds(patient)
        response = self.post_with_creds(
            self.uri,
            patient.user,
            data={
                "email": "patient1@jasprhealth.com",
                "activation_code": "correct-code",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestActivateTechnicianSetPasswordAPI(UidAndTokenTestMixin, JasprApiTestCase):
    token_generator = JasprExtraSecurityTokenGenerator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/technician/set-password"

    def _test_confirmation_email_sent(
        self, request_time: datetime, technician: Technician
    ) -> None:
        """
        If a `Technician` activates his/her account then a confirmation email should
        be sent. This checks for the presence of that email.
        """
        self.assertEqual(len(mail.outbox), 1)
        email_log = EmailLog.objects.get(user_id=technician.user_id, date=request_time)
        self.assertEqual(
            email_log.subject,
            "Congrats on activating your Jaspr Tech account",
        )

    def test_can_set_password_if_not_activated_yet(self):
        """
        Can an authenticated `Technician` set his/her password if a valid
        `set_password_token` (along with authentication `uid` and `token`) is
        provided and have `activated` get set to `True`, along with all the other
        fields being set properly and getting a confirmation email?
        """
        technician = self.create_technician(
            activated=False,
            user__password_complex=False,
            user__password_changed=None,
        )
        new_password = "TheGoose87623##"
        set_password_token = self.valid_token_for(
            technician.user, token_generator=JasprSetPasswordTokenGenerator
        )
        now = timezone.now()
        with freeze_time(now):
            response = self.post_with_creds(
                self.uri,
                technician.user,
                data={
                    "password": new_password,
                    "set_password_token": set_password_token,
                },
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        technician.user.refresh_from_db()
        self.assertTrue(technician.user.check_password(new_password))
        self.assertEqual(technician.user.password_changed, now)
        self.assertTrue(technician.user.password_complex)
        technician.refresh_from_db()
        self.assertTrue(technician.activated)
        self.assertEqual(technician.first_activated_at, now)
        self.assertEqual(technician.last_activated_at, now)
        self._test_confirmation_email_sent(now, technician)

        assert_auth_token_string_valid(self, response.data["token"], technician)
        jaspr_session = JasprSession.objects.get(auth_token__user=technician.user)
        self.assertIs(jaspr_session.in_er, True)
        self.assertIs(jaspr_session.from_native, False)
        self.assertIs(jaspr_session.long_lived, False)
        assert_technician_logged_in(
            self,
            technician,
            now,
            from_native=False,
            long_lived=False,
        )
        response.data["technician"].pop("support_url")
        me_tech_data = MeTechnicianSerializer(instance=technician).data
        me_tech_data.pop("support_url")
        self.assertEqual(
            response.data["technician"],
            me_tech_data,
        )
        self.assertEqual(
            response.data["session"],
            ReadOnlyJasprSessionSerializer(instance=jaspr_session).data,
        )
        self.assertIn("expiry", response.data)
        self.assertEqual(len(response.data), 4, response.data)

    def test_can_set_password_if_already_activated(self):
        """
        Can an authenticated `Technician` set his/her password if a valid
        `set_password_token` (along with authentication `uid` and `token`) is
        provided, even if `activated` is already set to `True`?
        """
        now = timezone.now()
        technician = self.create_technician(
            activated=True,
            first_activated_at=now - timedelta(days=2),
            last_activated_at=now - timedelta(days=2),
            user__password_complex=True,
            user__password_changed=now - timedelta(days=2),
        )
        new_password = "TheGoose87623##"
        set_password_token = self.valid_token_for(
            technician.user, token_generator=JasprSetPasswordTokenGenerator
        )
        with freeze_time(now):
            response = self.post_with_creds(
                self.uri,
                technician.user,
                data={
                    "password": new_password,
                    "set_password_token": set_password_token,
                },
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        technician.user.refresh_from_db()
        self.assertTrue(technician.user.check_password(new_password))
        self.assertEqual(technician.user.password_changed, now)
        self.assertTrue(technician.user.password_complex)
        technician.refresh_from_db()
        self.assertTrue(technician.activated)
        self.assertEqual(technician.first_activated_at, now - timedelta(days=2))
        self.assertEqual(technician.last_activated_at, now)
        self._test_confirmation_email_sent(now, technician)

        assert_auth_token_string_valid(self, response.data["token"], technician)
        jaspr_session = JasprSession.objects.get(auth_token__user=technician.user)
        self.assertIs(jaspr_session.in_er, True)
        self.assertIs(jaspr_session.from_native, False)
        self.assertIs(jaspr_session.long_lived, False)
        assert_technician_logged_in(
            self,
            technician,
            now,
            from_native=False,
            long_lived=False,
        )
        response.data["technician"].pop("support_url")
        me_tech_data = MeTechnicianSerializer(instance=technician).data
        me_tech_data.pop("support_url")
        self.assertEqual(
            response.data["technician"],
            me_tech_data,
        )
        self.assertEqual(
            response.data["session"],
            ReadOnlyJasprSessionSerializer(instance=jaspr_session).data,
        )
        self.assertIn("expiry", response.data)
        self.assertEqual(len(response.data), 4, response.data)

    def test_password_not_complex(self):
        """
        Does the endpoint enforce password requirements for the `Technician`?
        """
        technician = self.create_technician()
        new_password = "TheGoose##"
        set_password_token = self.valid_token_for(
            technician.user, token_generator=JasprSetPasswordTokenGenerator
        )
        response = self.post_with_creds(
            self.uri,
            technician.user,
            data={"password": new_password, "set_password_token": set_password_token},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data["password"],
            [
                (
                    "Passwords must be at least 8 characters and have at least one "
                    "uppercase character, one lowercase character, and one number."
                )
            ],
        )

    def test_token_invalid(self):
        """
        If the provided `token` is invalid, is a 400 response returned with a nice
        error message?
        """
        technician = self.create_technician()
        new_password = "TheGoose87623##"
        set_password_token = self.invalid_token_for(
            technician.user, token_generator=JasprSetPasswordTokenGenerator
        )
        response = self.post_with_creds(
            self.uri,
            technician.user,
            data={"password": new_password, "set_password_token": set_password_token},
            # Use a different token generator than the correct one
            # (`JasprExtraSecurityTokenGenerator`) to simulate an invalid token.
            token_generator=JasprSetPasswordTokenGenerator,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [
                (
                    "The link is invalid. Please get a new link sent to you or contact "
                    "support. Be aware that links currently expire after 15 days."
                )
            ],
        )

    def test_set_password_token_invalid(self):
        """
        If the provided `set_password_token` is invalid, is a 403 response returned?
        """
        technician = self.create_technician()
        new_password = "TheGoose87623##"
        set_password_token = self.invalid_token_for(
            technician.user, token_generator=JasprSetPasswordTokenGenerator
        )
        response = self.post_with_creds(
            self.uri,
            technician.user,
            data={"password": new_password, "set_password_token": set_password_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_type_other_than_technician_forbidden(self):
        """
        Since the authentication/permissions here are different/unusual compared to
        other types of authentication/permissions, it was difficult to use the
        standard permissions testing framework here. Hence we add one test to make
        sure that a `Patient`, even if authenticated successfully with a valid
        `set_password_token`, hits a `403` forbidden response code.
        """
        patient = self.create_patient(
            user__password_complex=False,
            user__password_changed=None,
            tools_to_go_status=Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
        )
        self.set_patient_creds(patient)
        new_password = "TheGoose87623##"
        set_password_token = self.valid_token_for(
            patient.user, token_generator=JasprSetPasswordTokenGenerator
        )
        response = self.post_with_creds(
            self.uri,
            patient.user,
            data={"password": new_password, "set_password_token": set_password_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
