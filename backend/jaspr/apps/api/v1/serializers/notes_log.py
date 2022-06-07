from rest_framework import serializers
from jaspr.apps.api.v1.helpers import zulu_time_format

from .base import JasprBaseModelSerializer
from jaspr.apps.epic.models import NotesLog

class NotesLogSerializer(JasprBaseModelSerializer):
    patient = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    clinic = serializers.SerializerMethodField()
    system = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    def get_system(self, obj):
        return obj.encounter.department.clinic.system.name

    def get_clinic(self, obj):
        return obj.encounter.department.clinic.name

    def get_department(self, obj):
        return obj.encounter.department.name

    def get_patient(self, obj):
        return obj.encounter.patient_id

    def get_created(self, obj):
        return zulu_time_format(obj.created)

    class Meta:
        model = NotesLog
        fields = [
            "id",
            "patient",
            "note",
            "note_type",
            "department",
            "clinic",
            "system",
            "created",

        ]
        read_only_fields = fields
