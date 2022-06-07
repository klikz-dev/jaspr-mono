from rest_framework import serializers
from jaspr.apps.clinics.models import Preferences


class PatientPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
        fields = [
            "timezone",
            "consent_language"
        ]
