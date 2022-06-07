import logging

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions

from .base import JasprBaseView

from jaspr.apps.clinics.models import Department, Clinic, HealthcareSystem, GlobalPreferences

from ..permissions import (
    IsAuthenticated,
    IsInER,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from ..serializers import (
    PreferencesSerializer
)

logger = logging.getLogger(__name__)


class PreferencesView(JasprBaseView):
    serializer_class = PreferencesSerializer

    class TechnicianBelongs(permissions.BasePermission):
        def has_permission(self, request, view):
            technician = request.user.technician
            department = request.GET.get('department')
            clinic = request.GET.get('clinic')
            system = request.GET.get('system')

            if department:
                department = Department.objects.get(pk=department)
                try:
                    return department.has_technician(technician)
                except Department.DoesNotExist:
                    return False
            elif clinic:
                clinic = Clinic.objects.get(pk=clinic)
                try:
                    return clinic.has_technician(technician)
                except Clinic.DoesNotExist:
                    return False
            elif system:
                system = HealthcareSystem.objects.get(pk=system)
                try:
                    return system.has_technician(technician)
                except HealthcareSystem.DoesNotExist:
                    return False

            # Otherwise we check the encounter which has already been validated to belong to the technician
            # Or we check the global permissions which should be available to all users
            return True



    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
        TechnicianBelongs,
    )

    def get_instance(self):
        department = self.request.GET.get('department')
        clinic = self.request.GET.get('clinic')
        system = self.request.GET.get('system')
        if department:
            return Department.objects.get(pk=department).get_preferences()
        elif clinic:
            return Clinic.objects.get(pk=clinic).get_preferences()
        elif system:
            return HealthcareSystem.objects.get(pk=system).get_preferences()
        elif self.request.auth.jaspr_session.encounter:
            return self.request.auth.jaspr_session.encounter.department.get_preferences()
        return GlobalPreferences.objects.get(pk="global_preferences")


    def get(self, request):
        """The list endpoint is overridden to just return one interview record. Like me endpoint."""
        serializer = PreferencesSerializer(
            self.get_instance(), context=self.get_serializer_context()
        )
        return Response(serializer.data)

