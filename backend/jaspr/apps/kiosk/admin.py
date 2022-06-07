import json
import logging
from datetime import datetime

from django.contrib import admin, messages
from django.db.models import Value, Prefetch
from django.db.models.functions import Concat
from django.template.defaultfilters import truncatewords
from django.utils.html import format_html
from rest_framework.request import Request
from simple_history.admin import SimpleHistoryAdmin
from dateutil.parser import parse
from fuzzywuzzy import fuzz

from jaspr.apps.clinics.models import DepartmentTechnician
from jaspr.apps.epic.models import PatientEhrIdentifier
from jaspr.apps.kiosk.activities.activity_utils import ActivityType, ActivityStatus

from .emails import send_technician_activation_email
from jaspr.apps.kiosk.narrative_note import NarrativeNote
from .models import (
    Action,
    ActivateRecord,
    Activity,
    Amendment,
    AssignedActivity,
    AssignmentLocks,
    CopingStrategy,
    CopingStrategyCategory,
    CustomOnboardingQuestions,
    Encounter,
    GuideMessage,
    Helpline,
    JasprSession,
    NoteTemplate,
    Patient,
    PatientActivity,
    PatientCopingStrategy,
    PatientDepartmentSharing,
    PatientVideo,
    Person,
    SharedStory,
    Technician,
    Topic, CrisisStabilityPlan,
    Srat,
    PatientMeasurements,
    Outro,
)


logger = logging.getLogger(__name__)


class DepartmentTechnicianInline(admin.TabularInline):
    extra = 0
    model = DepartmentTechnician
    readonly_fields = ("id",)
    raw_id_fields = ("technician", "department")


class SharedStoryInline(admin.TabularInline):
    extra = 0
    model = SharedStory
    readonly_fields = ("id",)
    raw_id_fields = ("person", "video")


class AmendmentInline(admin.TabularInline):
    extra = 0
    model = Amendment
    readonly_fields = (
        "id",
        # "assessment",
        "technician",
        "status",
        "created",
        "modified",
    )
    raw_id_fields = (
        # "assessment",
        "technician",
    )

    # NOTE: Currently, this inline is only in use in the `AssessmentAdmin`. We don't
    # necessarily want the assessment in the `AssessmentAdmin` being saved/edited at
    # the time of writing, which means we're explicitly going to make this read only
    # for now.

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Technician)
class TechnicianAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "user",
        "system",
        "analytics_token",
        "status",
        "activation_email_last_sent_at",
        "activated",
        "first_activated_at",
        "last_activated_at",
    )
    readonly_fields = ("first_activated_at", "analytics_token")
    search_fields = ("user__id", "user__email", "analytics_token", )
    raw_id_fields = ("user", "system")
    list_filter = (
        "status",
        "activation_email_last_sent_at",
        "activated",
        "system",
        "first_activated_at",
        "last_activated_at",
    )
    list_select_related = ("user", "primary_department")
    inlines = (DepartmentTechnicianInline,)
    actions = ("send_activation_email",)

    def send_activation_email(modeladmin, request, queryset):
        technicians = []
        for technician in queryset:
            # Let the function set field(s) (currently one, but maybe more in the
            # future) on the `Technician`, but don't have it save the `Technician`;
            # we'll efficiently do the update(s) in bulk.
            update_fields = send_technician_activation_email(
                technician, save_technician=False
            )[1]
            technicians.append(technician)
        if technicians:
            model_class = technicians[0].__class__
            model_class.objects.bulk_update(technicians, update_fields, batch_size=50)
            messages.add_message(
                request,
                messages.SUCCESS,
                f"{len(technicians)} technician activation email(s) queued for delivery.",
            )
        else:
            # NOTE: This shouldn't ever happen right now, but putting it in to be
            # consistent.
            messages.add_message(
                request, messages.WARNING, "No technicians were found to be emailed."
            )


class PatientEhrInline(admin.TabularInline):
    extra = 0
    model = PatientEhrIdentifier
    readonly_fields = (
        "id",
        "epic_settings",
    )

class PatientDepartmentInline(admin.TabularInline):
    extra = 0
    model = PatientDepartmentSharing
    readonly_fields = (
        "id",
    )


