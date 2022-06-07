from rest_framework import status
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestFreshdeskSSOAPI(JasprApiTestCase):

    def setUp(self):
        super().setUp()

        self.uri = "/v1/technician/freshdesk"

        self.system, self.clinic, self.department = self.create_full_healthcare_system()
        technician = self.create_technician(
            system=self.system, department=self.department
        )
        self.set_technician_creds(technician)

    def test_freshdesk_sso(self):
        """Can we get a redirect URL?"""
        response = self.client.get(self.uri, data={
            "state": "abcdef",
            "nonce": "12345678"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
