import logging

from rest_framework import status
from rest_framework.response import Response

from ..permissions import (
    HasRecentHeartbeat,
    IsNotInER,
)

from .base import JasprBaseView

from ..permissions import (
    IsAuthenticated,
    IsPatient,
)

from jaspr.apps.jah.models import CrisisStabilityPlan, JAHAccount

logger = logging.getLogger(__name__)


class JahCrisisStabilityPlanView(JasprBaseView):
    """Expose the JAH Copy of the Crisis Stability Plan for viewing and editing.

    GET /v1/patient/crisis-stability-plan

    return:
        {
            "reasonsLive": [],
            "strategiesGeneral": [],
            "strategiesFirearm": [],
            "strategiesMedicine": [],
            "strategiesPlaces": [],
            "strategiesOther": [],
            "strategiesCustom": [],
            "meansSupportYesNo": null,
            "meansSupportWho": null,
            "copingBody": [],
            "copingDistract": [],
            "copingHelpOthers": [],
            "copingCourage": [],
            "copingSenses": [],
            "supportivePeople": [
                {
                    "name": "",
                    "phone": ""
                }
            ],
            "copingTop": [],
            "wsStressors": [],
            "wsThoughts": [],
            "wsFeelings": [],
            "wsActions": [],
            "wsTop": []
        }
    """

    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat, IsNotInER)

    def get(self, request):
        patient = self.request.user.patient
        try:
            jah_account = patient.jahaccount
            crisis_stability_plan = jah_account.crisisstabilityplan
        except (JAHAccount.DoesNotExist, CrisisStabilityPlan.DoesNotExist):
            logger.error(f"JAH Patient {patient.pk} incorrectly configured")
            return Response({"non_field_errors": "JAH User incorrectly configured"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = crisis_stability_plan.get_serializer()(
            crisis_stability_plan,
            context=self.get_serializer_context(),
        )
        return Response(serializer.data)

    def patch(self, request):
        patient = self.request.user.patient
        jah_account = patient.jahaccount
        crisis_stability_plan = jah_account.crisisstabilityplan

        crisis_stability_plan_serializer = crisis_stability_plan.get_serializer()(
            crisis_stability_plan,
            data=request.data,
            context=self.get_serializer_context(),
        )

        crisis_stability_plan_serializer.is_valid(raise_exception=True)
        crisis_stability_plan_serializer.save()

        return Response(crisis_stability_plan_serializer.data)



