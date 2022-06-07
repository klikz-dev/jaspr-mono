from rest_framework import mixins, permissions, status, viewsets
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from rest_framework.viewsets import GenericViewSet

from .jaspr_base import JasprBaseViewSetMixin
from jaspr.apps.api.v1.permissions import (
    IsInER,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
    SharesClinic,
)
from jaspr.apps.api.v1.serializers import (
    AmendmentSerializer,
)
from jaspr.apps.kiosk.models import (
    Amendment,
    Encounter,
)
from jaspr.apps.api.v1.permissions import IsAuthenticated


class TechnicianPatientAmendmentViewSet(
    JasprBaseViewSetMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    /v1/technician/patients/{patient_id}/amendments

    GET

        {
            "id": 1,
            "comment": "John",
            "created": "2020-06-22T15:09:21.048000-05:00",
            "modified": "2020-06-22T15:11:23.034000-05:00",
            "noteType": "stability-plan",
            "technician": {
                "id": 12,
                "email": "techyyy@example.jasprhealth.com",
                "can_edit": true
            }
        }

    POST

        {
            "noteType": "narrative-note",
            "comment": "Here is an amendment note."
        }

    /v1/technician/patients/{patient_id}/amendments/{amendment_id}

    PUT

        {
            "noteType": "narrative-note",
            "comment": "Here is an updated amendment note."
        }

    """

    class PatientForAmendmentSharesClinic(SharesClinic):
        """
        Override `SharesClinic` to set the `patient` from this `ViewSet`
        (since it's not `obj` which is the default).
        """

        def get_patient(self, request, view, obj):
            return view.encounter.patient

        def has_permission(self, request, view):
            # The `Amendment` does not matter at all for this permission, so setting
            # `obj` to `None` works fine (note that `get_patient` above doesn't use
            # `obj`).
            return self.has_object_permission(request, view, None)

    class TechnicianPermittedToEditAmendment(permissions.BasePermission):
        """
        The `Technician` is permitted to edit the `Amendment` if the `Technician` is
        the one that created the `Amendment`.
        """

        def has_object_permission(self, request, view, obj):
            technician = request.user.technician
            return (
                request.method not in permissions.SAFE_METHODS
                and obj.technician_id == technician.id
            )

    queryset = (
        Amendment.objects.filter(status="active")
        .select_related("technician__user")
        .order_by("-created")
    )
    serializer_class = AmendmentSerializer
    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        PatientForAmendmentSharesClinic,
        SatisfiesClinicIPWhitelistingFromTechnician,
        TechnicianPermittedToEditAmendment,
    )
    lookup_url_kwarg = "amendment_id"

    @cached_property
    def encounter(self):
        assert "encounter_id" in self.kwargs, "`encounter_id` should be in the URL."
        encounter_id = self.kwargs["encounter_id"]
        return get_object_or_404(Encounter, id=encounter_id)

    def get_serializer_context(self):
        return {**super().get_serializer_context(), "encounter": self.encounter}

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).filter(encounter=self.encounter)

    def perform_destroy(self, instance: Amendment):
        instance.status = "deleted"
        instance.save()