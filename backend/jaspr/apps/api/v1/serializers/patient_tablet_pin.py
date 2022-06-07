import logging
logger = logging.getLogger(__name__)

from typing import Any,  Dict
from rest_framework import serializers
from .base import JasprBaseSerializer
from django.core.cache import cache
from jaspr.apps.clinics.models import Department, HealthcareSystem
from jaspr.apps.kiosk.models import Encounter, Technician


class PatientTabletPinSerializer(JasprBaseSerializer):
    department_code = serializers.CharField(required=False, max_length=255, allow_null=True)
    system_code = serializers.CharField(required=False, max_length=255, allow_null=True)
    pin_code = serializers.CharField(required=True, max_length=6, min_length=6)
    encounter = serializers.SerializerMethodField()
    technician = serializers.SerializerMethodField()
    technician_operated = serializers.SerializerMethodField()

    default_error_messages = {
        "code_mismatch": "The code entered is not valid",
        "missing_dept_system": "You must supply either a department_code or a system_code",
    }

    def get_encounter(self, obj):
        return obj.get("encounter")

    def get_technician(self, obj):
        return obj.get("technician")

    def get_technician_operated(self, obj):
        return obj.get("technician_operated")

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)

        if not data.get("department_code") and not data.get("system_code"):
            self.fail("missing_dept_system")

        if data.get("department_code"):
            try:
                department = Department.objects.get(tablet_department_code=data.get("department_code"))
            except Department.DoesNotExist:
                logger.warning(f"Pin validation failed with unknown department {data.get('department_code')}")
                self.fail("code_mismatch")
            cache_key = f"pin-code-department-{department.id}-{data.get('pin_code')}"
            pin_cache = cache.get(cache_key)
        elif data.get("system_code"):
            try:
                system = HealthcareSystem.objects.get(tablet_system_code=data.get("system_code"))
            except HealthcareSystem.DoesNotExist:
                logger.warning(f"Pin validation failed with unknown system {data.get('system_code')}")
                self.fail("code_mismatch")
            cache_key = f"pin-code-system-{system.pk}-{data.get('pin_code')}"
            pin_cache = cache.get(cache_key)

        if not pin_cache:
            self.fail("code_mismatch")

        encounter_id = pin_cache.get("encounter")
        technician_id = pin_cache.get("technician")
        technician_operated = pin_cache.get("technician_operated") or False

        if not encounter_id:
            logger.error("Pin validation failed due to missing encounter id")
            self.fail("code_mismatch")
        if not technician_id:
            logger.error("Pin validation failed due to missing technician id")
            self.fail("code_mismatch")

        try:
            encounter = Encounter.objects.get(pk=encounter_id)
        except Encounter.DoesNotExist:
            logger.error(f"Pin validation failed due to missing encounter with id {encounter_id}")
            self.fail("code_mismatch")

        try:
            technician = Technician.objects.get(pk=technician_id)
        except Technician.DoesNotExist:
            logger.error(f"Pin validation failed due to missing technician with id {technician_id}")
            self.fail("code_mismatch")

        data["encounter"] = encounter
        data["technician"] = technician
        data["technician_operated"] = technician_operated

        cache.delete(cache_key)

        return data

