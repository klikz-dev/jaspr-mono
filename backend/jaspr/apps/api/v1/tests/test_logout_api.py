from typing import Union

from django.utils import timezone
from knox.models import AuthToken
from rest_framework import status

from jaspr.apps.accounts.models import LoggedOutAuthToken
from jaspr.apps.kiosk.models import Patient, Technician
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase

from .helpers import assert_kiosk_instance_logged_out


class TestPatientLogoutAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403,  404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="patient/logout",
            version_prefix="v1",
            factory_name="create_patient",
        )

        # NOTE/TODO: When this is locked down to a specific user type, this should be
        # updated.
        self.action_group_map["create"]["allowed_groups"] = [
            "Technician",
            "Patient",
        ]

        # Don't need any `detail` endpoints since this is just a view and not a viewset
        # (so these shouldn't get hit by the router anyway).
        del self.action_group_map["retrieve"]
        del self.action_group_map["update"]
        del self.action_group_map["partial_update"]
        del self.action_group_map["delete"]


class TestTechnicianLogoutAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403,  404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="technician/logout",
            version_prefix="v1",
            factory_name="create_technician",
        )

        # NOTE/TODO: When this is locked down to a specific user type, this should be
        # updated.
        self.action_group_map["create"]["allowed_groups"] = [
            "Technician",
            "Patient",
        ]

        # Don't need any `detail` endpoints since this is just a view and not a viewset
        # (so these shouldn't get hit by the router anyway).
        del self.action_group_map["retrieve"]
        del self.action_group_map["update"]
        del self.action_group_map["partial_update"]
        del self.action_group_map["delete"]


class BaseLogoutTestCase(JasprApiTestCase):
    uri: str

    def _test_logout(
        self,
        kiosk_instance: Union[Patient, Technician],
        manually_initiated: bool = None,
    ) -> None:
        user = kiosk_instance.user
        auth_token = AuthToken.objects.get()
        self.assertEqual(user, auth_token.user)
        digest = auth_token.digest
        token_key = auth_token.token_key
        time_before_logout = timezone.now()
        post_data = {}
        if manually_initiated is not None:
            post_data["manually_initiated"] = manually_initiated
        response = self.client.post(self.uri, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        logout_record = LoggedOutAuthToken.objects.get()
        self.assertEqual(logout_record.user, user)
        self.assertEqual(logout_record.digest, digest)
        self.assertEqual(logout_record.token_key, token_key)
        self.assertGreater(logout_record.logged_out_at, time_before_logout)
        assert_kiosk_instance_logged_out(
            self,
            kiosk_instance,
            # Since we're using `self.set_creds`, which does a regular login, we won't
            # be in the ER.
            False,
            time_before_logout,
            manually_initiated=manually_initiated,
        )


class TestPatientLogoutAPI(BaseLogoutTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/logout"

    def test_patient_successful_logout_with_manual_initiation(self):
        """Can a Patient successfully logout with manual initiation?"""
        patient = self.create_patient()
        self.set_patient_creds(patient)
        self._test_logout(patient, manually_initiated=True)

    def test_patient_successful_logout_with_automatic_initiation(self):
        """Can a Patient successfully logout with automatic initiation?"""
        patient = self.create_patient()
        self.set_patient_creds(patient)
        self._test_logout(patient, manually_initiated=False)


class TestTechnicianLogoutAPI(BaseLogoutTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/technician/logout"

    def test_technician_successful_logout(self):
        """Can a Technician successfully logout?"""
        technician = self.create_technician()
        self.set_technician_creds(technician)
        self._test_logout(technician)
