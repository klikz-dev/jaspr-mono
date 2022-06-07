from django.utils import timezone
from django.utils.dateparse import parse_datetime
from freezegun import freeze_time
from jaspr.apps.api.v1.serializers import PatientVideoSerializer
from jaspr.apps.kiosk.models import PatientVideo
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


class TestPatientVideoAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="patient/patient-videos",
            version_prefix="v1",
            factory_name="create_patient_video",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["create"]["allowed_groups"] = ["Patient"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Patient"]
        self.action_group_map["update"]["allowed_groups"] = ["Patient"]
        self.action_group_map["partial_update"]["allowed_groups"] = ["Patient"]


class TestPatientVideoAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/patient/patient-videos"
        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)
        self.set_patient_creds(self.patient, encounter=self.encounter)

    def test_list(self):
        patient_video = self.create_patient_video(patient=self.patient)
        other_patient_video = self.create_patient_video()
        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], patient_video.id)
        # Just check one of the other fields.
        self.assertEqual(response.data[0]["rating"], patient_video.rating)
        self.assertNotIn("patient", response.data)

    def test_retrieve(self):
        patient_video = self.create_patient_video(patient=self.patient)
        response = self.client.get(f"{self.uri}/{patient_video.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], patient_video.id)
        # Just check one of the other fields.
        self.assertEqual(response.data["rating"], patient_video.rating)
        self.assertNotIn("patient", response.data)

    def test_create(self):
        jaspr_media = self.create_media()

        now = timezone.now()
        with freeze_time(now):
            response = self.client.post(
                self.uri,
                data={
                    "video": jaspr_media.id,
                    "rating": 4,
                    "save_for_later": True,
                    "viewed": True,
                },
            )
        patient_video = PatientVideo.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(patient_video)
        self.assertEqual(patient_video.patient_id, self.patient.id)
        self.assertEqual(patient_video.video_id, jaspr_media.id)
        self.assertEqual(patient_video.rating, 4)
        self.assertTrue(patient_video.save_for_later)
        self.assertEqual(patient_video.viewed, now)
        self.assertEqual(response.data["id"], patient_video.id)
        self.assertEqual(response.data["video"], jaspr_media.id)
        self.assertEqual(response.data["rating"], patient_video.rating)
        self.assertEqual(response.data["save_for_later"], patient_video.save_for_later)
        self.assertEqual(parse_datetime(response.data["viewed"]), patient_video.viewed)
        self.assertNotIn("patient", response.data)

    def test_partial_update(self):
        now = timezone.now()
        jaspr_media = self.create_media()
        patient_video = self.create_patient_video(
            patient=self.patient, video=jaspr_media, viewed=now
        )

        with freeze_time(now):
            response = self.client.patch(
                f"{self.uri}/{patient_video.pk}",
                data={"rating": 3, "save_for_later": False, "viewed": None},
            )
        patient_video = PatientVideo.objects.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(patient_video)
        self.assertEqual(patient_video.patient_id, self.patient.id)
        self.assertEqual(patient_video.video_id, jaspr_media.id)
        self.assertEqual(patient_video.rating, 3)
        self.assertFalse(patient_video.save_for_later)
        # Checking that the frontend can post a "null" to reset this field.
        self.assertIsNone(patient_video.viewed)
        self.assertEqual(response.data["id"], patient_video.id)
        self.assertEqual(response.data["video"], jaspr_media.id)
        self.assertEqual(response.data["rating"], patient_video.rating)
        self.assertEqual(response.data["save_for_later"], patient_video.save_for_later)
        self.assertIsNone(response.data["viewed"])
        self.assertNotIn("patient", response.data)

    def test_partial_update_progress(self):
        now = timezone.now()
        jaspr_media = self.create_media()
        patient_video = self.create_patient_video(
            patient=self.patient, video=jaspr_media, viewed=now, progress=0,
        )

        with freeze_time(now):
            response = self.client.patch(
                f"{self.uri}/{patient_video.pk}", data={"progress": 63},
            )
        patient_video = PatientVideo.objects.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(patient_video)
        self.assertEqual(patient_video.progress, 63)
        self.assertEqual(response.data["progress"], 63)

    def test_partial_update_cannot_update_activity(self):
        jaspr_media = self.create_media()
        patient_video = self.create_patient_video(
            patient=self.patient, video=jaspr_media
        )
        other_jaspr_media = self.create_media()

        response = self.client.patch(
            f"{self.uri}/{patient_video.pk}",
            data={"video": other_jaspr_media.pk, "rating": 3, "save_for_later": True},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["video"],
            [PatientVideoSerializer.default_error_messages["video_update_disallowed"]],
        )
