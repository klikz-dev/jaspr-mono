import random
import sys
import unittest
from datetime import timedelta
from inspect import getmembers

from django.utils import timezone
from django_rq import get_worker

from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.kiosk.jobs import queue_action_creation
from jaspr.apps.kiosk.models import Action
from jaspr.apps.test_infrastructure.testcases import JasprRedisTestCase
from jaspr.apps.kiosk.activities.activity_utils import ActivityType


class TestActions(JasprRedisTestCase):
    def test_action_created(self):
        """
        Use the default test redis behavior in this test that just
        runs the job immediately.
        """
        self.system, self.clinic, self.department = self.create_full_healthcare_system()

        patient = self.create_patient()
        encounter = self.create_patient_encounter(
            patient=patient, department=self.department
        )
        specific_time = timezone.now()
        client_time = specific_time - timedelta(milliseconds=555)
        in_er = False
        queue_action_creation(
            {
                "patient": patient,
                "encounter": encounter,
                "in_er": in_er,
                "action": ActionNames.JAH_WALKTHROUGH_ARRIVE,
                # NOTE: `screen` and `extra` below are made up for this test. They may
                # or may not be actual/legit values that the frontend would send.
                "screen": "Walkthrough",
                "extra": "Paced Breathing",
                "timestamp": specific_time,
                "client_timestamp": client_time,
            }
        )
        action = Action.objects.get()
        self.assertEqual(action.patient, patient)
        self.assertEqual(action.encounter, encounter)
        self.assertEqual(action.in_er, in_er)
        self.assertEqual(action.action, ActionNames.JAH_WALKTHROUGH_ARRIVE)
        self.assertEqual(action.screen, "Walkthrough")
        self.assertEqual(action.extra, "Paced Breathing")
        self.assertEqual(action.section_uid, "")
        self.assertEqual(action.timestamp, specific_time)
        self.assertEqual(action.client_timestamp, client_time)

    @unittest.skipIf(
        sys.platform == "win32",
        "'win32' platform does not support `os.fork` required by `rqworker`.",
    )
    def test_action_created_from_job(self):
        """
        Explicitly allow the redis job to be queued and run separately
        in this test. Also checks that the timestamp has a default
        set correctly on queueing vs. on running.
        """
        self.system, self.clinic, self.department = self.create_full_healthcare_system()

        patient = self.create_patient()
        encounter = self.create_patient_encounter(
            patient=patient, department=self.department
        )
        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        client_time = timezone.now()
        with self.patch_delay_of("jaspr.apps.kiosk.jobs.create_action"):
            queue_action_creation(
                {
                    "patient": patient,
                    "encounter": encounter,
                    # Being consistent with how this action would happen currently. At
                    # the time of writing `Assessment`s cannot be updated outside
                    # of the ER.
                    "in_er": True,
                    "action": ActionNames.ARRIVE,
                    # NOTE: `screen` is made up for this Ftest. It or may not be an
                    # actual/legit value that the frontend would send.
                    "screen": "CUI",
                    "section_uid": [*encounter.sections_dictionary][0],
                    "client_timestamp": client_time,
                }
            )
            time_after_queue = timezone.now()
            get_worker().work(burst=True)
        action = Action.objects.get()
        self.assertEqual(action.patient, patient)
        self.assertEqual(action.in_er, True)
        self.assertEqual(action.action, ActionNames.ARRIVE)
        self.assertEqual(action.screen, "CUI")
        self.assertEqual(action.extra, "")
        self.assertEqual(action.section_uid, [*encounter.sections_dictionary][0])
        self.assertLess(action.timestamp, time_after_queue)
        self.assertEqual(action.client_timestamp, client_time)
        # In this case the client server timestamp should be greater than the client timestamp.
        self.assertGreater(action.timestamp, action.client_timestamp)

    def test_jah_action_naming_consistency(self):
        """
        Check that all the `ActionNames` that have a constant or value starting with
        `JAH` are consistent with respect to the naming scheme.

        This in part is to make sure that `ActionNames` is consistent in the naming
        scheme for the logic in `validate_action_that_is_jah_only` that populates
        `JAH_ACTIONS`.
        """
        for member, value in getmembers(ActionNames):
            if (
                member.casefold().startswith("jah")
                or isinstance(value, str)
                and value.casefold().startswith("jah")
            ):
                with self.subTest(member=member, value=value):
                    self.assertTrue(member.startswith("JAH_"))
                    self.assertTrue(value.startswith("JAH"))
