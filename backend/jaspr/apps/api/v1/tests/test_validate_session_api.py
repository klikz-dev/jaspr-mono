from django.utils import timezone
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


class TestPatientValidateSessionAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(resource_pattern="patient/validate-session", version_prefix="v1")

        self.action_group_map["create"]["allowed_groups"] = ["Patient"]
        self.groups["Patient"]["set_creds_kwargs"] = {"in_er": True, "encounter": True}


class TestPatientValidateSessionAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.image = self.create_privacy_screen_image()
        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)
        self.uri = "/v1/patient/validate-session"
        self.encounter.encrypted_answer = "The Right Stuff"
        self.encounter.privacy_screen_image = self.image
        self.encounter.save()


    def test_patient_can_validate_correctly(self):
        """ Can a Patient post credentials and be verified? """
        self.encounter.session_lock = True
        self.encounter.save()

        data = {"security_question_answer": "The Right Stuff", "image": self.image.pk}

        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        now = timezone.now()
        response = self.client.post(self.uri, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.encounter.refresh_from_db()
        self.assertGreater(self.encounter.last_heartbeat, now)
        self.assertEqual(self.encounter.session_validation_attempts, 0)
        self.assertEqual(self.encounter.session_lock, False)

    def test_patient_receives_400_with_incorrect_image(self):
        """ Is a Patient given a 400 with incorrect iamge? """
        wrong_image = self.create_privacy_screen_image()
        data = {"security_question_answer": "The Right Stuff", "image": wrong_image.pk}

        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        response = self.client.post(self.uri, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"non_field_errors": ["Incorrect picture or answer. Please try again."]},
        )

    def test_patient_receives_400_with_incorrect_answer(self):
        """ Is a Patient given a 400 with incorrect iamge? """
        data = {
            "security_question_answer": "Right Answer - Not!",
            "image": self.image.pk,
        }

        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        response = self.client.post(self.uri, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"non_field_errors": ["Incorrect picture or answer. Please try again."]},
        )

    def test_patient_receives_400_with_right_answer_after_5_incorrect(self):
        """ Is a Patient given a 400 after answering incorrectly 5 times? """
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)

        data = {
            "security_question_answer": "Right Answer - Not!",
            "image": self.image.pk,
        }
        self.client.post(self.uri, data)
        self.client.post(self.uri, data)
        self.client.post(self.uri, data)
        self.client.post(self.uri, data)
        self.client.post(self.uri, data)

        data["security_question_answer"] = "The Right Stuff"

        response = self.client.post(self.uri, data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )
        self.assertEqual(
            response.data,
            {
                "non_field_errors": [
                    "Your account has been locked due to 5 failed attempts."
                ]
            },
        )

