import logging

from ..permissions import (
    HasToolsToGoSetupFinished,
    IsAuthenticated,
    IsPatient,
)
from jaspr.apps.kiosk.authentication import (
    JasprResetPasswordUidAndTokenAuthentication,
)
from .patient_check_phone_number_code import PatientCheckPhoneNumberCodeView

logger = logging.getLogger(__name__)


class PatientResetPasswordCheckPhoneNumberCodeView(PatientCheckPhoneNumberCodeView):
    """
    Endpoint for verifying the phone number, but for reset password instead of
    tools to go setup/activation. Reason for the separate endpoint is different
    permissions for now (and maybe possibility of different logic in the future;
    no current plans for that but this leaves things open) alongside a different
    token generator in the first place.
    """

    authentication_classes = (JasprResetPasswordUidAndTokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPatient, HasToolsToGoSetupFinished)