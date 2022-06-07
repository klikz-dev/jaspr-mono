import logging
from jaspr.apps.api.v1.helpers import zulu_time_format

from rest_framework import status, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from jaspr.apps.kiosk.models import ProviderComment, Encounter

from ..permissions import (
    HasRecentHeartbeat,
    IsAuthenticated,
    IsTechnician,
    IsInER,
    SatisfiesClinicIPWhitelistingFromTechnician,
    SharesClinic
)
from ..serializers import (
    ProviderCommentSerializer,
)
from .jaspr_base import JasprBaseViewSetMixin

logger = logging.getLogger(__name__)



class TechnicianPatientProviderCommentViewSet(
    JasprBaseViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """

    GET /v1/technician/encounter/:encounter_id/provider-comments

    returns:
    """


    class PatientSharesClinic(SharesClinic):
        """
        Override `SharesClinic` to set the `patient` from this `ViewSet`
        (since it's not `obj` which is the default).
        """

        def get_patient(self, request, view, obj):
            encounter_id = view.kwargs.get("encounter_id")
            encounter = Encounter.objects.get(pk=encounter_id)
            return encounter.patient

        def has_permission(self, request, view):
            return self.has_object_permission(request, view, None)


    queryset = (
        ProviderComment.objects.filter(status="active")
            .select_related("technician__user")
            .order_by("-created")
    )
    serializer_class = ProviderCommentSerializer
    lookup_url_kwarg = "provider_comment_id"

    # TODO JACOB Make sure we have correct permissions
    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
        PatientSharesClinic,
    )

    def get_serializer_context(self, *args, **kwargs):
        encounter_id = self.kwargs.get("encounter_id")
        encounter = Encounter.objects.get(pk=encounter_id)
        return {**super().get_serializer_context(), "encounter": encounter}

    def list(self, request, *args, **kwargs):
        encounter_id = self.kwargs.get("encounter_id")

        provider_comments = ProviderComment.objects.filter(encounter__pk=encounter_id)\
            .select_related('technician', 'technician__user').order_by("created").all()


        comment_dict = {}
        for provider_comment in provider_comments:
            data = {
                "id": provider_comment.pk,
                "answer_key": provider_comment.answer_key,
                "technician": {
                    "id": provider_comment.technician.pk,
                    "first_name": getattr(request.user.technician, "first_name", ""),
                    "last_name": getattr(request.user.technician, "last_name", ""),
                    "email": provider_comment.technician.user.email,
                    "can_edit": provider_comment.technician == request.user.technician
                },
                "comment": provider_comment.comment,
                "created": zulu_time_format(provider_comment.created),
                "modified": zulu_time_format(provider_comment.modified)
            }

            if provider_comment.answer_key not in comment_dict:
                comment_dict[provider_comment.answer_key] = [data]
            else:
                comment_dict[provider_comment.answer_key].append(data)

        return Response(comment_dict)

