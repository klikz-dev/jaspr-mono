from operator import itemgetter

from rest_framework import status

from jaspr.apps.api.v1.serializers import ActivateExistingPatientSerializer
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestTechnicianPatientDataAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(resource_pattern="technician/patient-data", version_prefix="v1")

        self.action_group_map["list"]["allowed_groups"] = ["Technician"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Technician"]
        # Just simulate some `pk` for the clinic location and some `pk` for the
        # `Patient`.
        self.detail_uri = self.base_uri = f"{self.base_uri}/2/5"


class TestTechnicianPatientDataAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/technician/patient-data"
        self.system, self.clinic, self.department = self.create_full_healthcare_system()
        self.technician = self.create_technician(
            system=self.system, department=self.department
        )
        self.department_technician = self.technician.departmenttechnician_set.first()

    def assert_serializer_error_thrown(self, data, data_key, error_key):
        if error_key is ...:  # Just check that there was some error thrown.
            self.assertGreaterEqual(len(data[data_key]), 1)
        else:  # We have a specific key to check for one of our custom error messages.
            self.assertEqual(
                data[data_key][0],
                ActivateExistingPatientSerializer().error_messages[error_key],
            )

    def test_skills(self):
        """
        Can a `Patient`'s skills be retrieved by `pk` from a valid/allowed
        `Technician`'s request?
        """
        patient = self.create_patient(department=self.department)
        encounter = self.create_patient_encounter(patient=patient)
        first_skill = self.create_patient_activity(patient=patient)
        second_skill = self.create_patient_activity(patient=patient)
        # Create another skill to make sure we're filtering the skills down to the
        # correct patient and the correct data is returned.
        third_skill = self.create_patient_activity(patient=self.create_patient())

        self.set_technician_creds(self.technician)
        response = self.client.get(f"{self.uri}/{self.department.pk}/{patient.pk}")
        self.set_patient_creds(patient, encounter=encounter)
        patient_response = self.client.get("/v1/patient/activities")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(patient_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(patient_response.data), 3)
        sort = lambda l: sorted(
            l,
            key=lambda data: 0
            if data["patient_activity"] is None
            else data["patient_activity"],
        )
        skills = sort(response.data["skills"])
        self.assertEqual(skills, sort(patient_response.data))
        self.assertIsNone(skills[0]["patient_activity"])
        self.assertIn(skills[1]["patient_activity"], (first_skill.pk, second_skill.pk))
        self.assertIn(skills[2]["patient_activity"], (first_skill.pk, second_skill.pk))
        self.assertEqual(skills[0]["id"], third_skill.activity.pk)
        self.assertIn(
            skills[1]["id"], (first_skill.activity.pk, second_skill.activity.pk)
        )
        self.assertIn(
            skills[2]["id"], (first_skill.activity.pk, second_skill.activity.pk)
        )

    def test_stories_and_videos(self):
        """
        Can the stories videos be retrieved by `pk` from a valid/allowed
        `Technician`'s request?
        """
        patient = self.create_patient(department=self.department)
        encounter = self.create_patient_encounter(patient=patient, department=self.department)
        first_story_video = self.create_media(tags="PLE", name="First Story")

        # Checking that it's just filtering on the "PLE" tag and not `type`.
        second_story_audio = self.create_media(
            name="Second Story", file_type="audio", tags="PLE,buggz,daffy"
        )

        # Create another media to make sure we're filtering the "videos" (even
        # though technically the `video` endpoint _could_ include audio, but "PLE" tag
        # enforcement should prevent that) down to the correct tags.
        self.create_media()

        # get technician response
        # uses MediaSerializer via TechnicianPatientDataView
        self.set_technician_creds(self.technician)
        technician_response = self.client.get(
            f"{self.uri}/{self.department.pk}/{patient.pk}"
        )
        self.assertEqual(
            technician_response.status_code,
            status.HTTP_200_OK,
            technician_response.data,
        )
        self.assertEqual(
            len(technician_response.data["stories_videos"]), 2, technician_response.data
        )

        self.set_patient_creds(patient, encounter=encounter)
        patient_response = self.client.get("/v1/videos?tag=PLE")
        self.assertEqual(patient_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(patient_response.data), 2)

        sort = lambda l: sorted(l, key=itemgetter("id"))
        stories_videos = sort(technician_response.data["stories_videos"])
        self.assertEqual(stories_videos, sort(patient_response.data))
        self.assertIn(
            stories_videos[0]["id"], (first_story_video.pk, second_story_audio.pk)
        )
        self.assertIn(
            stories_videos[1]["id"], (first_story_video.pk, second_story_audio.pk)
        )

    def test_stories_patient_videos(self):
        """
        Can a `Patient`'s `PatientVideo`s be retrieved by `pk` from a valid/allowed
        `Technician`'s request?
        """
        patient = self.create_patient(department=self.department)
        encounter = self.create_patient_encounter(patient=patient, department=self.department)
        first_patient_video = self.create_patient_video(patient=patient)
        second_patient_video = self.create_patient_video(patient=patient)
        # Create another patient video to make sure we're filtering the kiosk
        # patient videos down to the correct patient.
        self.create_patient_video(patient=self.create_patient())

        self.set_technician_creds(self.technician)
        response = self.client.get(f"{self.uri}/{self.department.pk}/{patient.pk}")
        self.set_patient_creds(patient, encounter=encounter)
        patient_response = self.client.get("/v1/patient/patient-videos")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(patient_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(patient_response.data), 2)
        sort = lambda l: sorted(l, key=itemgetter("id"))
        patient_videos = sort(response.data["patient_videos"])
        self.assertEqual(patient_videos, sort(patient_response.data))
        self.assertIn(
            patient_videos[0]["id"],
            (first_patient_video.pk, second_patient_video.pk),
        )
        self.assertIn(
            patient_videos[1]["id"],
            (first_patient_video.pk, second_patient_video.pk),
        )

    def test_all_data(self):
        """
        Can a `Patient`'s data be retrieved by `pk` from a valid/allowed
        `Technician`'s request (more of an integration test for all of the various
        `Patient` data that is returned)?
        """
        patient = self.create_patient(department=self.department)
        encounter = self.create_patient_encounter(
            patient=patient, department=self.department
        )
        skill = self.create_patient_activity(patient=patient)
        story_video = self.create_media(file_type="video", tags="PLE")
        patient_video = self.create_patient_video(patient=patient)
        answers = encounter.get_answers()

        self.set_technician_creds(self.technician)
        response = self.client.get(f"{self.uri}/{self.department.pk}/{patient.pk}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["skills"]), 1)
        self.assertEqual(response.data["skills"][0]["id"], skill.activity.pk)
        self.assertEqual(response.data["skills"][0]["patient_activity"], skill.pk)
        self.assertEqual(len(response.data["stories_videos"]), 1)
        self.assertEqual(response.data["stories_videos"][0]["id"], story_video.pk)
        self.assertEqual(len(response.data["patient_videos"]), 1)
        self.assertEqual(response.data["patient_videos"][0]["id"], patient_video.pk)
        self.assertEqual(response.data["answers"], answers)

    def test_cannot_get_data_if_wrong_clinic(self):
        """
        Is the data not retrievable by `pk` if the `Patient`'s clinic location does
        not belong to the `Technician`'s clinic?
        """
        (
            other_system,
            other_clinic,
            other_department,
        ) = self.create_full_healthcare_system(name="Other System")
        patient = self.create_patient(department=other_department)
        self.set_technician_creds(self.technician)
        response = self.client.get(f"{self.uri}/{other_department.pk}/{patient.pk}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_serializer_error_thrown(
            response.data, "department", "improper_department"
        )

    def test_cannot_get_data_if_wrong_department_within_clinic(self):
        """
        Is the data not retrievable by `pk` if the `Patient`'s clinic location does
        not correspond to one of the `Technician`s `ClinicLocationTechnician`
        records?
        """
        other_department_within_clinic = self.create_department(
            name="Other Department", clinic=self.clinic
        )
        patient = self.create_patient(department=other_department_within_clinic)
        self.set_technician_creds(self.technician)
        response = self.client.get(
            f"{self.uri}/{other_department_within_clinic.pk}/{patient.pk}"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_serializer_error_thrown(
            response.data, "department", "improper_department"
        )

    def test_cannot_get_data_if_correct_department_but_not_active(self):
        """
        Is the data not retrievable by `pk` if the `Patient`'s clinic location
        corresponds to one of the `Technician`s `ClinicLocationTechnician` records
        but the record is not active?
        """
        self.department_technician.status = "inactive"
        self.department_technician.save()

        patient = self.create_patient(department=self.department)

        self.set_technician_creds(self.technician)

        response = self.client.get(f"{self.uri}/{self.department.pk}/{patient.pk}")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_serializer_error_thrown(response.data, "detail", ...)

    def test_cannot_get_data_if_department_does_not_match_patients(self):
        """
        Is the data not retrievable by `pk` if the clinic location corresponds to one
        of the `Technician`s `ClinicLocationTechnician` records but does not match
        the `Patient`s clinic location?
        """
        other_department = self.create_department(name="Other Dept", clinic=self.clinic)
        patient = self.create_patient(department=other_department)
        self.set_technician_creds(self.technician)
        response = self.client.get(f"{self.uri}/{self.department.pk}/{patient.pk}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_serializer_error_thrown(
            response.data, "non_field_errors", "department_mismatch"
        )

    def test_department_valid_but_no_patient_with_pk(self):
        """
        Is the data not retrievable by `pk` if the clinic location corresponds to one
        of the `Technician`s `ClinicLocationTechnician` records but the provided `pk`
        does not correspond to any existing `Patient`?
        """
        self.set_technician_creds(self.technician)
        patient = self.create_patient()
        pk = patient.pk
        assert pk and isinstance(pk, int)
        patient.delete()
        response = self.client.get(f"{self.uri}/{self.department.pk}/{pk}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assert_serializer_error_thrown(response.data, "patient", ...)
