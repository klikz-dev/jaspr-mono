from rest_framework import serializers
from jaspr.apps.api.v1.helpers import zulu_time_format

from typing import Any, Dict

from ..serializer_fields import (
    ContextDefault,
    CurrentTechnicianDefault,
)

from jaspr.apps.kiosk.models import (
    ProviderComment
)


class ProviderCommentSerializer(serializers.ModelSerializer):
    encounter = serializers.HiddenField(default=ContextDefault("encounter"))
    technician = serializers.HiddenField(default=CurrentTechnicianDefault())
    created = serializers.SerializerMethodField()
    modified = serializers.SerializerMethodField()

    def get_created(self, obj: ProviderComment):
        return zulu_time_format(obj.created)

    def get_modified(self, obj: ProviderComment):
        return zulu_time_format(obj.created)

    def to_representation(self, obj: ProviderComment) -> Dict[str, Any]:
        can_edit = self.context["request"].user.technician.pk == obj.technician_id

        return {
            **super().to_representation(obj),
            "technician": {
                "id": obj.technician_id,
                "email": obj.technician.user.email,
                "can_edit": can_edit,
            },
        }

    class Meta:
        model = ProviderComment
        fields = [
            "id",
            "answer_key",
            "encounter",
            "technician",
            "comment",
            "created",
            "modified",
        ]
        read_only_fields = ["created", "modified", "technician"]
