from contextlib import contextmanager
from unittest.mock import NonCallableMagicMock, patch

from jaspr.apps.common.phonenumbers.verify import VERIFY_SERVICE_CONTEXT
from twilio.base.exceptions import TwilioRestException
from twilio.rest.api.v2010.account.message import MessageInstance
from twilio.rest.verify.v2.service.verification import VerificationInstance
from twilio.rest.verify.v2.service.verification_check import VerificationCheckInstance


class TwilioClientTestCaseMixin:
    """
    This mixin provides functionality for patching
    SMS message sending and verification creating/checking
    (so we don't actually have to make Twilio API calls).
    """

    twilio_rest_exception_instance = TwilioRestException(
        500,
        # NOTE: Example/made up SID/example URI, don't expect this to actually
        # work/make sense/be a valid URL.
        "https://api.twilio.com/Accounts/AC60edab5c3343b14c531e8cf123a6ff2a/Messages.json",
        msg="A squirrel intercepted the message and replaced every S with Q.",
        # Also, not a valid code and/or one we handle. Our code should still work fine
        # whether we recognize the `code` below or not.
        code=77755,
        method="POST",
    )

    @contextmanager
    def patched_twilio_client_messages_create(self):
        def patched_messages_create_success(*args, **kwargs) -> NonCallableMagicMock:
            mock = NonCallableMagicMock(spec_set=MessageInstance)
            mock.sid = "message-sid-success"
            return mock

        # NOTE: We are only patching in the place we expect
        # `twilio_client.messages.create` to be called from. With the way the code is
        # structured at the time of writing, `jaspr.apps.common.jobs.messaging` is
        # the only place `twilio_client.messages.create` should be getting called from.
        with patch(
            "jaspr.apps.common.jobs.messaging.twilio_client.messages.create",
            autospec=True,
            spec_set=True,
        ) as mock_create:
            mock_create.side_effect = patched_messages_create_success
            yield mock_create

    @contextmanager
    def patched_twilio_verifications_create(self):
        def patched_verifications_create_success(
            *args, **kwargs
        ) -> NonCallableMagicMock:
            mock = NonCallableMagicMock(spec_set=VerificationInstance)
            mock.sid = "verification-sid-success"
            return mock

        with patch.object(
            VERIFY_SERVICE_CONTEXT.verifications, "create", autospec=True, spec_set=True
        ) as mock_verifications_create:
            mock_verifications_create.side_effect = patched_verifications_create_success
            yield mock_verifications_create

    @contextmanager
    def patched_twilio_verification_checks_create(self, *, status: str = "approved"):
        def patched_verification_checks_create_success(
            *args, **kwargs
        ) -> NonCallableMagicMock:
            mock = NonCallableMagicMock(spec_set=VerificationCheckInstance)
            mock.sid = "verification-check-sid-success"
            mock.status = status
            return mock

        with patch.object(
            VERIFY_SERVICE_CONTEXT.verification_checks,
            "create",
            autospec=True,
            spec_set=True,
        ) as mock_verification_checks_create:
            mock_verification_checks_create.side_effect = (
                patched_verification_checks_create_success
            )
            yield mock_verification_checks_create
