from rest_framework import serializers
from jaspr.apps.clinics.models import Preferences


class PreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
        fields = [
            "timezone",
            "provider_notes",
            "stability_plan_label",
        ]
