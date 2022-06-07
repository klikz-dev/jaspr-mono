from django.contrib.contenttypes.models import ContentType
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status
from jaspr.apps.api.v1.views import StaticMediaView

MEDIA_URL = "/media/"


class TestStaticMediaTestCase(JasprApiTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/static-media"

    def test_basic_case(self):
        expected = StaticMediaView.getData(MEDIA_URL)
        response = self.client.get(self.uri)
        actual = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK, actual)
        self.assertDictEqual(actual, expected)