@admin.register(Patient)
class PatientAdmin(SimpleHistoryAdmin):
    def get_patient_name(self, patient: Patient):
        if patient.first_name or patient.last_name:
            return f"{patient.last_name}, {patient.first_name}"
    get_patient_name.short_description = "Name"

    def get_queryset(self, request):
        return super(PatientAdmin, self).get_queryset(request).prefetch_related(
            Prefetch(
                'patientdepartmentsharing_set',
                queryset=PatientDepartmentSharing.objects.select_related('department', 'department__clinic',
                                                                         'department__clinic__system'),
                to_attr="patient_department_sharing")
        )

    def get_departments(self, obj):
        try:
            departments = []
            for pds in obj.patient_department_sharing:
                department = pds.department
                clinic = pds.department.clinic
                system = clinic.system
                departments.append(f"{system.name} / {clinic.name} / {department.name}")
            return format_html(('<br />').join(departments))
        except AttributeError:
            return "None"

    get_departments.short_description = "Departments"
    get_departments.allow_tags = True

    def get_search_results(self, request, queryset, search_term):
        # Set search limit since we are doing this in application space
        HARD_SEARCH_LIMIT = 1500
        # Original queryset with just the filters and no search term
        queryset, use_distinct = super(PatientAdmin, self).get_search_results(request, queryset, search_term="")

        result_ids = []
        if search_term:
            # Check search term for date field
            try:
                date, parts = parse(search_term, fuzzy_with_tokens=True)
                search_term = " ".join(parts)
            except ValueError:
                date = False

            # Only search a limited number of records to limit system impact.
            # Users should use a list filter before searching
            for patient in queryset[:HARD_SEARCH_LIMIT]:
                if date:
                    if date.date() != patient.date_of_birth:
                        continue
                    elif date.date() == patient.date_of_birth and not search_term:
                        # If there are no additional search terms, just match on birthdate, otherwise
                        # continue filtering by additional keywords
                        result_ids.append(patient.pk)
                        continue

                if search_term:
                    for prop in self.search_fields:
                        patient_value = getattr(patient, prop)
                        if patient_value is not None:
                            patient_value = str(patient_value).casefold()

                        fuzz_value = fuzz.partial_ratio(patient_value, search_term)
                        if fuzz_value >= 90:
                            result_ids.append(patient.pk)
                            break
                    # We only want to return a max of 30
                    if len(result_ids) >= 30:
                        break

            queryset = queryset.filter(pk__in=result_ids)
        return queryset, use_distinct


    list_display = ("id", "get_patient_name", "ssid", "mrn", "date_of_birth", "analytics_token", "status", "get_departments")
    readonly_fields = ("current_walkthrough_step_changed", "analytics_token")
    raw_id_fields = ("user",)
    search_fields = ("mrn", "ssid", "first_name", "last_name", "analytics_token")
    list_filter = ("status", "created", "tour_complete", "onboarded", "patientdepartmentsharing__department__clinic__system", "patientdepartmentsharing__department__clinic")
    ordering = ("-created",)
    list_select_related = ("user", 'current_walkthrough_step')
    inlines = [PatientEhrInline, PatientDepartmentInline]


class SratInlineAdmin(admin.StackedInline):
    model = Srat


class CspInlineAdmin(admin.StackedInline):
    model = CrisisStabilityPlan


class PatientMeasurementsInlineAdmin(admin.TabularInline):
    extra = 0
    model = PatientMeasurements


class AssignedActivityInline(admin.StackedInline):
    extra = 0
    model = AssignedActivity

    def has_add_permission(self, request: Request, obj: Encounter = None):
        return False

    def get_status(self, assigned_activity: AssignedActivity):
        return ActivityStatus(assigned_activity.activity_status)

    get_status.short_description = "Status"

    def get_type(self, assigned_activity: AssignedActivity):
        return ActivityType(assigned_activity.type).name

    get_type.short_description = "Type"

    fields = ("start_time", "get_type", "get_status", "get_answers", "locked")
    readonly_fields = ("start_time", "locked", "get_answers", "get_type", "get_status")


