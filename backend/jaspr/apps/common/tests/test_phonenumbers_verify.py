import logging

from jaspr.apps.common.phonenumbers.verify import (
    VerificationCodeInvalid,
    VerificationCodeNotFound,
    VerificationTwilioException,
    check_phonenumber_verification,
)
from jaspr.apps.common.phonenumbers.verify import logger as verify_logger
from jaspr.apps.common.phonenumbers.verify import send_phonenumber_verification
from jaspr.apps.test_infrastructure.mixins.common_mixins import (
    TwilioClientTestCaseMixin,
)
from jaspr.apps.test_infrastructure.testcases import JasprSimpleTestCase
from parameterized import parameterized
from twilio.base.exceptions import TwilioRestException
from twilio.rest.verify.v2.service.verification import VerificationInstance
from twilio.rest.verify.v2.service.verification_check import VerificationCheckInstance


class TestSendPhonenumberVerification(TwilioClientTestCaseMixin, JasprSimpleTestCase):
    def test_success(self):
        phone_number = "+14155552671"
        with self.patched_twilio_verifications_create() as mock_verifications_create:
            result = send_phonenumber_verification(phone_number)

        mock_verifications_create.assert_called_once_with(phone_number, channel="sms")
        self.assertIsInstance(result, VerificationInstance)

    @parameterized.expand(
        [
            ("code-60203", 60203, 400, True, "code:60203"),
            ("code-60205", 60205, 400, True, "code:60205"),
            ("code-60207", 60207, 400, True, "code:60203"),
            ("code-60212", 60212, 400, True, "code:60203"),
            ("status-400", None, 400, False, "generic:..."),
            ("status-404", None, 404, True, "exception:NotFound"),
            ("status-429", None, 429, True, "code:60203"),
            ("status-500", None, 500, True, "generic:..."),
            ("status-503", None, 503, True, "generic:..."),
            ("status-555", None, 555, False, "generic:..."),
        ]
    )
    def test_error(self, _, twilio_code, status_code, handled_specifically, expected):
        twilio_rest_exception = TwilioRestException(
            status_code,
            # NOTE: Example/made up SID/example URI, don't expect this to actually
            # work/make sense/be a valid URL.
            "https://api.twilio.com/Accounts/AC60edab5c3343b14c531e8cf123a6ff2a/Messages.json",
            msg="A squirrel intercepted the message and replaced every S with Q.",
            code=twilio_code,
            method="POST",
        )
        source, value = expected.split(":")
        if source == "code":
            error_message = VerificationTwilioException.TWILIO_CODE_MAP[int(value)]
            exception_class = VerificationTwilioException
        elif source == "generic":
            error_message = VerificationTwilioException.GENERIC_ERROR_MESSAGE
            exception_class = VerificationTwilioException
        else:
            if value == "NotFound":
                exception_class = VerificationCodeNotFound
                error_message = VerificationCodeNotFound.error_message
        phone_number = "+14155552671"
        user_id = 27
        with self.patched_twilio_verifications_create() as mock_verifications_create, self.assertLogs(
            verify_logger, logging.INFO
        ) as logs, self.assertRaises(
            exception_class
        ) as e_info:
            mock_verifications_create.side_effect = twilio_rest_exception
            send_phonenumber_verification(phone_number, user_id=user_id)

        mock_verifications_create.assert_called_once_with(phone_number, channel="sms")
        self.assertEqual(e_info.exception.error_message, error_message)
        self.assertIn(
            (
                f"(user_id={user_id}, twilio_error_code={twilio_code}, "
                f"status_code={status_code}, "
                f"handled_specifically={handled_specifically}, twilio_msg=A squirrel "
                "intercepted the message and replaced every S with Q.) Raising "
                f"{exception_class.__name__} from TwilioRestException "
                f"({twilio_rest_exception})."
            ),
            logs.output[-1],
        )


