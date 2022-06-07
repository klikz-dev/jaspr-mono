import datetime

from django.utils import timezone
from jaspr.apps.accounts.models import LogUserLoginAttempts, User
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestAccountLock(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.technician = self.create_technician()
        self.uri = "/v1/technician/login"

    def test_successful_login_generates_record(self):
        """If a user logins correctly is it recorded in the db?"""

        data = {
            "email": self.technician.user.email,
            "password": "password",
            "organization_code": "generic",
        }
        self.client.post(self.uri, data=data)

        user_attempts = LogUserLoginAttempts.objects.filter(user=self.technician.user)
        self.assertEqual(len(user_attempts), 1)
        self.assertEqual(user_attempts[0].was_successful, True)

    def test_failed_login_generates_record(self):
        """If a user logins with wrong password is it recored in the db?"""

        data = {
            "email": self.technician.user.email,
            "password": "notthisone",
            "organization_code": "generic",
        }
        self.client.post(self.uri, data=data)

        user_attempts = LogUserLoginAttempts.objects.filter(user=self.technician.user)
        self.assertEqual(len(user_attempts), 1)
        self.assertEqual(user_attempts[0].was_successful, False)

    def test_successive_failed_login_cause_lockout_since_last_success(self):
        """If user fails login 5 times in 15 minutes without success then lockout?"""

        # one successful login needed to get locked out; happened on activated
        data = {
            "email": self.technician.user.email,
            "password": "notthisone",
            "organization_code": "generic",
        }
        for loop in range(5):
            self.client.post(self.uri, data=data)
            user_attempts = LogUserLoginAttempts.objects.filter(
                user=self.technician.user, was_successful=False
            )
            self.assertEqual(len(user_attempts), loop + 1)  # account for first login
            self.assertEqual(user_attempts[loop].was_successful, False)

        user = User.objects.get(id=self.technician.user.id)
        if user.account_locked_at:
            locked_out = True
        else:
            locked_out = False

        self.assertEqual(locked_out, True)

    def test_success_login_middle_of_five_unsuccessful_no_lockout(self):
        """If user has a successful login in the middle of 5 unsuccessful
        log ins in 15 minutes then no lockout?"""

        # one successful login needed to get locked out; happened on activated
        self.set_technician_creds(self.technician)

        for loop in range(3):
            self.client.post(
                self.uri,
                {
                    "email": self.technician.user.email,
                    "password": "wrongone",
                    "organization_code": "generic",
                },
            )
            user_attempts = LogUserLoginAttempts.objects.filter(
                user=self.technician.user, was_successful=False
            )
            self.assertEqual(len(user_attempts), loop + 1)  # account for first login
            self.assertEqual(user_attempts[loop].was_successful, False)

        self.client.post(
            self.uri,
            {
                "email": self.technician.user.email,
                "password": "password",
                "organization_code": "generic",
            },
        )
        user_attempts = LogUserLoginAttempts.objects.filter(
            user=self.technician.user, was_successful=True
        ).latest("date_time")
        self.assertEqual(user_attempts.was_successful, True)

        for loop in range(2):
            self.client.post(
                self.uri,
                {
                    "email": self.technician.user.email,
                    "password": "wrongone",
                    "organization_code": "generic",
                },
            )
            user_attempts = LogUserLoginAttempts.objects.filter(
                user=self.technician.user, was_successful=False
            )
            self.assertEqual(len(user_attempts), loop + 4)  # account for first login
            self.assertEqual(user_attempts[loop + 3].was_successful, False)

        user = User.objects.get(id=self.technician.user.id)
        if user.account_locked_at:
            locked_out = True
        else:
            locked_out = False

        self.assertEqual(locked_out, False)

    def test_success_login_during_lockout_fails(self):
        """If user account locked and not greater than an hour, user is not
        allowed to login?"""

        # one successful login needed to get locked out; happened on activated
        self.set_technician_creds(self.technician)
        user = User.objects.get(id=self.technician.user.id)
        user.account_locked_at = timezone.now() - datetime.timedelta(minutes=5)
        user.save()

        # Test account is locked
        user = User.objects.get(id=self.technician.user.id)
        self.assertTrue(user.account_locked_at is not None)

        # login with right credentials
        response = self.client.post(
            self.uri,
            {
                "email": self.technician.user.email,
                "password": "password",
                "organization_code": "generic",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["non_field_errors"], ["User account is locked."])
        user_attempts = LogUserLoginAttempts.objects.filter(
            user=self.technician.user
        ).latest("date_time")
        self.assertFalse(user_attempts.was_successful)

        user.refresh_from_db()
        self.assertTrue(user.account_locked_at is not None)

    def test_success_login_after_lockout_timeout_success(self):
        """If user account locked and greater than an hour, user is
        allowed to login?"""

        # mark user as locked.
        user = User.objects.get(id=self.technician.user.id)
        user.account_locked_at = timezone.now() - datetime.timedelta(hours=2)
        user.save()

        # Test account is locked
        user = User.objects.get(id=self.technician.user.id)
        self.assertTrue(user.account_locked_at is not None)

        # login with right credentials
        self.client.post(
            self.uri,
            {
                "email": self.technician.user.email,
                "password": "password",
                "organization_code": "generic",
            },
        )
        user_attempts = LogUserLoginAttempts.objects.filter(
            user=self.technician.user, was_successful=True
        ).latest("date_time")
        self.assertEqual(user_attempts.was_successful, True)

        user.refresh_from_db()
        self.assertTrue(user.account_locked_at is None)
