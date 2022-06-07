from typing import Any,  Dict
from rest_framework import serializers
from .base import JasprBaseSerializer
from ..serializer_fields import (
    CurrentEncounterDefault
)
from jaspr.apps.kiosk.models import Encounter


class TechnicianTabletPinSerializer(JasprBaseSerializer):
    encounter = serializers.SerializerMethodField()
    technician_operated = serializers.BooleanField(default=False)
    encounter_context = serializers.HiddenField(default=CurrentEncounterDefault())

    default_error_messages = {
        "no_encounter": "Encounter must be specified when not in a patient context",
        "invalid_encounter": "The specified encounter is not valid",
        "invalid_encounter_pk": "encounter must be a positive integer"
    }

    def get_encounter(self, obj):
        if obj.get("encounter_context"):
            return obj.get("encounter_context")
        else:
            try:
                encounter_id = int(self.context["request"].data.get("encounter"))
            except (ValueError, TypeError):
                return None

            encounter = Encounter.objects.get(pk=encounter_id)
            return encounter

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)
        encounter_exists = data.get("encounter_context") or bool(self.context["request"].data.get("encounter"))
        if not encounter_exists:
            self.fail("no_encounter")

        if not data.get("encounter_context"):

            try:
                encounter_id = int(self.context["request"].data.get("encounter"))
            except (ValueError, TypeError):
                self.fail("invalid_encounter_pk")

            try:
                Encounter.objects.get(pk=encounter_id)
            except Encounter.DoesNotExist:
                self.fail("invalid_encounter")

        return data

    class Meta:
        fields = (
            "encounter",
            "technician_operated"
        )