@admin.register(Encounter)
class EncounterAdmin(SimpleHistoryAdmin):
    inlines = (AssignedActivityInline, PatientMeasurementsInlineAdmin)
    list_display = (
        "get_patient",
        "department",
        "last_heartbeat",
        "session_lock",
    )

    list_select_related = ("department",)
    list_filter = (
        "status",
        "department",
        "session_lock",
        "created",
    )
    ordering = ("-last_heartbeat",)

    def get_patient(self, encounter: Encounter):
        patient = encounter.patient
        if patient.first_name or patient.last_name:
            return f"{patient.last_name}, {patient.first_name}"
        return patient.ssid or patient.mrn

    get_patient.short_description = "Patient"

    def get_answers(self, encounter: Encounter):
        return json.dumps(encounter.get_answers(), indent=4, sort_keys=True)

    get_answers.short_description = "Answers"

    readonly_fields = ["get_answers"]

    actions = ("create_stability_plan_note", "create_narrative_note")

    def create_stability_plan_note(self, request, queryset):
        failed_encounters = []
        success_note_count = 0
        for encounter in queryset:
            try:
                NarrativeNote(encounter).save_stability_plan_note(trigger="admin")
                success_note_count += 1
            except Exception as e:
                failed_encounters.append(encounter)
                logger.exception(e)

            if success_note_count:
                self.message_user(request, f"{success_note_count} note(s) saved")
            if failed_encounters:
                self.message_user(request,
                                  f"{len(failed_encounters)} note(s) failed to save.  They are for encounters {' ,'.join([str(encounter.pk) for encounter in failed_encounters])}",
                                  level=messages.ERROR)

    def create_narrative_note(self, request, queryset):
        failed_encounters = []
        success_note_count = 0
        for encounter in queryset:
            try:
                NarrativeNote(encounter).save_narrative_note(trigger="admin")
                success_note_count += 1
            except Exception as e:
                failed_encounters.append(encounter)
                logger.exception(e)

        if success_note_count:
            self.message_user(request, f"{success_note_count} note(s) saved")
        if failed_encounters:
            self.message_user(request,
                              f"{len(failed_encounters)} note(s) failed to save.  They are for encounters {' ,'.join([str(encounter.pk) for encounter in failed_encounters])}",
                              level=messages.ERROR)


@admin.register(AssignmentLocks)
class AssignmentLocksAdmin(SimpleHistoryAdmin):

    list_display = (
        "activity",
        "locked",
        "acknowledged"
    )

    list_select_related = ("activity",)
    list_filter = (
        "status",
        "locked",
        "acknowledged",
    )


@admin.register(AssignedActivity)
class AssignedActivityAdmin(SimpleHistoryAdmin):

    def get_patient(self, assigned_activity: AssignedActivity):
        return assigned_activity.encounter.patient

    get_patient.short_description = "patient"

    list_display = (
        "get_patient",
        "type",
        "activity_status",
        "activity_status_updated",
    )

    list_filter = (
        "activity_status",
    )



@admin.register(Amendment)
class AmendmentAdmin(SimpleHistoryAdmin):
    list_display = ("id", "technician", "status", "created", "modified")
    # raw_id_fields = ("technician")
    list_filter = ("status", "created", "modified")
    date_hierarchy = "created"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ("created", "modified")
        if obj is None:
            return readonly_fields
        return ("technician", *readonly_fields)


@admin.register(Activity)
class ActivityAdmin(SimpleHistoryAdmin):
    list_display = ("name", "video", "order")
    raw_id_fields = ("video",)
    search_fields = ("name",)
    list_select_related = ("video",)
    ordering = ("order",)


@admin.register(Person)
class PersonAdmin(SimpleHistoryAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)
    list_editable = ("order",)
    ordering = ("order",)

    inlines = (SharedStoryInline,)


@admin.register(Topic)
class TopicAdmin(SimpleHistoryAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)
    list_editable = ("order",)
    ordering = ("order",)

    inlines = (SharedStoryInline,)


