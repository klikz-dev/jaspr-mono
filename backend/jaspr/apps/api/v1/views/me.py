import logging

from rest_condition import And, Or

from rest_framework.response import Response

from .base import JasprBaseView

from ..permissions import (
    HasRecentHeartbeat,
    IsAuthenticated,
    IsInER,
    IsPatient,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from ..serializers import (
    MePatientSerializer,
    MeTechnicianSerializer
)

logger = logging.getLogger(__name__)


class MeView(JasprBaseView):
    permission_classes = (
        IsAuthenticated,
        Or(
            And(IsPatient, HasRecentHeartbeat),
            And(
                IsTechnician,
                IsInER,
                SatisfiesClinicIPWhitelistingFromTechnician,
            ),
        ),
    )

    def get_serializer_class(self):
        # NOTE: Just using `hasattr` here because `permission_classes` above will
        # handle the `is_patient` check at the time of writing.
        if hasattr(self.request.user, "patient"):
            return MePatientSerializer
        # Currently really not used or needed, here as a stub.
        if hasattr(self.request.user, "technician"):
            return MeTechnicianSerializer

    def get_instance(self):
        # NOTE: Just using `hasattr` here because `permission_classes` above will
        # handle the `is_patient` check at the time of writing.
        if hasattr(self.request.user, "patient"):
            return self.request.user.patient
        # Currently really not used or needed, here as a stub.
        if hasattr(self.request.user, "technician"):
            return self.request.user.technician

    def get(self, request):
        """The list endpoint is overridden to just return one interview record. Like me endpoint."""
        serializer = self.get_serializer_class()(
            self.get_instance(), context=self.get_serializer_context()
        )
        return Response(serializer.data)

    def patch(self, request):
        serializer = self.get_serializer_class()(
            self.get_instance(),
            data=request.data,
            context=self.get_serializer_context(),
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
