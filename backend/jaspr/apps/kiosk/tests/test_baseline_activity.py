from django.utils import timezone

from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from jaspr.apps.test_infrastructure.testcases import JasprTestCase
from jaspr.apps.kiosk.activities.intro.factory import create


class EncounterTestCase(JasprTestCase):

    fixtures = [
        #"jaspr/apps/bootstrap/fixtures/jaspr_content.json",
        #"jaspr/apps/bootstrap/fixtures/jaspr_user.json",
        #"jaspr/apps/bootstrap/fixtures/jaspr_root.json"
    ]

    def setUp(self):
        super().setUp()
        self.encounter = self.create_patient_encounter()


    def test_activity_creation(self):
        aa = create(self.encounter)

