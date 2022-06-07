from rest_framework import serializers
from typing import Dict, Optional
from jaspr.apps.api.v1.helpers import zulu_time_format
from jaspr.apps.kiosk.models import (
    AssignedActivity,
)


class AssignedActivitySerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    metadata = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    status_updated = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    progress_bar_label = serializers.SerializerMethodField()

    @staticmethod
    def get_type(activity: AssignedActivity) -> str:
        return str(activity.type)

    @staticmethod
    def get_metadata(activity: AssignedActivity) -> Dict:
        return activity.get_metadata() or {}

    @staticmethod
    def get_created(activity: AssignedActivity) -> str:
        return zulu_time_format(activity.created)

    @staticmethod
    def get_start_time(activity: AssignedActivity) -> Optional[str]:
        if activity.start_time:
            return zulu_time_format(activity.start_time)
        return None

    @staticmethod
    def get_status(activity: AssignedActivity) -> str:
        return str(activity.get_status())

    @staticmethod
    def get_status_updated(activity: AssignedActivity) -> Optional[str]:
        if activity.get_status_updated():
            return zulu_time_format(activity.get_status_updated())
        return None

    @staticmethod
    def get_questions(activity: AssignedActivity) -> Dict:
        return activity.get_questions()

    @staticmethod
    def get_progress_bar_label(activity: AssignedActivity):
        return activity.get_progress_bar_label()

    class Meta:
        model = AssignedActivity
        fields = [
            "id",
            "created",
            "start_time",
            "status",
            "status_updated",
            "locked",
            "type",
            "metadata",
            "questions",
            "progress_bar_label",
        ]
        read_only_fields = [
            "id",
            "created",
            "start_time",
            "status",
            "status_updated",
            "locked",
            "type",
            "metadata",
            "questions",
            "progress_bar_label"
        ]
