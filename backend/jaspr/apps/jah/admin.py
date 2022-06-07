from django.contrib import admin
from django.template.defaultfilters import truncatewords
from simple_history.admin import SimpleHistoryAdmin
from jaspr.apps.jah.models import (
    CommonConcern,
    ConversationStarter,
    PatientCopingStrategy,
    JAHAccount,
    CrisisStabilityPlan as JAHCrisisStabilityPlan
)


@admin.register(CommonConcern)
class CommonConcernAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "truncated_content",
        "order",
    )
    list_editable = ("order",)

    def truncated_content(self, obj):
        return truncatewords(obj.content, 10)

    truncated_content.short_description = "Content"


@admin.register(ConversationStarter)
class ConversationStarterAdmin(admin.ModelAdmin):
    list_display = (
        "truncated_content",
        "order",
    )
    list_editable = ("order",)

    def truncated_content(self, obj):
        return truncatewords(obj.content, 10)

    truncated_content.short_description = "Content"


@admin.register(PatientCopingStrategy)
class PatientCopingStrategyAdmin(SimpleHistoryAdmin):
    list_display = (
        "title",
        "jah_account",
        "category",
        "status",
    )
    raw_id_fields = (
        "jah_account",
        "category",
    )
    search_fields = (
        "title",
        "jah_account__patient__ssid",
    )
    list_filter = ("category",)

@admin.register(JAHCrisisStabilityPlan)
class JAHCrisisStabilityPlanAdmin(SimpleHistoryAdmin):
    def get_patient_name(self, obj):
        try:
            patient = obj.jah_account.patient
            if patient.first_name or patient.last_name:
                return f"{patient.last_name}, {patient.first_name}"
            return f"ssid: {patient.ssid}" if patient.ssid else f"mrn: {patient.mrn}"
        except:
            return ""

    get_patient_name.short_description = "Patient"

    def get_patient_email(self, obj):
        try:
            return obj.jah_account.patient.user.email
        except:
            return ""

    get_patient_email.short_description = "Patient Email"

    list_display = (
        "id",
        "get_patient_name",
        "get_patient_email",
        "status",
        "created",
        "modified"
    )

    search_fields = (
        "jah_account__patient__user__email",
        "jah_account__patient__ssid",
    )

@admin.register(JAHAccount)
class JAHAccountAdmin(SimpleHistoryAdmin):
    def get_patient_name(self, obj):
        try:
            patient = obj.patient
            if patient.first_name or patient.last_name:
                return f"{patient.last_name}, {patient.first_name}"
            return f"ssid: {patient.ssid}" if patient.ssid else f"mrn: {patient.mrn}"
        except:
            return ""

    get_patient_name.short_description = "Patient"

    list_display = (
        "id",
        "get_patient_name",
        "status",
        "created",
        "modified"
    )