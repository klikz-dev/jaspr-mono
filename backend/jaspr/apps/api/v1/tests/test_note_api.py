from django.utils import timezone
from rest_framework import status

from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from jaspr.apps.clinics.models import GlobalPreferences
from jaspr.apps.kiosk.activities.activity_utils import ActivityType


class TestNoteApiPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):

        super().setUp(
            resource_pattern="technician/patients",
            version_prefix="v1",
        )

        # because list action points to the base_uri
        self.action_group_map["list"]["allowed_groups"] = ["Technician"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Technician"]

        # Just simulate  `pk` for the `Patient`.
        self.detail_uri = self.base_uri = f"{self.base_uri}/1/note"


class TestNoteApiRetrieve(JasprApiTestCase):
    fixtures = [
        "jaspr/apps/bootstrap/fixtures/jaspr_content.json",
    ]
    def setUp(self):
        super().setUp()

        GlobalPreferences.objects.update_or_create(timezone="America/New_York", consent_language="")
        self.technician = self.create_technician()
        self.department_technician = self.technician.departmenttechnician_set.get(
            department__name="unassigned"
        )
        self.department = self.department_technician.department
        self.clinic = self.department.clinic
        self.system = self.technician.system

        self.patient_data = {
            "department": self.department,
        }
        self.patient = self.create_patient(**self.patient_data)
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )

        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        self.uri = f"/v1/technician/patients/{self.patient.pk}/note"
        self.set_technician_creds(self.technician)

    def test_technician_can_retrieve_patient_note(self):
        self.encounter.rate_psych_section_viewed = timezone.now()
        self.encounter.start_time = timezone.now()
        self.encounter.save()
        response = self.client.get(self.uri)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data,
        )

        self.assertTrue(
            "SUICIDE STATUS INTERVIEW FINDINGS FROM PATIENT USE OF JASPR HEALTH"
            in response.data["narrative_note"]
        )

    # def test_technician_can_retrieve_patient_note(self):
    #
    #     response = self.client.get(self.uri)
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_200_OK,
    #         response.data,
    #     )
    #     self.assertTrue(
    #         "Patient has not begun Suicide Status Interview, no note available."
    #         in response.data["narrative_note"]
    #     )

    def test_scoring_suicide_index_score_displays_proper_info_when_none(self):
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        suicide_assessment.rate_psych_section_viewed = timezone.now()
        suicide_assessment.save()

        # verify that scoring_suicide_index_score is None
        self.assertEqual(self.encounter.get_answers()["metadata"]["scoring_suicide_index_score"], None)

        response = self.client.get(self.uri)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data,
        )

    def test_scoring_suicide_index_score_displays_proper_info_when_0(self):
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        suicide_assessment.rate_psych_section_viewed = timezone.now()

        # set things up to make a 0 for scoring_suicide_index_score
        self.encounter.save_answers({"wish_live": 0, "wish_die": 0})
        suicide_assessment.refresh_from_db()
        # verify that we got a 0
        self.assertEqual(suicide_assessment.scoring_suicide_index_score, 0)

        response = self.client.get(self.uri)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data,
        )

        self.assertTrue(
            "not calculated due to missing answers*" not in response.data["narrative_note"]
        )
