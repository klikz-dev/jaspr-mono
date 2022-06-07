from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


class TestCommonConcernAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="common-concerns",
            version_prefix="v1",
            factory_name="create_common_concern",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Patient"]


class TestCommonConcernAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/common-concerns"
        self.patient = self.create_patient()
        self.set_patient_creds(self.patient)

    def test_list(self):
        """ Can a patient see an ordered list of active common concerns?"""
        cc2 = self.create_common_concern(order=2)
        cc1 = self.create_common_concern(order=1)
        self.create_common_concern(status="archived")

        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], cc1.title)
        self.assertEqual(response.data[1]["title"], cc2.title)

    def test_retrieve(self):
        """ Can a patient retrieve 1 common concern if it is active?"""
        cc1 = self.create_common_concern(status="active")
        response = self.client.get(f"{self.uri}/{cc1.id}")
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data["id"], cc1.id)
        self.assertEqual(response.data["title"], cc1.title)
        self.assertEqual(response.data["content"], cc1.content)

    def test_retrieve(self):
        """ Are common concerns with status of archived barred from retrieval? """
        cc1 = self.create_common_concern(status="archived")
        response = self.client.get(f"{self.uri}/{cc1.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
