from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestVideoAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="videos", version_prefix="v1", factory_name="create_media",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Patient"]


class TestVideoAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()
        self.patient = self.create_patient()
        self.uri = "/v1/videos"
        self.set_patient_creds(self.patient)
        self.jaspr_media1 = self.create_media(tags="buggz,bunny")

    def list_api_call(self, filters=None):
        if not filters:
            filters = {}
        filter_string = "&".join([f"{k}={v}" for k, v in filters.items()])
        if filter_string:
            filter_string = f"?{filter_string}"
        return self.client.get(f"{self.uri}{filter_string}")

    def retrieve_api_call(self, media_id):
        return self.client.get(f"{self.uri}/{media_id}")

    def test_list(self):
        """Can videos be listed?"""
        self.jaspr_media2 = self.create_media()
        response = self.list_api_call()
        self.assertEqual(len(response.data), 2)
        id_set = {self.jaspr_media1.id, self.jaspr_media2.id}
        self.assertEqual(set(map(lambda m: m["id"], response.data)), id_set)

    def test_retrieve(self):
        """Can videos be retrieved?"""
        response = self.retrieve_api_call(self.jaspr_media1.id)
        self.assertEqual(response.data["id"], self.jaspr_media1.id)
        self.assertEqual(len(response.data["tags"]), 2)
        self.assertTrue("buggz" in response.data["tags"])
        self.assertTrue("bunny" in response.data["tags"])

    def test_basic_tag_filtering(self):
        """Can videos be filtered by tag?"""
        self.jaspr_media1.tags.add("PLE")
        self.jaspr_media2 = self.create_media()
        self.jaspr_media2.tags.add("ELP")
        response = self.list_api_call(filters={"tag": "PLE"})
        self.assertEqual(len(response.data), 1)
