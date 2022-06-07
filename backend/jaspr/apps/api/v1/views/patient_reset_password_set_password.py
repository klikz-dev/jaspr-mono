import logging

from ..permissions import (
    HasToolsToGoSetupFinished,
    HasValidJasprSetPasswordToken,
    IsAuthenticated,
    IsPatient,
)
from jaspr.apps.kiosk.authentication import (
    JasprResetPasswordUidAndTokenAuthentication,
)
from .patient_set_password import PatientSetPasswordView

logger = logging.getLogger(__name__)


class PatientResetPasswordSetPasswordView(PatientSetPasswordView):
    authentication_classes = (JasprResetPasswordUidAndTokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        IsPatient,
        HasToolsToGoSetupFinished,
        HasValidJasprSetPasswordToken,
    )
