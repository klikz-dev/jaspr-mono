from datetime import timedelta

from django.utils import timezone
from freezegun import freeze_time
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status

from .helpers import assert_kiosk_instance_not_logged_out


class TestPatientHeartbeatPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(resource_pattern="patient/heartbeat", version_prefix="v1")

        self.action_group_map["create"]["allowed_groups"] = ["Patient"]


class TestPatientHeartbeatView(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)
        self.uri = "/v1/patient/heartbeat"

    def test_patient_records_time_of_heartbeat(self):
        """ Can patient record heartbeat? """
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        # NOTE: We set `history_count` after calling `self.set_creds` above because
        # `set_creds` could potentially generate a history record for the
        # `Encounter` (at the time of writing it doesn't, but in case we change
        # things up in the future or add things, etc. we want this test to still work
        # as intended).
        history_count = self.encounter.history.count()
        now = timezone.now()
        with freeze_time(now):
            response = self.client.post(self.uri, data={})

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data
        )
        self.encounter.refresh_from_db()

        self.assertEqual(self.encounter.last_heartbeat, now)

        # verify that we've only changed the last_heartbeat, and haven't added a history record.
        self.assertNotEqual(self.encounter.modified, now)
        self.assertEqual(self.encounter.history.count(), history_count)

    def test_heartbeat_ignored_when_not_in_er_even_if_would_be_forbidden_in_er(self):
        """
        If the `Patient` is locked out from a timeout and/or session lock and
        not in the ER, is a 204 returned without any updates?
        """
        self.set_patient_creds(self.patient, encounter=self.encounter)
        now = timezone.now()
        self.encounter.last_heartbeat = now
        self.encounter.session_lock = True
        self.encounter.save()
        frozen_time = now + timedelta(minutes=10, seconds=1)
        with freeze_time(frozen_time):
            response = self.client.post(self.uri, data={})

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data
        )
        self.assertEqual(self.encounter.last_heartbeat, now)
        self.assertTrue(self.encounter.session_lock)

    def test_heartbeat_ignored_when_not_in_er_even_if_would_set_heartbeat_in_er(self):
        """
        If the `Patient` is not locked out from a timeout or session lock and
        not in the ER, is a 204 returned without any `last_heartbeat` updates?
        """
        self.set_patient_creds(self.patient, encounter=self.encounter)
        now = timezone.now()
        self.encounter.last_heartbeat = now
        self.encounter.session_lock = False
        self.encounter.save()
        frozen_time = now + timedelta(seconds=31)
        with freeze_time(frozen_time):
            response = self.client.post(self.uri, data={})

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data
        )
        self.assertEqual(self.encounter.last_heartbeat, now)
        self.assertFalse(self.encounter.session_lock)

    def test_patient_not_logged_out_from_timeout_if_in_er(self):
        """
        If the `Patient` is locked out from a timeout and in the ER, is that
        `Patient` not logged out and a 403 returned?
        """
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        now = timezone.now()
        self.encounter.last_heartbeat = now
        self.encounter.session_lock = False
        self.encounter.save()
        frozen_time = now + timedelta(minutes=10, seconds=1)
        with freeze_time(frozen_time):
            response = self.client.post(self.uri, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        assert_kiosk_instance_not_logged_out(self, self.patient, frozen_time)

    def test_patient_not_logged_out_from_session_lock_if_in_er(self):
        """
        If the `Patient` is locked out from `session_lock = True` and in the ER,
        is that `Patient` not logged out and a 403 returned?
        """
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        now = timezone.now()
        self.encounter.last_heartbeat = None
        self.encounter.session_lock = True
        self.encounter.save()
        response = self.client.post(self.uri, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)
        assert_kiosk_instance_not_logged_out(self, self.patient, now)
