from rest_framework import serializers

from jaspr.apps.common.models import CrisisStabilityPlanBaseModel


class SupportivePersonSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length=CrisisStabilityPlanBaseModel.SUPPORTIVE_PERSON_NAME_MAX_LENGTH,
        allow_blank=True,
    )
    phone = serializers.CharField(
        max_length=CrisisStabilityPlanBaseModel.SUPPORTIVE_PERSON_PHONE_MAX_LENGTH,
        allow_blank=True,
    )

    default_error_messages = {
        "not_all_blank": "Must provide at least one of name or phone number."
    }

    def validate(self, attrs: dict) -> dict:
        if not (attrs.get("name") or attrs.get("phone")):
            self.fail("not_all_blank")
        return attrs
