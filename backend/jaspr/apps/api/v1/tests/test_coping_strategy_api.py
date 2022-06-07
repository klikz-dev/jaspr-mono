from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


class TestCopingStrategyAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="coping-strategies",
            version_prefix="v1",
            factory_name="create_coping_strategy",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Patient"]


class TestCopingStrategyAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/coping-strategies"
        self.patient = self.create_patient()
        self.set_patient_creds(self.patient)

    def test_list(self):
        """ Can patient see only active coping strategies? """
        self.create_coping_strategy(name="Go for a walk.")
        self.create_coping_strategy(name="Go to the Gym.")
        self.create_coping_strategy(name="old", status="archived")
        response = self.client.get(self.uri)
        self.assertEqual(len(response.data), 2)

    def test_list_filter(self):
        """ Can patient filter active coping strategies by category? """
        physical_category = self.create_coping_strategy_category(
            name="Physical", slug="physical"
        )

        coping_strategy = self.create_coping_strategy(
            category=physical_category, name="Walk"
        )
        self.create_coping_strategy(
            category=physical_category, name="Jog", status="archived"
        )
        self.create_coping_strategy()
        response = self.client.get(self.uri + "?category__slug=physical")

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], coping_strategy.pk)
        self.assertEqual(response.data[0]["title"], coping_strategy.title)

    def test_retrieve(self):
        """ Are all fields present that we'd expect on a coping strategy?"""
        coping_strategy = self.create_coping_strategy()
        response = self.client.get(f"{self.uri}/{coping_strategy.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["id"], coping_strategy.pk)
        self.assertEqual(response.data["title"], coping_strategy.title)
        self.assertTrue(
            coping_strategy.image.url
            and response.data["image"].endswith(coping_strategy.image.url)
        )
        self.assertEqual(len(response.data["category"]), 3)
        self.assertEqual(response.data["category"]["id"], coping_strategy.category.id)
        self.assertEqual(
            response.data["category"]["name"], coping_strategy.category.name
        )
        self.assertEqual(
            response.data["category"]["why_text"], coping_strategy.category.why_text
        )

    def test_retrieve_archived_coping_strategy_yields_404(self):
        """ Does patient get 404 when attempting to view archived coping strategy? """
        coping_strategy = self.create_coping_strategy(status="archived")
        response = self.client.get(f"{self.uri}/{coping_strategy.id}")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