@admin.register(SharedStory)
class SharedStoryAdmin(SimpleHistoryAdmin):
    list_display = ("title", "person_name", "topic_name", "video_name", "order")
    raw_id_fields = (
        "person",
        "topic",
        "video",
    )
    search_fields = ("person__name", "topic__name", "video__name")
    list_select_related = (
        "person",
        "topic",
        "video",
    )
    list_editable = ("order",)
    ordering = ("order",)

    def title(self, obj: SharedStory) -> str:
        return f"{obj.person.name} - {obj.topic.name}"

    title.short_description = "Title"
    title.admin_order_field = Concat("person__name", Value(" - "), "topic__name")

    def person_name(self, obj: SharedStory) -> str:
        return obj.person.name

    person_name.short_description = "Name of Person"
    person_name.admin_order_field = "person__name"

    def topic_name(self, obj: SharedStory) -> str:
        return obj.topic.name

    topic_name.short_description = "Name of Topic"
    topic_name.admin_order_field = "topic__name"

    def video_name(self, obj: SharedStory) -> str:
        return obj.video.name

    video_name.short_description = "Name of Video"
    video_name.admin_order_field = "video__name"


@admin.register(NoteTemplate)
class NoteTemplateAdmin(SimpleHistoryAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("created", "modified",)


@admin.register(PatientActivity)
class PatientActivityAdmin(SimpleHistoryAdmin):
    list_display = (
        "patient",
        "activity",
        "modified",
        "rating",
        "save_for_later",
        "viewed",
    )
    raw_id_fields = ("patient", "activity")
    search_fields = ("patient__ssid",)
    list_filter = ("activity", "modified", "save_for_later")
    list_select_related = ("patient", "activity")


@admin.register(PatientVideo)
class PatientVideoAdmin(SimpleHistoryAdmin):
    list_display = (
        "patient",
        "video",
        "modified",
        "rating",
        "save_for_later",
        "viewed",
    )
    raw_id_fields = ("patient", "video")
    search_fields = ("patient__ssid",)
    list_filter = ("video__name", "video__tags", "modified", "save_for_later", "viewed")
    list_select_related = ("patient", "video")


@admin.register(Action)
class ActionAdmin(SimpleHistoryAdmin):
    list_display = (
        "patient",
        "action",
        "screen",
        "extra",
        "section_uid",
        "timestamp",
        "client_timestamp",
    )
    raw_id_fields = ("patient",)
    list_select_related = ("patient",)
    search_fields = ("action", "screen", "extra", "section_uid", "patient__ssid")
    list_filter = ("action", "section_uid")
    ordering = ("-timestamp",)


@admin.register(ActivateRecord)
class ActivateRecordAdmin(SimpleHistoryAdmin):
    list_display = ("timestamp", "technician", "patient", "new")
    readonly_fields = ("timestamp",)
    raw_id_fields = ("technician", "patient")
    list_filter = ("timestamp", "new")
    date_hierarchy = "timestamp"
    list_select_related = ("technician", "patient")
    search_fields = (
        "timestamp",
        "technician__id",
        "patient__id",
        "patient__ssid",
    )
    ordering = ("-timestamp",)


@admin.register(JasprSession)
class JasprSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "user_email",
        "user_type",
        "created",
        "expiry",
        "in_er",
        "from_native",
        "long_lived",
    )
    readonly_fields = (
        "id",
        "user_id",
        "user_email",
        "user_type",
        "created",
        "expiry",
        "digest",
        "token_key",
    )
    # Don't need the `auth_token` field to show because we shouldn't ever set/change
    # that field directly, and we're already showing all the relevant/necessary fields
    # from it anyway.
    exclude = ("auth_token",)
    search_fields = (
        "auth_token__token_key",
        "auth_token__user__id",
        "auth_token__user__email",
    )
    list_filter = (
        "auth_token__created",
        "auth_token__expiry",
        "user_type",
        "in_er",
        "from_native",
        "long_lived",
    )
    ordering = ("-auth_token__created", "-auth_token__expiry")
    list_select_related = ("auth_token__user",)
    date_hierarchy = "auth_token__created"

    def user_id(self, obj: JasprSession) -> int:
        return obj.auth_token.user.id

    user_id.short_description = "User ID"
    user_id.admin_order_field = "auth_token__user__id"

    def user_email(self, obj: JasprSession) -> str:
        return obj.auth_token.user.email

    user_email.short_description = "User Email"
    user_email.admin_order_field = "auth_token__user__email"

    def created(self, obj: JasprSession) -> datetime:
        return obj.auth_token.created

    created.short_description = "Created"
    created.admin_order_field = "auth_token__created"

    def expiry(self, obj: JasprSession) -> datetime:
        return obj.auth_token.expiry

    expiry.short_description = "Expires At"
    expiry.admin_order_field = "auth_token__expiry"

    def digest(self, obj: JasprSession) -> str:
        return obj.auth_token.digest

    digest.short_description = "Digest"
    digest.admin_order_field = "auth_token__digest"

    def token_key(self, obj: JasprSession) -> str:
        return obj.auth_token.token_key

    token_key.short_description = "Token Key"
    token_key.admin_order_field = "auth_token__token_key"


    def has_add_permission(self, request):
        """
        `JasprSession`s cannot be created in the admin.
        """
        return False


