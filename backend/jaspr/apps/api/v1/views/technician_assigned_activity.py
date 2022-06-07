import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from jaspr.apps.kiosk.models import Encounter, Technician, AssignedActivity, AssignmentLocks
from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from jaspr.apps.api.v1.serializers import AssignedActivitySerializer

from ..permissions import (
    IsAuthenticated,
    IsInER,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
    SharesClinic,
)

from .base import JasprBaseView

logger = logging.getLogger(__name__)


class SharesClinicWithPatient(SharesClinic):
    """ Technician shares clinic with Patient"""

    def get_patient(self, request, view, obj):
        encounter_id = view.kwargs.get("encounter_id")
        encounter = Encounter.objects.get(pk=encounter_id)
        return encounter.patient

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)


class TechnicianAssignedActivityView(JasprBaseView):
    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
        SharesClinicWithPatient,
    )

    @staticmethod
    def post(request: Request, encounter_id: int):
        csp = request.data.get('csp', False)
        csa = request.data.get("csa", False)
        skills = request.data.get('skills', False)
        encounter = Encounter.objects.get(pk=encounter_id)

        activities_to_add = []
        if skills:
            activities_to_add.append(ActivityType.ComfortAndSkills)
        if csa:
            activities_to_add.append(ActivityType.SuicideAssessment)
        if csp:
            activities_to_add.append(ActivityType.StabilityPlan)
        if activities_to_add:
            encounter.add_activities(activities_to_add)

        assigned_activity_serializer = AssignedActivitySerializer(encounter.filter_activities(explicit_only=True),
                                                                  many=True)
        result = assigned_activity_serializer.data
        count = 0
        for item in result:
            item["order"] = count
            count += 1

        return Response(result, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request, encounter_id: int, activity_id: int):
        locked = request.data.get('locked', False)
        activity = AssignedActivity.objects.get(pk=activity_id)
        if 'locked' in request.data:
            if locked:
                activity.lock()
            else:
                activity.unlock()

        result = AssignedActivitySerializer(activity).data

        return Response(result, status=status.HTTP_200_OK)

    @staticmethod
    def get(request, encounter_id: int):
        encounter = Encounter.objects.get(pk=encounter_id)
        assigned_activity_serializer = AssignedActivitySerializer(encounter.get_explicit_activities(),
                                                                  many=True)
        result = assigned_activity_serializer.data
        count = 0
        for item in result:
            item["order"] = count
            count += 1
        return Response(assigned_activity_serializer.data, status=status.HTTP_200_OK)
