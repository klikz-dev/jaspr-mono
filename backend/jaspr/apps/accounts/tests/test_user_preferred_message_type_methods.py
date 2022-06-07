from django.test import SimpleTestCase
from jaspr.apps.accounts.models import User


class TestUserPreferredMessageTypeMethods(SimpleTestCase):
    def setUp(self):
        self.user = User()

    def add(self, message_type):
        self.user.add_to_preferred_message_type(message_type, db_save=False)

    def remove(self, message_type):
        self.user.remove_from_preferred_message_type(message_type, db_save=False)

    def run_add_or_remove_test(self, method, message_type, mapping):
        for initial, expected in mapping.items():
            self.user.preferred_message_type = initial
            method(message_type)
            self.assertEqual(
                self.user.preferred_message_type,
                expected,
                f"{method.__name__} {message_type}: {initial} !==> {expected}",
            )

    def test_adding_email(self):
        self.run_add_or_remove_test(
            self.add,
            "email",
            {
                "": "email",
                "email": "email",
                "sms": "email and sms",
                "email and sms": "email and sms",
            },
        )

    def test_removing_email(self):
        self.run_add_or_remove_test(
            self.remove,
            "email",
            {"": "", "email": "", "sms": "sms", "email and sms": "sms"},
        )

    def test_adding_sms(self):
        self.run_add_or_remove_test(
            self.add,
            "sms",
            {
                "": "sms",
                "email": "email and sms",
                "sms": "sms",
                "email and sms": "email and sms",
            },
        )

    def test_removing_sms(self):
        self.run_add_or_remove_test(
            self.remove,
            "sms",
            {"": "", "email": "email", "sms": "", "email and sms": "email"},
        )
