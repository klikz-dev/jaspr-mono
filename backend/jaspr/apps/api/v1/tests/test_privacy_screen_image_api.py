from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


class TestPatientPrivacyScreenImageAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403,  404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="patient/privacy-screen-images",
            version_prefix="v1",
            factory_name="create_privacy_screen_image",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.groups["Patient"]["set_creds_kwargs"] = {"in_er": True, "encounter": True}


class TestPatientPrivacyScreenImagesAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/privacy-screen-images"
        self.image = self.create_privacy_screen_image()
        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)

    def test_list_privacy_screen(self):
        """Can an authenticated patient get a list of photos?"""

        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue("id" in response.data[0])
        self.assertTrue("url" in response.data[0])

class TestPatientPrivacyScreenImageAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/privacy-screen-image"
        self.image = self.create_privacy_screen_image()
        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)

    def test_patient_can_set_privacy_screen_image(self):
        """Can an authenticated patient set their photo"""
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        image = self.encounter.patient.current_privacy_screen_images.first()
        response = self.client.patch(self.uri, {
            "privacy_screen_image": image.pk,
        })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


