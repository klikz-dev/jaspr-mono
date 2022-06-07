from rest_framework import mixins, permissions, status, viewsets
from django.db.models import Prefetch

from .jaspr_base import JasprBaseViewSetMixin
from jaspr.apps.api.v1.permissions import (
    IsPatient,
)
from jaspr.apps.api.v1.serializers import (
    ReadOnlyActivitySerializer,
)
from jaspr.apps.kiosk.models import (
    PatientActivity,
    Activity
)
from jaspr.apps.api.v1.permissions import HasRecentHeartbeat, IsAuthenticated


class ActivityViewSet(JasprBaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    Viewset for allowing Patients to view their activity
    alongside any data associated with those activities.
    """

    # NOTE: `get_queryset` below uses this as a base, and then does
    # a `prefetch_related` on it to retrieve possibly present
    # `PatientActivity` instances corresponding to the activities.
    queryset = Activity.objects.filter(status="active").select_related('video').prefetch_related('video__tags')
    serializer_class = ReadOnlyActivitySerializer
    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat)

    @staticmethod
    def queryset_for_patient_user(base_queryset, user):
        return base_queryset.prefetch_related(
            Prefetch(
                "patientactivity_set",
                queryset=PatientActivity.objects.filter(patient__user=user),
                to_attr="patient_activities",
            )
        )

    def get_queryset(self):
        return self.queryset_for_patient_user(super().get_queryset(), self.request.user)

