from datetime import timedelta

from django.test import override_settings
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status

from jaspr.apps.kiosk.models import JasprSession
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestTechnicianHeartbeatAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(resource_pattern="technician/heartbeat", version_prefix="v1")

        self.action_group_map["create"]["allowed_groups"] = ["Technician"]


@override_settings(
    IN_ER_TECHNICIAN_DEFAULT_TOKEN_EXPIRES_AFTER=timedelta(hours=1),
    IN_ER_TECHNICIAN_DEFAULT_TOKEN_MIN_REFRESH_INTERVAL_SECONDS=60,
)
class TestTechnicianHeartbeatAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.technician = self.create_technician()
        self.uri = "/v1/technician/heartbeat"

    def test_heartbeat_extends_technicians_jaspr_session_auth_token_expiry(self):
        now = timezone.now()
        with freeze_time(now):
            jaspr_session, token_string = JasprSession.create(
                self.technician.user,
                "Technician",
                in_er=True,
                from_native=False,
                long_lived=False,
            )
        auth_token = jaspr_session.auth_token
        self.assertEqual(auth_token.created, now, "Pre-condition")
        self.assertEqual(auth_token.expiry, now + timedelta(hours=1), "Pre-condition")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_string}")
        with freeze_time(now + timedelta(seconds=61)):
            response = self.client.post(self.uri, data={})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        auth_token.refresh_from_db()
        self.assertEqual(auth_token.created, now)
        self.assertEqual(
            auth_token.expiry, now + timedelta(seconds=61) + timedelta(hours=1)
        )

    def test_heartbeat_honors_technician_in_er_min_refresh_interval_seconds(self):
        now = timezone.now()
        with freeze_time(now):
            jaspr_session, token_string = JasprSession.create(
                self.technician.user,
                "Technician",
                in_er=True,
                from_native=False,
                long_lived=False,
            )
        auth_token = jaspr_session.auth_token
        self.assertEqual(auth_token.created, now, "Pre-condition")
        self.assertEqual(auth_token.expiry, now + timedelta(hours=1), "Pre-condition")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_string}")
        # NOTE: At the time of writing, the above test does `timedelta(seconds=61)` to
        # test the other side of the boundary.
        with freeze_time(now + timedelta(seconds=59)):
            response = self.client.post(self.uri, data={})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        auth_token.refresh_from_db()
        self.assertEqual(auth_token.created, now)
        self.assertEqual(auth_token.expiry, now + timedelta(hours=1))
