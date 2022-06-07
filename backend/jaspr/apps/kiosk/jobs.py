import logging
from datetime import timedelta
from sentry_sdk import capture_exception

from django.core.cache import cache
from django.db.models import Count, DurationField, ExpressionWrapper, F, Q
from django.utils import timezone
from django_rq.decorators import job
from django_rq.jobs import Job

from .emails import send_tools_to_go_setup_email
from jaspr.apps.kiosk.models import Action, Patient, AssignedActivity
from jaspr.apps.kiosk.narrative_note import NarrativeNote
from jaspr.apps.epic.models import EpicDepartmentSettings, NotesLog
from jaspr.apps.common.jobs.messaging import email_engineering, email_support

logger = logging.getLogger(__name__)


@job
def create_action(valid_action_data: dict) -> None:
    action = Action.objects.create(**valid_action_data)
    logger.info(
        "Created Action %s (screen=%s, extra=%s, section_uid=%s) at %s for Patient ID %d.",
        action.action,
        action.screen,
        action.extra,
        action.section_uid,
        action.timestamp,
        action.patient_id,
    )


def queue_action_creation(valid_action_data: dict) -> Job:
    valid_action_data.setdefault("timestamp", timezone.now())
    return create_action.delay(valid_action_data)


@job
def check_and_resend_tools_to_go_setup_email(
        patient_pk: int, email_number: int
) -> Job:
    patient = Patient.objects.get(pk=patient_pk)
    if patient.tools_to_go_status in (
            Patient.TOOLS_TO_GO_NOT_STARTED,
            Patient.TOOLS_TO_GO_EMAIL_SENT,
    ):
        kwargs = {}
        if email_number == 1:
            kwargs["template_base"] = "kiosk/tools_to_go_setup_first_resend"
        elif email_number == 2:
            kwargs["template_base"] = "kiosk/tools_to_go_setup_second_resend"
        send_tools_to_go_setup_email(patient.user, **kwargs)


@job
def check_for_unsent_notes() -> Job:
    cache_key = "job-in-progress-sending-ehr-notes"
    in_progress = cache.get(cache_key)

    if in_progress:
        logger.info("Skipping Job Sending EHR Notes because the previous job is still running")
        return None

    logger.info("Starting Job Sending EHR Notes")
    cache.set(cache_key, True)
    notes_sent = 0
    try:
        # We will only process departments that are integrated with the Epic EHR
        epic_department_ids = list(EpicDepartmentSettings.objects.values_list("department", flat=True))

        # Time since update
        inactive_time = timezone.now() - timezone.timedelta(minutes=10)

        # Find all patient suicide assessments where the note has not been sent to
        # the EHR Or the Note was sent to the EHR, but the suicide_assessment has been modified since the note was sent.
        # We only send notes that have been stale for at least 10 minutes.  We do not send notes that have been stale
        # for longer than 60 minutes
        suicide_assessment_assignments = AssignedActivity.objects.filter(
            start_time__isnull=False,
            encounter__department__in=epic_department_ids,
            suicide_assessment__isnull=False,
            suicide_assessment__answers__isnull=False,
        ).select_related("encounter").annotate(
            time_since=ExpressionWrapper(F("suicide_assessment__modified") - F("suicide_assessment__note_generated"),
                                         output_field=DurationField())).annotate(
            note_count=Count("encounter__noteslog", filter=Q(encounter__noteslog__note_type="narrative_note",
                                                             encounter__noteslog__status="sent"))).filter(
            Q(time_since__gte=timezone.timedelta(minutes=10),
              time_since__lte=timezone.timedelta(minutes=60)
              ) | Q(suicide_assessment__note_generated__isnull=True,
                    suicide_assessment__modified__lte=inactive_time))

        logger.info(f"Auto Sending {len(suicide_assessment_assignments)} narrative notes to EHR")

        for suicide_assessment_assignment in suicide_assessment_assignments:
            encounter = suicide_assessment_assignment.encounter
            logger.info(f"saving narrative note for activity assignment {suicide_assessment_assignment.pk}")
            logger.info(
                f"encounter {encounter.pk} has had {suicide_assessment_assignment.note_count} stability plan notes sent to EHR")
            if suicide_assessment_assignment.note_count > 1000:
                message = f"More than 1,000 narrative notes have been sent to the EHR for encounter {encounter.pk}"
                logger.warning(message)
                continue

            try:
                NarrativeNote(encounter).save_narrative_note(trigger="cron")
                notes_sent = notes_sent + 1
            except Exception as e:
                logger.exception(
                    f"Failed to Auto send narrative note for encounter {suicide_assessment_assignment.encounter.pk}",
                    exc_info=e)
                capture_exception(e)

        # Find all patient CSP's where the CSP is assigned, but the note has not been sent to the EHR
        # Or the Note was sent to the EHR, but the CSP has been modified since the note was sent.
        # We only send notes that have been stale for at least 10 minutes.  Notes older than 60 minutes
        # do not get sent.
        stability_plan_assignments = AssignedActivity.objects.filter(
            start_time__isnull=False,
            encounter__department__in=epic_department_ids,
            stability_plan__isnull=False,
            stability_plan__answers__isnull=False,
        ).select_related("encounter").annotate(
            time_since=ExpressionWrapper(F("stability_plan__modified") - F("stability_plan__note_generated"),
                                         output_field=DurationField())).annotate(
            note_count=Count("encounter__noteslog", filter=Q(encounter__noteslog__note_type="stability_plan",
                                                             encounter__noteslog__status="sent"))).filter(
            Q(time_since__gte=timezone.timedelta(minutes=10), time_since__lte=timezone.timedelta(minutes=60)) | Q(
                stability_plan__note_generated__isnull=True,
                stability_plan__modified__lte=inactive_time))

        for stability_plan_assignment in stability_plan_assignments:
            encounter = stability_plan_assignment.encounter
            logger.info("saving stability note for assigned activity {stability_plan_assignment.pk")

            logger.info(
                f"encounter {encounter.pk} has had {stability_plan_assignment.note_count} stability plan notes sent to EHR")
            if stability_plan_assignment.note_count > 1000:
                message = f"More than 1,000 stability plan notes have been sent to the EHR for encounter {encounter.pk}"
                logger.warning(message)
                continue

            try:
                NarrativeNote(stability_plan_assignment.encounter).save_stability_plan_note(trigger="cron")
                notes_sent = notes_sent + 1
            except Exception as e:
                logger.exception("Failed to Auto send stability plan note for encounter %s",
                                 stability_plan_assignment.encounter.pk,
                                 exc_info=e)
                capture_exception(e)

    except Exception as e:
        logger.exception("Job Sending EHR Notes has failed", exc_info=e)
        capture_exception(e)
    finally:
        # Cleanup
        cache.delete(cache_key)
        logger.info(f"Finished Job Sending {notes_sent} EHR Notes")


