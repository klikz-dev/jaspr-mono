import datetime

from django.utils import timezone
from rest_framework import status

from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestPatientSecurityQuestionAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403,  404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="patient/security-questions",
            version_prefix="v1",
            factory_name="create_security_question",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["create"]["allowed_groups"] = ["Patient"]
        # self.action_group_map["partial_update"]["allowed_groups"] = ["Patient"]
        # self.action_group_map["update"]["allowed_groups"] = ["Patient"]
        # self.action_group_map["retrieve"]["allowed_groups"] = ["Patient"]

        # Don't need any `detail` endpoints since this is just a view and not a viewset
        # (so these shouldn't get hit by the router anyway).
        del self.action_group_map["retrieve"]
        del self.action_group_map["update"]
        del self.action_group_map["partial_update"]
        del self.action_group_map["delete"]


class TestPatientSecurityQuestionAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)
        self.uri = "/v1/patient/security-questions"

    def test_create_security_questions(self):
        """Can a user create security questions?"""
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        data = {"question": "Why?", "answer": "Because"}
        response = self.client.post(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_create_security_question_permission(self):
        """ Is a recent heartbeat necessary to create a security question? """
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        eleven_minutes_ago = timezone.now() - datetime.timedelta(minutes=11)
        self.encounter.last_heartbeat = eleven_minutes_ago
        self.encounter.save()

        data = {"question": "Why?", "answer": "Because"}
        response = self.client.post(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_can_get_security_questions(self):
        """Can a user get security questions?"""
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        self.assertTrue("question" in response.data)
        self.assertTrue("answer" not in response.data)

    def test_can_update_security_questions(self):
        """A patient can only update a security question by POSTING"""
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        data = {"question": "Why?", "answer": "Because"}
        response = self.client.patch(self.uri + "/" + str(self.encounter.id), data=data)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, response.data
        )

        response = self.client.put(self.uri + "/" + str(self.encounter.id), data=data)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, response.data
        )

    def test_update_security_questions_permission(self):
        """Is a recent heartbeat necessary to update security questions?"""
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        eleven_minutes_ago = timezone.now() - datetime.timedelta(minutes=11)
        self.encounter.last_heartbeat = eleven_minutes_ago
        self.encounter.save()

        data = {"question": "Why?", "answer": "Because"}
        response = self.client.post(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_partial_update_security_questions_permission(self):
        """Is a recent heartbeat necessary to partial_update security questions?"""
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        eleven_minutes_ago = timezone.now() - datetime.timedelta(minutes=11)
        self.encounter.last_heartbeat = eleven_minutes_ago
        self.encounter.save()

        data = {"question": "Why?", "answer": "Because"}
        response = self.client.post(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)
