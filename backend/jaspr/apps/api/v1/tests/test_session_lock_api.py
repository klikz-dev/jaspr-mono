from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.kiosk.models import Action
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


class TestPatientSessionLockViewPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(resource_pattern="patient/session-lock", version_prefix="v1")

        self.action_group_map["create"]["allowed_groups"] = ["Patient"]
        self.groups["Patient"]["set_creds_kwargs"] = {"in_er": True, "encounter": True}


class TestPatientSessionLockAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)
        self.uri = "/v1/patient/session-lock"

    def test_set_session_lock(self):
        """Can a patient_user turn session_lock to True? """

        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        response = self.client.post(self.uri, data={})
        self.patient.refresh_from_db()
        self.encounter.refresh_from_db()

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data
        )

        self.assertEqual(self.encounter.session_lock, True)

        self.assertIsNotNone(
            Action.objects.get(
                action=ActionNames.LOCKOUT,
                patient=self.encounter.patient,
                encounter=self.encounter,
                in_er=True,
            )
        )
