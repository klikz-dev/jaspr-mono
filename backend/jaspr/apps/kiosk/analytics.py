import sys
import pytz
from datetime import datetime
from typing import Iterator, Optional, Sequence

from django.db.models import Prefetch, Subquery
from django.utils.functional import cached_property
from jaspr.apps.clinics.models import DepartmentTechnician, HealthcareSystem
from jaspr.apps.epic.models import NotesLog
from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.kiosk.models import (
    Action,
    ActivateRecord,
    AssignedActivity,
    PatientActivity,
    PatientVideo,
    Patient,
    Technician,
    Encounter,
    Srat,
    Outro,
    CustomOnboardingQuestions,
    CrisisStabilityPlan,
    LethalMeans,
)
from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from jaspr.apps.kiosk.activities.question_json import extract_answer_keys_from_json


class AnalyticsExporter:
    """Exports analytics data for Jaspr."""

    def __init__(self, system: HealthcareSystem, start_date: datetime, end_date: datetime, include_mrn: bool,
                 include_analytics_token: bool):
        self.system = system
        self.start_date = start_date or datetime('2020-01-01')
        self.end_date = end_date or datetime.now()
        self.include_mrn = include_mrn
        self.include_analytics_token = include_analytics_token

    @cached_property
    def departments(self):
        return self.system.get_departments()

    @staticmethod
    def format_timestamp(timestamp: Optional[datetime]) -> Optional[str]:
        if not timestamp:
            return None
        tz = pytz.timezone("America/Los_Angeles")
        # Allow the timestamp to be generated properly locally for testing purposes if
        # the local machine is a windows machine.
        day_format = "%#d" if sys.platform == "win32" else "%d"
        return timestamp.astimezone(tz).strftime("%B {0}, %Y %I:%M:%S %p %Z".format(day_format))

    @staticmethod
    def format_date(timestamp: Optional[datetime]) -> Optional[str]:
        if not timestamp:
            return None
        tz = pytz.timezone("America/Los_Angeles")
        day_format = "%#d" if sys.platform == "win32" else "%d"
        return timestamp.astimezone(tz).strftime("%B {0}, %Y".format(day_format))

    @staticmethod
    def format_time(timestamp: Optional[datetime]) -> Optional[str]:
        if not timestamp:
            return None
        tz = pytz.timezone("America/Los_Angeles")
        return timestamp.astimezone(tz).strftime("%I:%M:%S %p %Z")

    @property
    def visit_log_iterator(self) -> Iterator[Sequence]:
        optional_headers = []
        if self.include_analytics_token:
            optional_headers.append("Analytics Token")
        if self.include_mrn:
            optional_headers.append('MRN')
        yield [
            *optional_headers,
            "Technician ID",
            "Visit Timestamp",
            "Clinic Department",
        ]
        activate_record_iterator = (
            ActivateRecord.objects.filter(
                encounter__department__in=self.departments,
                timestamp__range=[self.start_date, self.end_date]
            )
                .select_related("encounter__department")
                .order_by("timestamp")
                .iterator()
        )

        for record in activate_record_iterator:
            optional_fields = []
            if self.include_analytics_token:
                optional_fields.append(record.patient.analytics_token)
            if self.include_mrn:
                optional_fields.append(record.patient.mrn)
            yield [
                *optional_fields,
                record.technician_id,
                self.format_timestamp(record.timestamp),
                record.encounter.department.name,
            ]

    @property
    def action_log_iterator(self) -> Iterator[Sequence]:
        optional_headers = []
        if self.include_analytics_token:
            optional_headers.append("Analytics Token")
        if self.include_mrn:
            optional_headers.append('MRN')
        yield [
            *optional_headers,
            "In ER",
            "Action",
            "Screen",
            "Timestamp",
            "Client Timestamp",
        ]
        actions_iterator = (
            Action.objects.filter(
                encounter__department__in=self.departments,
                created__range=[self.start_date, self.end_date]
            )
                .select_related("patient")
                .order_by("timestamp")
                .iterator()
        )
        for action in actions_iterator:
            action_name = action.action
            if (
                    action_name in (ActionNames.SUBMIT, ActionNames.ARRIVE)
                    and action.section_uid
            ):
                action_name += f" {action.section_uid}"
            elif (
                    action_name
                    in (
                            ActionNames.WATCH,
                            ActionNames.JAH_WALKTHROUGH_ARRIVE,
                            ActionNames.JAH_WALKTHROUGH_CLICKED_MORE_INFO,
                            ActionNames.JAH_USER_COPY,
                            ActionNames.JAH_OPEN_CONCERN,
                    )
                    and action.extra
            ):
                action_name += f" {action.extra}"
            optional_fields = []
            if self.include_analytics_token:
                optional_fields.append(action.patient.analytics_token)
            if self.include_mrn:
                optional_fields.append(action.patient.mrn)
            yield [
                *optional_fields,
                action.in_er,
                action_name,
                action.screen,
                self.format_timestamp(action.timestamp),
                self.format_timestamp(action.client_timestamp),
            ]

    @property
    def assessment_iterator(self) -> Iterator[Sequence]:
        field_names = extract_answer_keys_from_json(
            CustomOnboardingQuestions.get_static_questions()) + extract_answer_keys_from_json(
            Srat.get_static_questions()) + extract_answer_keys_from_json(
            LethalMeans.get_static_questions()) + extract_answer_keys_from_json(
            CrisisStabilityPlan.get_static_questions()) + extract_answer_keys_from_json(Outro.get_static_questions())

        scoring_fields = [
            "scoring_score",
            "scoring_current_attempt",
            "scoring_suicide_plan_and_intent",
            "scoring_risk",
            "scoring_suicide_index_score",
            "scoring_suicide_index_score_typology",
        ]

        def _map_fields_to_answers(encounter: Encounter):
            department_name = encounter.department.name
            analytics_token = encounter.patient.analytics_token
            mrn = encounter.patient.mrn
            intro = encounter.get_activity(ActivityType.Intro)
            stability_plan = encounter.get_activity(ActivityType.StabilityPlan)
            suicide_assessment = encounter.get_activity(ActivityType.SuicideAssessment)
            outro = encounter.get_activity(ActivityType.Outro)

            answers = {}
            if intro:
                answers.update(intro.get_answers()),
            if suicide_assessment:
                answers.update(suicide_assessment.get_answers())
            if stability_plan:
                answers.update(stability_plan.get_answers()),
            if outro:
                answers.update(outro.get_answers())

            optional_fields = []
            if self.include_analytics_token:
                optional_fields.append(analytics_token)
            if self.include_mrn:
                optional_fields.append(mrn)

            if answers:
                values = [encounter.start_time, *[answers.get(field_name, "") for field_name in field_names]]
                if suicide_assessment:
                    metadata = suicide_assessment.get_metadata()
                else:
                    metadata = {}
                scores = [metadata.get(field, "") for field in scoring_fields]
                return optional_fields + [department_name] + values + scores
            return optional_fields

        # For the first row, yield the headers of the Excel/CSV data.
        optional_headers = []
        if self.include_analytics_token:
            optional_headers.append("Analytics Token")
        if self.include_mrn:
            optional_headers.append('MRN')

        yield [*optional_headers, "Department", "Encounter Start Time", *field_names, *scoring_fields]

        yield from map(_map_fields_to_answers, Encounter.objects.filter(
            department__in=self.departments,
            created__range=[self.start_date, self.end_date]
        ).select_related("patient", "department").order_by("modified").iterator())

    @property
    def technicians_iterator(self) -> Iterator[Sequence]:
        optional_headers = []
        if self.include_analytics_token:
            optional_headers.append("Analytics Token")
        yield [
            *optional_headers,
            "Provider",
            "Role",
            "Intro Sent",
            "Education/Training",
            "Account Created",
            "Setup 1st Patient",
            "Jaspr Coach Modeling",
            "Practice with Support",
            "Document 1st patient",
            "Share Jaspr Experiences"
        ]

        technician_iterator = (
            Technician.objects.filter(
                status="active",
                id__in=Subquery(DepartmentTechnician.objects.filter(
                    status="active",
                    department__in=self.departments,
                    created__range=[self.start_date, self.end_date]
                ).distinct("technician").values_list("technician", flat=True)),
            ).iterator()
        )

        for technician in technician_iterator:
            optional_fields = []
            if self.include_analytics_token:
                optional_fields.append(technician.analytics_token)

            yield [
                *optional_fields,
                f"{technician.last_name}, {technician.first_name}",
                technician.role,
                technician.activation_email_last_sent_at is not None,
                technician.training_complete,
                technician.activated,
                ActivateRecord.objects.filter(technician=technician).exists(),
                technician.coach_modeling_complete,
                technician.practice_with_support_complete,
                NotesLog.objects.filter(sent_by=technician).exists(),
                ""  # To be filled in manually in the export for now
            ]

    @property
    def skills_iterator(self) -> Iterator[Sequence]:
        optional_headers = []
        if self.include_analytics_token:
            optional_headers.append("Analytics Token")
        if self.include_mrn:
            optional_headers.append('MRN')
        yield [
            *optional_headers,
            "Activity Title",
            "Modified",
            "Saved",
            "Rating",
            "Viewed",
        ]
        patient_activities_iterator = (
            PatientActivity.objects.filter(
                status="active",
                patient_id__in=Subquery(Patient.objects.filter(encounter__department__in=self.departments).only("id")),
                created__range=[self.start_date, self.end_date]
            )
                .select_related("patient", "activity")
                .order_by("patient__id", "modified")
                .iterator()
        )
        for patient_activity in patient_activities_iterator:
            optional_fields = []
            if self.include_analytics_token:
                optional_fields.append(patient_activity.patient.analytics_token)
            if self.include_mrn:
                optional_fields.append(patient_activity.patient.mrn)
            yield [
                *optional_fields,
                patient_activity.activity.name,
                self.format_timestamp(patient_activity.modified),
                patient_activity.save_for_later,
                patient_activity.rating,
                self.format_timestamp(patient_activity.viewed),
            ]

    @property
    def videos_iterator(self) -> Iterator[Sequence]:
        optional_headers = []
        if self.include_analytics_token:
            optional_headers.append("Analytics Token")
        if self.include_mrn:
            optional_headers.append('MRN')
        yield [
            *optional_headers,
            "Video Title",
            "Modified",
            "Saved",
            "Rating",
            "Viewed",
        ]
        patient_videos_iterator = (
            PatientVideo.objects.filter(
                status="active",
                patient_id__in=Subquery(Patient.objects.filter(encounter__department__in=self.departments).only("id")),
                created__range=[self.start_date, self.end_date]
            )
                .select_related("patient", "video")
                .order_by("patient__id", "modified")
                .iterator()
        )
        for patient_video in patient_videos_iterator:
            optional_fields = []
            if self.include_analytics_token:
                optional_fields.append(patient_video.patient.analytics_token)
            if self.include_mrn:
                optional_fields.append(patient_video.patient.mrn)
            yield [
                *optional_fields,
                patient_video.video.name,
                self.format_timestamp(patient_video.modified),
                patient_video.save_for_later,
                patient_video.rating,
                self.format_timestamp(patient_video.viewed),
            ]

    @property
    def encounters_iterator(self) -> Iterator[Sequence]:
        optional_headers = []
        if self.include_analytics_token:
            optional_headers.append("Analytics Token")
        if self.include_mrn:
            optional_headers.append('MRN')
        yield [
            *optional_headers,
            "Date Created",
            "Time Created",
            "Date Patient Started",
            "Time Patient Started",
            "CSA",
            "CSP",
            "C&S",
            "LM",
            "Activities Assigned",
            "Completed CSA",
            "Completed LM",
            "Completed CSP",
            "Confidence",
            "Readiness",
            "JAH",
            "Jaspr Rating",
            "Overall ER Rating",
            "Recommend Jaspr",
            "Time Here",
            "Pre-Distress",
            "Pre-Frustration",
            "Post-Distress",
            "Post-Frustration",
            "Change in Distress",
            "Change in Frustration",
            "Active CSP",
            "Provider Led",
            "Clinic",
            "Department"
        ]

        def _map_fields_to_answers(encounter: Encounter):
            optional_fields = []
            analytics_token = encounter.patient.analytics_token
            mrn = encounter.patient.mrn
            if self.include_analytics_token:
                optional_fields.append(analytics_token)
            if self.include_mrn:
                optional_fields.append(mrn)

            has_csa = encounter.has_activity(ActivityType.SuicideAssessment)
            has_csp = encounter.has_activity(ActivityType.StabilityPlan)
            has_cs = encounter.has_activity(ActivityType.ComfortAndSkills)
            has_lm = encounter.has_activity(ActivityType.LethalMeans)

            activities_assigned = []
            if has_csa:
                activities_assigned.append('CSA')
            if has_csp:
                activities_assigned.append('CSP')
            if has_cs:
                activities_assigned.append('C&S')

            answers = encounter.get_answers().get('answers', {})

            distress0 = answers.get('distress0')
            distress1 = answers.get('distress1')
            frustration0 = answers.get('frustration0')
            frustration1 = answers.get('frustration1')
            change_distress = None
            change_frustration = None
            if (distress0 is not None and distress1 is not None):
                change_distress = distress1 - distress0
            if (frustration0 is not None and frustration1 is not None):
                change_frustration = frustration1 - frustration0

            values = [
                self.format_date(encounter.created),
                self.format_time(encounter.created),
                self.format_date(encounter.start_time),
                self.format_time(encounter.start_time),
                has_csa,
                has_csp,
                has_cs,
                has_lm,
                " + ".join(activities_assigned),
                encounter.get_activity(ActivityType.SuicideAssessment).assignedactivity.activity_status in ["completed", "updated"] if has_csa else "",
                encounter.get_activity(ActivityType.LethalMeans).assignedactivity.activity_status in ["completed", "updated"] if has_lm else "",
                encounter.get_activity(ActivityType.StabilityPlan).assignedactivity.activity_status in ["completed", "updated"] if has_csp else "",
                answers.get("stability_confidence"),
                answers.get("readiness"),
                encounter.patient.tools_to_go_status != "Not Started",
                answers.get("jaspr_rating"),
                answers.get("overall_er_care"),
                answers.get("jaspr_recommend"),
                answers.get("time_here"),
                distress0,
                frustration0,
                distress1,
                frustration1,
                change_distress,
                change_frustration,
                encounter.get_activity(ActivityType.StabilityPlan).assignedactivity.activity_status in ["in-progress", "completed", "updated"] if has_csp else "",
                encounter.technician_operated,
                encounter.department.clinic.name,
                encounter.department.name
            ]

            return optional_fields + values

        yield from map(_map_fields_to_answers,
                       Encounter.objects.select_related('patient', 'department', 'department__clinic').prefetch_related(Prefetch(
                           "assignedactivity_set",
                           queryset=AssignedActivity.objects.order_by("-created").select_related(
                               'stability_plan', 'suicide_assessment', 'comfort_and_skills', 'intro', 'outro',
                               'lethal_means'
                           )
                       )).filter(
                           department__in=self.departments,
                           created__range=[self.start_date, self.end_date]
                       ))
