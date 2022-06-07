import logging

from rest_framework.response import Response

from ....stability_plan.models import PatientWalkthrough, PatientWalkthroughStep
from ....stability_plan.walkthrough_manager import WalkthroughManager
from ..permissions import (
    HasRecentHeartbeat,
    IsNotInER,
)
from ..serializers import (
    ReadOnlyPatientWalkthroughStepSerializer,
)

from .base import JasprBaseView

from ..permissions import (
    IsAuthenticated,
    IsPatient,
)

logger = logging.getLogger(__name__)


class PatientWalkthroughView(JasprBaseView):
    """Expose a list of step data ordered by PatientWalkthrough and the related Walkthrough row.
        Step data consists of the most recent content
        for each step included in associated Walkthrough and a given Patient.

    GET /v1/patient/walkthrough

    returns:
        [
            {stepName: "PLE Video>, frontendRenderType: "videoDescription", value: <serialized Media object: name="Welcome Video", description="Welcmoe video descripotion here">},
            {stepName: "Comfort & Skills", frontendRenderType: "video", value: <serialized Media object: name="Puppies">},
            {stepName: "Paced Breathing", frontendRenderType: "breathe", value: null},
            {stepName: "Message from your Virtual Guide", frontendRenderType: "guide", value: {"message": "Message text from your guide"}},
            {stepName: "Physical Coping Strategy", frontendRenderType: copingStrategy, value: {"image": "https://....", "title": "Go for a walk"},
            {stepName: "Coping Skill", frontendRenderType: copingStrategy, value: {"image": "https://....", "title": "Go for a walk"},
            {stepName:  “Reasons for Living”, "frontendRenderType": "reasonsForLiving", value: null},
            {stepName:  “My Steps to Make Home Safer”, "frontendRenderType": "lethalMeans", value: null},
            {stepName:  “Make Home Safer”, "frontendRenderType": "videoDescription", value: {serialized Media object},
            {stepName:  “National Hotline”, "frontendRenderType": "nationalHotline", value: {name="National Hotline", phone="206 555 1232", text="206 234 2345"}},
            {stepName: “Recap”, frontendRenderType: "recap", value: null}
        ]"""

    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat, IsNotInER)

    def get(self, request):
        patient = self.request.user.patient

        patient_walkthrough = PatientWalkthrough.objects.filter(
            status="active",
            patient=patient,
        )

        if not patient_walkthrough:
            WalkthroughManager(patient).handle()

        patient_walkthrough_steps = PatientWalkthroughStep.objects.filter(
            status="active",
            patient_walkthrough__status="active",
            patient_walkthrough__patient=patient,
        )

        if patient_walkthrough_steps:
            serializer = ReadOnlyPatientWalkthroughStepSerializer(
                patient_walkthrough_steps,
                context=self.get_serializer_context(),
                many=True,
            )
            return Response(serializer.data)
        return Response([])