@admin.register(CopingStrategy)
class CopingStrategyAdmin(SimpleHistoryAdmin):
    list_display = (
        "name",
        "title",
        "category",
    )
    raw_id_fields = ("category",)
    search_fields = ("name",)
    list_filter = ("category",)


@admin.register(CopingStrategyCategory)
class CopingStrategyCategoryAdmin(SimpleHistoryAdmin):
    list_display = ("name", "slug", "why_text")

    def truncated_why_text(self, obj):
        return truncatewords(obj.content, 10)

    truncated_why_text.short_description = "Why Text"


@admin.register(PatientCopingStrategy)
class PatientCopingStrategyAdmin(SimpleHistoryAdmin):
    list_display = (
        "title",
        "encounter",
        "category",
        "status",
    )
    raw_id_fields = (
        "encounter",
        "category",
    )
    search_fields = (
        "title",
        "encounter__patient__ssid",
    )
    list_filter = ("category",)


@admin.register(GuideMessage)
class GuideAdmin(SimpleHistoryAdmin):
    list_display = ("name", "message")

    def truncated_message(self, obj):
        return truncatewords(obj.content, 10)

    truncated_message.short_description = "Message"


@admin.register(Helpline)
class Helpline(SimpleHistoryAdmin):
    list_display = (
        "name",
        "phone",
        "text",
    )


class BaseAssessmentAdmin(SimpleHistoryAdmin):
    def get_patient_name(self, obj):
        try:
            patient = obj.encounter.patient
            if (patient.last_name or patient.first_name):
                return f"{patient.last_name}, {patient.first_name}"
            return f"SSID: {patient.ssid}"
        except:
            return ""

    get_patient_name.short_description = "Patient"

    def get_department_name(self, obj):
        try:
            dept = obj.encounter.department
            clinic = dept.clinic
            system = clinic.system
            return f"{system.name} > {clinic.name} > {dept.name}"
        except:
            return ""

    get_department_name.short_description = "Department"

    def get_encounter(self, obj):
        try:
            return obj.assigned_activity.encounter
        except:
            return None

    get_encounter.short_description = "Encounter"



@admin.register(CustomOnboardingQuestions)
class CustomOnboardingQuestionsAdmin(BaseAssessmentAdmin):
    list_display = (
        "id",
        "get_patient_name",
        "get_department_name",
        "get_encounter",
        "status",
        "created",
        "modified"
    )



@admin.register(CrisisStabilityPlan)
class CrisisStabilityPlanAdmin(BaseAssessmentAdmin):
    list_display = (
        "id",
        "get_patient_name",
        "get_department_name",
        "get_encounter",
        "status",
        "created",
        "modified"
    )


@admin.register(Srat)
class SRATAdmin(BaseAssessmentAdmin):
    list_display = (
        "id",
        "get_patient_name",
        "get_department_name",
        "get_encounter",
        "status",
        "created",
        "modified"
    )

@admin.register(Outro)
class OutroAdmin(BaseAssessmentAdmin):
    list_display = (
        "id",
        "get_patient_name",
        "get_department_name",
        "get_encounter",
        "status",
        "created",
        "modified"
    )


@admin.register(PatientMeasurements)
class PatientMeasurements(admin.ModelAdmin):
    list_display = (
        "id",
        "encounter",
        "created",
        "modified"
    )