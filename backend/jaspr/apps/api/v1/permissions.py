import datetime
import logging
import operator
from typing import ClassVar, Sequence, Type

from django.utils import timezone
from ipware import get_client_ip
from rest_framework import permissions

from jaspr.apps.clinics.models import Clinic
from jaspr.apps.kiosk.models import Encounter, Patient
from jaspr.apps.kiosk.tokens import (
    JasprExtraSecurityTokenGenerator,
    JasprSetPasswordTokenGenerator,
)

logger = logging.getLogger(__name__)


class IsAuthenticated(permissions.IsAuthenticated):
    """ See https://github.com/caxap/rest_condition/issues/12  -- we got rid of restcondition, leaving this in place for now"""

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsTechnician(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_technician and hasattr(request.user, "technician")


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_patient and hasattr(request.user, "patient")


class IsInER(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.auth.jaspr_session.in_er is True


class IsNotInER(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.auth.jaspr_session.in_er is False


class HasAccessAssessmentObj(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.patient.pk == obj.encounter.patient_id


class SharesClinic(permissions.BasePermission):
    """ Technician shares clinic with Patient"""

    def get_patient(self, request, view, obj):
        return obj

    def has_object_permission(self, request, view, obj):
        technician = request.user.technician
        available_department_ids = technician.departmenttechnician_set.filter(
            status="active"
        ).values_list("department_id", flat=True)

        patient = self.get_patient(request, view, obj)

        if patient:
            sharing_depts = patient.patientdepartmentsharing_set.all()
            for dept_id in available_department_ids:
                for sharing_dept in sharing_depts:
                    if dept_id == sharing_dept.department_id:
                        return True

        return False


class SatisfiesClinicIPWhitelisting(permissions.BasePermission):
    """
    This is an abstract permission that is meant to be subclassed, and you should
    use the subclass. For example, use one of:
    - `SatisfiesClinicLocationIPWhitelistingFromTechnician`
    - `SatisfiesClinicLocationIPWhitelistingFromPatient`

    As for the actual permissions check, here's the big picture flow:
    - If the `ClinicLocation` has no whitelisted IP addresses or ranges specified,
    then we assume that the requesting user (I.E. `Technician` or `Patient` at the
    time of writing) has permission.
    - Otherwise, if the `ClinicLocation` has any whitelisting (address(es), range(s),
    or any combination of the two), then we check the requesting user's IP address
    against those whitelist and only permit if contained in some whitelist entry.
    - One subtlety is that if we cannot find the requesting user's IP address, and
    there is a whitelist of some sort, we do not permit the request to continue and
    log a warning.
    """

    def get_clinics(
        self, request, view
    ) -> Sequence[Clinic]:  # pragma: no cover
        raise NotImplementedError("Subclasses must define this method.")

    def has_permission(self, request, view):
        clinics = self.get_clinics(request, view)
        # NOTE: If all the `Technician` records (the example right now) are set up
        # properly, this should not happen.
        if not clinics:
            logger.warning(
                "(permission=%s, request=%s, view=%s) No departments returned.",
                str(self),
                str(request),
                str(view),
            )
            return False
        locations_with_whitelisting = [
            location for location in clinics if location.has_ip_whitelisting
        ]
        if not locations_with_whitelisting:
            return True
        client_ip = get_client_ip(request)[0]
        if client_ip is None:
            logger.warning(
                "(permission=%s, request=%s, view=%s) Couldn't get client's IP Address.",
                str(self),
                str(request),
                str(view),
            )
            return False
        for location in locations_with_whitelisting:
            if location.ip_satisfies_whitelisting(client_ip):
                return True
        return False


class SatisfiesClinicIPWhitelistingFromTechnician(
    SatisfiesClinicIPWhitelisting
):
    def get_clinics(self, request, view) -> Sequence[Clinic]:

        return list(
            map(
                operator.attrgetter("department.clinic"),
                request.user.technician.departmenttechnician_set.filter(
                    status="active"
                ).select_related("department").select_related("department__clinic"),
            )
        )


class SatisfiesClinicIPWhitelistingFromPatient(
    SatisfiesClinicIPWhitelisting
):
    def get_clinics(self, request, view) -> Sequence[Clinic]:
        encounter = request.user.patient.current_encounter
        return [encounter.department.clinic]


class HasRecentHeartbeat(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Verifies that `last_heartbeat` is within 10 minutes of now (or `None`) and
        sets a new `last_heartbeat`, but only if `session_lock is False`.

        NOTE: `HasRecentHeartbeat` is only in effect in the Emergency Room at this
        time.
        """
        # NOTE: At the time of writing, all views/viewsets that use this permission
        # require `JasprTokenAuthentication`, which means we're guaranteed to have
        # `request.auth` present with an `AuthToken` instance.

        if not request.auth.jaspr_session.in_er:
            return True

        encounter = request.auth.jaspr_session.encounter
        if not encounter:
            return False

        last_heartbeat = encounter.last_heartbeat
        ten_minutes = datetime.timedelta(minutes=10)
        now = timezone.now()

        # Note: when a patient hits an api for the first time,
        # last_heartbeat is None, so this is an ok state.
        # We also need to respect session_lock = True,
        # and not update heartbeats in that case.

        if not encounter.session_lock and (
            (last_heartbeat is None) or (now - last_heartbeat) <= ten_minutes
        ):

            # updating because of pass-by-reference (just in case)
            encounter.last_heartbeat = now

            # update last_heartbeat without causing a simple history record.
            Encounter.objects.filter(pk=encounter.pk).update(last_heartbeat=now)
            return True
        return False


class TokenGeneratorPermission(permissions.BasePermission):
    """
    Base permission class intended for subclassing and specifying the relevant
    `token_generator` to check the token against.
    """

    token_generator: Type[JasprExtraSecurityTokenGenerator]
    token_data_key: ClassVar[str] = "token"

    def has_permission(self, request, view):
        user = request.user
        token = request.data.get(self.token_data_key)
        return self.token_generator().check_token(user, token)


class HasValidJasprSetPasswordToken(TokenGeneratorPermission):
    token_generator = JasprSetPasswordTokenGenerator
    token_data_key: ClassVar[str] = "set_password_token"


class HasToolsToGoStartedButNotFinished(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.patient.tools_to_go_status in (
            Patient.TOOLS_TO_GO_EMAIL_SENT,
            Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
        )


class HasToolsToGoAtLeastPhoneNumberVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.patient.tools_to_go_status in (
            Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
            Patient.TOOLS_TO_GO_SETUP_FINISHED,
        )


class HasToolsToGoSetupFinished(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.patient.tools_to_go_status
            == Patient.TOOLS_TO_GO_SETUP_FINISHED
        )
