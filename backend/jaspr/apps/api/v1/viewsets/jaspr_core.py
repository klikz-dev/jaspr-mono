from rest_framework import mixins, permissions, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .jaspr_base import JasprBaseViewSetMixin
from jaspr.apps.api.v1.permissions import (
    IsInER,
    IsPatient,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromPatient,
    SatisfiesClinicIPWhitelistingFromTechnician,
    SharesClinic,
)
from jaspr.apps.api.v1.serializers import (
    AmendmentSerializer,
    DepartmentSerializer,
    CommonConcernSerializer,
    ConversationStarterSerializer,
    MediaSerializer,
    PatientActivitySerializer,
    PatientSerializer,
    PatientVideoSerializer,
    ReadOnlyActivitySerializer,
    ReadOnlyCopingStrategySerializer,
    ReadOnlySharedStorySerializer,
)
from jaspr.apps.api.v1.filters import (
    DepartmentFilterBackend,
    JasprMediaFilterBackend,
    PatientOwnerFilterBackend,
)
from jaspr.apps.kiosk.models import (
    Activity,
    Amendment,
    CopingStrategy,
    Patient,
    PatientActivity,
    PatientVideo,
    SharedStory,
)
from jaspr.apps.clinics.models import Department
from jaspr.apps.awsmedia.models import Media
from jaspr.apps.jah.models import CommonConcern, ConversationStarter
from jaspr.apps.api.v1.permissions import HasRecentHeartbeat, IsAuthenticated


class ConversationStarterViewSet(JasprBaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    Viewset for allowing Patients to
    list and retrieve Conversation Starters.

    GET: /v1/conversation-starters
    """

    queryset = ConversationStarter.objects.filter(status="active")
    serializer_class = ConversationStarterSerializer
    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat)


class CommonConcernViewSet(JasprBaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    Viewset for allowing Patients to
    list and retrieve Common Concerns.

    GET: /v1/common-concerns
    """

    queryset = CommonConcern.objects.filter(status="active")
    serializer_class = CommonConcernSerializer
    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat)


class JasprMediaViewSet(JasprBaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    Viewset for allowing Patients to
    list and retrieve Jaspr video files.
    """

    queryset = Media.objects.all().prefetch_related("tags")
    serializer_class = MediaSerializer
    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat)
    filter_backends = (JasprMediaFilterBackend,)


class SharedStoryViewSet(JasprBaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """
    Viewset for allowing Patients to view shared stories.
    """

    queryset = (
        SharedStory.objects.filter(status="active")
        .select_related("person", "topic", "video")
        .prefetch_related("video__tags")
        .order_by("order")
    )
    serializer_class = ReadOnlySharedStorySerializer
    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat)


class PatientActivityViewSet(
    JasprBaseViewSetMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset for allowing Patients to read and modify their activity data.
    """

    queryset = PatientActivity.objects.filter(status="active")
    serializer_class = PatientActivitySerializer
    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat)
    filter_backends = (PatientOwnerFilterBackend,)


class PatientVideoViewSet(
    JasprBaseViewSetMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset for allowing Patients to view and update
    their data associated with videos (`JasprMedia(file_type='video')`).
    """

    queryset = PatientVideo.objects.all()
    serializer_class = PatientVideoSerializer
    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat)
    filter_backends = (PatientOwnerFilterBackend,)


class DepartmentViewSet(
    JasprBaseViewSetMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    Viewset for allowing Technicians to view their available Clinic Locations.
    """

    queryset = Department.objects.filter(status="active")
    serializer_class = DepartmentSerializer
    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
    )
    filter_backends = (DepartmentFilterBackend,)


class CopingStrategyViewSet(JasprBaseViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """Viewset to allow Patients to view coping strategies with an optional filter on category.

    GET

    /v1/coping-strategies/

    optional:
        /v1/coping-strategies/?slug__name=physical

        [
            {
                "id": 1,
                "title": "Go For a Walk",
                "image": "https://image/path.png",
                "frontendKey": "walk",
                "category": {
                    id: 1, "name": "physical", "why_text": "This is the why behind going for a walk"
                }
            },
        ]

    """

    queryset = CopingStrategy.objects.filter(status="active").select_related(
        "category",
    )
    serializer_class = ReadOnlyCopingStrategySerializer
    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "category__slug",
    ]