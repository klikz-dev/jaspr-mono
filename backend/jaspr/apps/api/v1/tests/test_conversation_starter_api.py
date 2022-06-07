from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


class TestConversationStarterAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="conversation-starters",
            version_prefix="v1",
            factory_name="create_conversation_starter",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Patient"]


class TestConversationStarterAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/conversation-starters"
        self.patient = self.create_patient()
        self.set_patient_creds(self.patient)

    def test_list(self):
        """ Can a patient see an ordered list of active common concerns?"""
        cs2 = self.create_conversation_starter(order=2)
        cs1 = self.create_conversation_starter(order=1)
        self.create_conversation_starter(status="archived")

        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["content"], cs1.content)
        self.assertEqual(response.data[1]["content"], cs2.content)

    def test_retrieve(self):
        """ Can a patient retrieve 1 common concern if it is active?"""
        cs1 = self.create_conversation_starter(status="active")
        response = self.client.get(f"{self.uri}/{cs1.id}")
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data["id"], cs1.id)
        self.assertEqual(response.data["content"], cs1.content)

    def test_retrieve(self):
        """ Are common concerns with status of archived barred from retrieval? """
        cs1 = self.create_conversation_starter(status="archived")
        response = self.client.get(f"{self.uri}/{cs1.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