@job
def review_note_sending() -> Job:
    oversent_notes = NotesLog.objects.filter(status="sent").values("encounter", "note_type").annotate(
        Count("encounter")).filter(encounter__count__gte=1)

    message = ""
    if oversent_notes:
        message += f"The following encounters have sent 1000+ notes to the EHR and should be investigated:\n"
        for oversent_note in oversent_notes:
            message += f"\tEncounter {oversent_note['encounter']} has saved {oversent_note['encounter__count']} notes" \
                       f" of type {oversent_note['note_type']}\n "

    epic_department_ids = list(EpicDepartmentSettings.objects.values_list("department", flat=True))

    suicide_assessment_assignments = AssignedActivity.objects.filter(
        start_time__isnull=False,
        encounter__department__in=epic_department_ids,
        suicide_assessment__isnull=False,
        suicide_assessment__answers__isnull=False,
    ).select_related("encounter").annotate(
        time_since=ExpressionWrapper(F("suicide_assessment__modified") - F("suicide_assessment__note_generated"),
                                     output_field=DurationField())).filter(
        Q(time_since__gte=timezone.timedelta(minutes=60)
          ))

    stability_plan_assignments = AssignedActivity.objects.filter(
        start_time__isnull=False,
        encounter__department__in=epic_department_ids,
        stability_plan__isnull=False,
        stability_plan__answers__isnull=False,
    ).select_related("encounter").annotate(
        time_since=ExpressionWrapper(F("stability_plan__modified") - F("stability_plan__note_generated"),
                                     output_field=DurationField())).filter(
        Q(time_since__gte=timezone.timedelta(minutes=60)))

    if suicide_assessment_assignments:
        message += f"\n\nThe following encounters have suicide assessments that have not had notes sent, but should have, and the time has since expired to send them:\n"
        for suicide_assessment_assignment in suicide_assessment_assignments:
            message += f"\tEncounter {suicide_assessment_assignment.encounter}, suicide assessment {suicide_assessment_assignment.pk}\n"

    if stability_plan_assignments:
        message += f"\n\nThe following encounters have stability plans that have not had notes sent, but should have, and the time has since expired to send them:\n"
        for stability_plan_assignment in stability_plan_assignments:
            message += f"\tEncounter {stability_plan_assignment.encounter}, stability plan {stability_plan_assignment.pk}\n"

    if len(message) > 0:
        email_engineering("EHR Note syncing log", message)