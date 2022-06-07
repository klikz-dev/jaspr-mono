from django.utils import timezone
from django.utils.dateparse import parse_datetime
from freezegun import freeze_time
from jaspr.apps.api.v1.serializers import PatientActivitySerializer
from jaspr.apps.kiosk.models import PatientActivity
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


class TestPatientActivityAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="patient/patient-activities",
            version_prefix="v1",
            factory_name="create_patient_activity",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["create"]["allowed_groups"] = ["Patient"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Patient"]
        self.action_group_map["update"]["allowed_groups"] = ["Patient"]
        self.action_group_map["partial_update"]["allowed_groups"] = ["Patient"]


class TestPatientActivityAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/patient/patient-activities"
        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)
        self.set_patient_creds(self.patient, encounter=self.encounter)

    def test_create(self):
        activity = self.create_activity()

        now = timezone.now()
        with freeze_time(now):
            response = self.client.post(
                self.uri,
                data={
                    "activity": activity.id,
                    "rating": 4,
                    "save_for_later": False,
                    "viewed": None,
                },
            )
        patient_activity = PatientActivity.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(patient_activity)
        self.assertEqual(patient_activity.patient_id, self.patient.id)
        self.assertEqual(patient_activity.activity_id, activity.id)
        self.assertEqual(patient_activity.rating, 4)
        self.assertFalse(patient_activity.save_for_later)
        self.assertEqual(patient_activity.viewed, None)
        self.assertEqual(response.data["id"], patient_activity.id)
        self.assertEqual(response.data["activity"], activity.id)
        self.assertEqual(response.data["rating"], patient_activity.rating)
        self.assertEqual(
            response.data["save_for_later"], patient_activity.save_for_later
        )
        self.assertEqual(response.data["viewed"], patient_activity.viewed)

    def test_partial_update(self):
        activity = self.create_activity()
        patient_activity = self.create_patient_activity(
            patient=self.patient, activity=activity
        )

        now = timezone.now()
        with freeze_time(now):
            response = self.client.patch(
                f"{self.uri}/{patient_activity.pk}",
                data={"rating": 4, "save_for_later": False, "viewed": True},
            )
        patient_activity = PatientActivity.objects.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(patient_activity)
        self.assertEqual(patient_activity.patient_id, self.patient.id)
        self.assertEqual(patient_activity.activity_id, activity.id)
        self.assertEqual(patient_activity.rating, 4)
        self.assertFalse(patient_activity.save_for_later)
        self.assertEqual(patient_activity.viewed, now)
        self.assertEqual(response.data["id"], patient_activity.id)
        self.assertEqual(response.data["activity"], activity.id)
        self.assertEqual(response.data["rating"], patient_activity.rating)
        self.assertEqual(
            response.data["save_for_later"], patient_activity.save_for_later
        )
        self.assertEqual(parse_datetime(response.data["viewed"]), now)

    def test_partial_update_cannot_update_activity(self):
        activity = self.create_activity()
        patient_activity = self.create_patient_activity(
            patient=self.patient, activity=activity
        )
        other_activity = self.create_activity()

        response = self.client.patch(
            f"{self.uri}/{patient_activity.pk}",
            data={"activity": other_activity.pk, "rating": 3, "save_for_later": True},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["activity"],
            [
                PatientActivitySerializer.default_error_messages[
                    "activity_update_disallowed"
                ]
            ],
        )
