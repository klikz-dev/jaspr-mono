from django.utils import timezone
from jaspr.apps.api.v1.serializers import PatientChangePasswordSerializer
from jaspr.apps.kiosk.models import Patient
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


class TestPatientChangePasswordAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(resource_pattern="patient/change-password", version_prefix="v1")

        self.groups["Patient"]["factory"] = self.create_tools_to_go_patient
        self.action_group_map["create"]["allowed_groups"] = ["Patient"]


class TestPatientChangePasswordAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/change-password"

    def test_can_change_password(self):
        """
        Can an authenticated (and tools to go setup finished) patient change
        his/her password?
        """
        patient = self.create_tools_to_go_patient(user__password_complex=False)
        time_before_patch = timezone.now()
        self.set_patient_creds(patient)
        current_password = "password"
        new_password = "TheGoose87623##"
        response = self.client.post(
            self.uri,
            data={"current_password": current_password, "password": new_password},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Make sure 'current_password' is write only.
        self.assertNotIn("current_password", response.data)
        # Make sure 'password' is write only.
        self.assertNotIn("password", response.data)
        patient.user.refresh_from_db()
        self.assertTrue(patient.user.check_password(new_password))
        self.assertGreater(patient.user.password_changed, time_before_patch)
        self.assertTrue(patient.user.password_complex)

    def test_password_not_complex(self):
        """
        Check that password complexity checking is not done for validation, but that
        the `password_complex` field is set accordingly. The above test (at the time
        of writing) tests for a complex password while this test tests for a
        non-complex password and still makes sure everything else works except for
        setting the field.
        """
        patient = self.create_tools_to_go_patient(user__password_complex=True)
        time_before_patch = timezone.now()
        self.set_patient_creds(patient)
        current_password = "password"
        new_password = "a"
        response = self.client.post(
            self.uri,
            data={"current_password": current_password, "password": new_password},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("current_password", response.data)
        self.assertNotIn("password", response.data)
        patient.user.refresh_from_db()
        self.assertTrue(patient.user.check_password(new_password))
        self.assertGreater(patient.user.password_changed, time_before_patch)
        self.assertFalse(patient.user.password_complex)

    def test_current_password_incorrect(self):
        """
        If the provided `current_password` is incorrect, is a 400 response returned
        with an error message?
        """
        patient = self.create_tools_to_go_patient()
        self.set_patient_creds(patient)
        current_password = "passwordy"
        new_password = "TheGoose87623##"
        response = self.client.post(
            self.uri,
            data={"current_password": current_password, "password": new_password},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["current_password"][0],
            PatientChangePasswordSerializer.default_error_messages["current_password"],
        )

    def test_requires_tools_to_go_phonenumber_verified(self):
        """
        This is partially a test to make sure that `HasToolsToGoSetupFinished` is
        working properly. You shouldn't be able to change your Jaspr password until
        you're at the "Setup Finished" tools to go status.
        """
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED
        )
        self.set_patient_creds(patient)
        password = "password"
        new_password = "TheGoose87623##"

        response = self.client.post(
            self.uri, data={"current_password": password, "password": new_password}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