class TestCheckPhonenumberVerification(TwilioClientTestCaseMixin, JasprSimpleTestCase):
    def test_success(self):
        phone_number = "+14155552671"
        code = "123456"
        with self.patched_twilio_verification_checks_create() as mock_verification_checks_create:
            result = check_phonenumber_verification(phone_number, code)

        mock_verification_checks_create.assert_called_once_with(
            to=phone_number, code=code
        )
        self.assertEqual(result.status, "approved")
        self.assertIsInstance(result, VerificationCheckInstance)

    def test_pending_and_hence_invalid(self):
        phone_number = "+14155552671"
        code = "123456"
        with self.patched_twilio_verification_checks_create(
            status="pending"
        ) as mock_verification_checks_create, self.assertRaises(
            VerificationCodeInvalid
        ) as e_info:
            check_phonenumber_verification(phone_number, code)

        mock_verification_checks_create.assert_called_once_with(
            to=phone_number, code=code
        )
        self.assertEqual(
            e_info.exception.error_message, VerificationCodeInvalid.error_message
        )

    def test_denied(self):
        phone_number = "+14155552671"
        code = "123456"
        with self.patched_twilio_verification_checks_create(
            status="denied"
        ) as mock_verification_checks_create, self.assertRaises(
            VerificationCodeNotFound
        ) as e_info:
            check_phonenumber_verification(phone_number, code)

        mock_verification_checks_create.assert_called_once_with(
            to=phone_number, code=code
        )
        self.assertEqual(
            e_info.exception.error_message, VerificationCodeNotFound.error_message
        )

    @parameterized.expand(
        [
            ("code-60202", 60202, 400, True, "code:60202"),
            ("code-60205", 60205, 400, True, "code:60205"),
            ("code-60207", 60207, 400, True, "code:60202"),
            ("code-60212", 60212, 400, True, "code:60202"),
            ("status-400", None, 400, False, "generic:..."),
            ("status-404", None, 404, True, "exception:NotFound"),
            ("status-429", None, 429, True, "code:60202"),
            ("status-500", None, 500, True, "generic:..."),
            ("status-503", None, 503, True, "generic:..."),
            ("status-555", None, 555, False, "generic:..."),
        ]
    )
    def test_error(self, _, twilio_code, status_code, handled_specifically, expected):
        twilio_rest_exception = TwilioRestException(
            status_code,
            # NOTE: Example/made up SID/example URI, don't expect this to actually
            # work/make sense/be a valid URL.
            "https://api.twilio.com/Accounts/AC60edab5c3343b14c531e8cf123a6ff2a/Messages.json",
            msg="A squirrel intercepted the message and replaced every S with Q.",
            code=twilio_code,
            method="POST",
        )
        source, value = expected.split(":")
        if source == "code":
            error_message = VerificationTwilioException.TWILIO_CODE_MAP[int(value)]
            exception_class = VerificationTwilioException
        elif source == "generic":
            error_message = VerificationTwilioException.GENERIC_ERROR_MESSAGE
            exception_class = VerificationTwilioException
        else:
            if value == "NotFound":
                exception_class = VerificationCodeNotFound
                error_message = VerificationCodeNotFound.error_message
        phone_number = "+14155552671"
        code = "123456"
        user_id = 36
        with self.patched_twilio_verification_checks_create() as mock_verification_checks_create, self.assertLogs(
            verify_logger, logging.INFO
        ) as logs, self.assertRaises(
            exception_class
        ) as e_info:
            mock_verification_checks_create.side_effect = twilio_rest_exception
            check_phonenumber_verification(phone_number, code, user_id=user_id)

        mock_verification_checks_create.assert_called_once_with(
            to=phone_number, code=code
        )
        self.assertEqual(e_info.exception.error_message, error_message)
        self.assertIn(
            (
                f"(user_id={user_id}, twilio_error_code={twilio_code}, "
                f"status_code={status_code}, "
                f"handled_specifically={handled_specifically}, twilio_msg=A squirrel "
                "intercepted the message and replaced every S with Q.) Raising "
                f"{exception_class.__name__} from TwilioRestException "
                f"({twilio_rest_exception})."
            ),
            logs.output[-1],
        )
