import logging
from django.contrib import admin, messages
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from simple_history.admin import SimpleHistoryAdmin

from jaspr.apps.epic.models import (
    EpicDepartmentSettings,
    EpicSettings,
    PatientEhrIdentifier,
    NotesLog,
)

logger = logging.getLogger(__name__)


# Register your models here.
class EpicSettingsAdmin(SimpleHistoryAdmin, DynamicArrayMixin):

    @staticmethod
    def public_key(obj):
        return obj.serialized_public_key

    list_display = (
        "id",
        "name",
        "status",
        "provider",
    )

    readonly_fields = (
        "public_key",
    )



class EpicDepartmentSettingsAdmin(SimpleHistoryAdmin, DynamicArrayMixin):

    list_display = ("id", "status", "department", "location_code")
    search_fields = ("department", "location_code")


class PatientEhrIdentifiersAdmin(SimpleHistoryAdmin, DynamicArrayMixin):

    list_display = ("patient_name", "fhir_id")
    search_fields = ("id", "fhir_id")

    def patient_name(self, obj):
        return "%s, %s" % (obj.patient.last_name, obj.patient.first_name)


class NotesLogAdmin(SimpleHistoryAdmin, DynamicArrayMixin):
    list_display = ("id", "patient_name", "department", "note_type", "fhir_id", "created")
    search_fields = ("id", "fhir_id")
    readonly_fields = ("response", )

    list_filter = (
        "encounter__department",
        "note_type",
        "created",
    )
    list_select_related = (
        "encounter",
        "encounter__department",
        "encounter__patient"
    )

    def department(self, obj):
        return obj.encounter.department

    def patient_name(self, obj):
        patient = obj.encounter.patient
        return f"{patient.last_name}, {patient.first_name}"

    actions = ("send_note_to_ehr",)

    def send_note_to_ehr(self, request, queryset):
        failed_notes = []
        success_note_count = 0
        for note in queryset:
            try:
                note.send_to_ehr()
                success_note_count += 1
            except Exception as e:
                failed_notes.append(note)
                logger.exception(e)

        if success_note_count:
            self.message_user(request, f"{success_note_count} note(s) successfully sent to EHR")
        if failed_notes:
            self.message_user(request,
                              f"{len(failed_notes)} note(s) failed to send.  They are {' ,'.join([str(note.pk) for note in failed_notes])}",
                              level=messages.ERROR)


admin.site.register(EpicSettings, EpicSettingsAdmin)
admin.site.register(EpicDepartmentSettings, EpicDepartmentSettingsAdmin)
admin.site.register(PatientEhrIdentifier, PatientEhrIdentifiersAdmin)
admin.site.register(NotesLog, NotesLogAdmin)
