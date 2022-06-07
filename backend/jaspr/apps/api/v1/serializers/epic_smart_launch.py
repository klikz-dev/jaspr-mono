from typing import Any,  Dict
from rest_framework import serializers
from .base import JasprBaseSerializer



class EpicSmartLaunchSerializer(JasprBaseSerializer):
    access_token = serializers.CharField(required=True)
    token_type = serializers.CharField(required=False)
    expires_in = serializers.IntegerField(required=True)
    scope = serializers.CharField(required=False)
    state = serializers.CharField(required=True)
    csn = serializers.CharField(required=False)
    dept_id = serializers.CharField(required=True)
    dob = serializers.CharField(required=True)
    encounter = serializers.CharField(required=True)
    encounter_date = serializers.CharField(required=True)
    location = serializers.CharField(required=False)
    mrn = serializers.CharField(required=True)
    need_patient_banner = serializers.BooleanField(required=False)
    patient = serializers.CharField(required=False) # Identical to patient_fhir_id
    patient_fhir_id = serializers.CharField(required=True)
    patient_first_name = serializers.CharField(required=True)
    patient_last_name = serializers.CharField(required=True)
    practitioner_fhir_id = serializers.CharField(required=True)
    practitioner_first_name = serializers.CharField(required=True)
    practitioner_last_name = serializers.CharField(required=True)
    service_area = serializers.CharField(required=False)
    smart_style_url = serializers.CharField(required=False)
