import logging

from rest_framework.response import Response
from rest_framework import status

from .base import JasprBaseView
from jaspr.apps.kiosk.models import (
    Patient,
    Technician
)
from ..serializers import (
    ResetPasswordSerializer,
)
from jaspr.apps.kiosk.emails import (
    send_reset_password_email,
    send_technician_activation_email,
    send_tools_to_go_setup_email,
)

logger = logging.getLogger(__name__)


class ResetPasswordView(JasprBaseView):
    """
    View that receives an `email` and performs the following steps:

    1. If the `User` is a `Patient`:
        a. If the `User` doesn't exist corresponding to that email, or the `User` exists
        but there isn't a `Patient`, or there's a `Patient` but the
        `Patient` has `tools_to_go_status` set to "Not Started" (I.E. they haven't
        put in a phone number or email in the ER) don't do anything and just return a 204.
        b. If the `User` exists and has a `Patient`, and the `Patient` hasn't
        finished setting up tools to go, send the tools to go setup email and return a
        204.
        c. If the `User` exists and has a `Patient`, and the `Patient` has
        finished setting up tools to go, send the reset password email and return a 204.

    2. If the `User` is a `Technician`:
        a. If the `User` doesn't exist corresponding to that email, or the `User`
        exists but there isn't a `Technician`, don't do anything and just return a
        204.
        b. If the `User` exists and has a `Technician`, and the `Technician` hasn't
        been activated yet, send the `Technician` activation email and return a 204.
        c. If the `User` exists and has a `Technician`, and the `Technician` has been
        activated, send the reset password email and return a 204.
    """

    authentication_classes = ()
    permission_classes = ()

    def send_patient_email(self, patient):

        if patient.tools_to_go_status in (
                Patient.TOOLS_TO_GO_EMAIL_SENT,
                Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
        ):
            send_tools_to_go_setup_email(patient.user)

        if patient.tools_to_go_status == Patient.TOOLS_TO_GO_SETUP_FINISHED:
            send_reset_password_email(patient.user)

    def send_technician_email(self, technician):
        if technician.activated:
            send_reset_password_email(technician.user)
        else:
            send_technician_activation_email(technician)

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        if (
                patient := Patient.objects.select_related("user")
                        .filter(user__email__iexact=email)
                        .first()
        ):
            self.send_patient_email(patient)

        elif (
                technician := Technician.objects.select_related("user")
                        .filter(user__email__iexact=email)
                        .first()
        ):
            self.send_technician_email(technician)

        return Response(status=status.HTTP_204_NO_CONTENT)