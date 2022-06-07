# Generated by Django 2.2.26 on 2022-01-11 00:08

from django.db import migrations, models


def populate_provider_comment_encounter(apps, schema_editor):
    ProviderComment = apps.get_model("kiosk", "ProviderComment")
    for record in ProviderComment.objects.all():
        record.encounter = record.patient_session.encounter
        record.save()

def populate_patient_measurement_encounter(apps, schema_editor):
    PatientMeasurements = apps.get_model("kiosk", "PatientMeasurements")
    for record in PatientMeasurements.objects.all():
        record.encounter = record.patient_session.encounter
        record.save()

def populate_patient_coping_strategy_encounter(apps, schema_editor):
    PatientCopingStrategy = apps.get_model("kiosk", "PatientCopingStrategy")
    for record in PatientCopingStrategy.objects.all():
        try:
            record.encounter = record.patient_session.encounter
        except AttributeError:
            # Not all PatientCopingStrategies have patient_sessions
            pass
        record.save()

def populate_action_encounter(apps, schema_editor):
    Action = apps.get_model("kiosk", "Action")
    for record in Action.objects.all():
        try:
            record.encounter = record.patient_session.encounter
        except AttributeError:
            # Not all actions are associated with an encounter
            pass
        record.save()

def populate_amendment_encounter(apps, schema_editor):
    Amendment = apps.get_model("kiosk", "Amendment")
    for record in Amendment.objects.all():
        if hasattr(record, 'patient_session') and hasattr(record.patient_session, 'encounter'):
            record.encounter = record.patient_session.encounter
            record.save()

def copy_scores_to_srat(apps, schema_editor):
    PatientSession = apps.get_model("kiosk", "PatientSession")
    for record in PatientSession.objects.order_by('created').all():
        srat = record.srat if hasattr(record, 'srat') else None
        if srat:
            srat.rate_psych_section_viewed = record.rate_psych_section_viewed
            srat.scoring_current_attempt = record.scoring_current_attempt
            srat.scoring_risk = record.scoring_risk
            srat.scoring_score = record.scoring_score
            srat.scoring_suicide_index_score = record.scoring_suicide_index_score
            srat.scoring_suicide_index_score_typology = record.scoring_suicide_index_score_typology
            srat.scoring_suicide_plan_and_intent = record.scoring_suicide_plan_and_intent
            srat.srat_status = record.srat_status
            srat.srat_status_timestamp = record.srat_status_timestamp

            srat.save()


def create_assigned_activities(apps, schema_editor):
    Encounter = apps.get_model("kiosk", "Encounter")
    AssignedActivity = apps.get_model("kiosk", "AssignedActivity")
    ComfortAndSkills = apps.get_model("kiosk", "ComfortAndSkills")
    CustomOnboardingQuestions = apps.get_model("kiosk", "CustomOnboardingQuestions")
    Srat = apps.get_model("kiosk", "Srat")
    Outro = apps.get_model("kiosk", "Outro")

    for custom_onboarding_questions in CustomOnboardingQuestions.objects.all():
        patient_session = custom_onboarding_questions.patient_session
        encounter = patient_session.encounter
        AssignedActivity.objects.create(
            encounter=encounter,
            intro=custom_onboarding_questions,
            created=encounter.created,
            modified=custom_onboarding_questions.created,
            start_time=custom_onboarding_questions.created
        )

    for srat in Srat.objects.all():
        patient_session = srat.patient_session
        encounter = patient_session.encounter

        AssignedActivity.objects.create(
            encounter=encounter,
            suicide_assessment=srat,
            created=srat.created,
            modified=srat.created,
            start_time=patient_session.start_time
        )

    # CSP's are copied forward, so we want to grab the last, most updated version
    # and make all others archived

    for encounter in Encounter.objects.all():
        patient_sessions = encounter.patientsession_set.order_by("-created").all()
        active_csp_processed = False
        for patient_session in patient_sessions:
            csp = patient_session.crisisstabilityplan if hasattr(patient_session, 'crisisstabilityplan') else None
            if csp:
                AssignedActivity.objects.create(
                    status="active" if active_csp_processed == False else 'archived',
                    encounter=encounter,
                    stability_plan=csp,
                    created=csp.created,
                    modified=csp.created,
                    start_time=csp.created
                )
                active_csp_processed = True

        # Every encounter to date has had a skills object
        skills = ComfortAndSkills.objects.create(
            created = encounter.created,
            modified = encounter.created,
        )
        AssignedActivity.objects.create(
            encounter=encounter,
            comfort_and_skills=skills,
            created=encounter.created,
            modified=encounter.created,
            start_time=encounter.created
        )

    for outro in Outro.objects.all():
        patient_session = outro.patient_session
        encounter = patient_session.encounter
        AssignedActivity.objects.create(
            encounter=encounter,
            outro=outro,
            created=outro.modified,
            modified=outro.modified,
            start_time=outro.modified,
        )


def populate_current_section_uid(apps, schema_editor):
    Encounter = apps.get_model("kiosk", "Encounter")
    for encounter in Encounter.objects.all():
        patient_session = encounter.patientsession_set.order_by('created').last()
        if patient_session:
            encounter.current_section_uid = patient_session.current_section_uid
            encounter.save()


def populated_assignment_locks_activity(apps, schema_editor):
    AssignmentLocks = apps.get_model("kiosk", "AssignmentLocks")
    CrisisStabilityPlan = apps.get_model("kiosk", "CrisisStabilityPlan")
    for record in AssignmentLocks.objects.all():
        patient_session = record.patient_session
        # Locks were global, we now need one for both CSA and CSP
        try:
            if patient_session.crisisstabilityplan:
                AssignmentLocks.objects.create(
                    patient_session=patient_session,
                    status=record.status,
                    locked=record.locked,
                    acknowledged=record.acknowledged,
                    activity=patient_session.crisisstabilityplan.assignedactivity
                )
        except CrisisStabilityPlan.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0064_remove_patient_session'),
    ]

    operations = [
        migrations.RunPython(
            copy_scores_to_srat
        ),
        migrations.RunPython(
            populate_current_section_uid
        ),
        migrations.RunPython(
            populate_patient_measurement_encounter
        ),
        migrations.RunPython(
            populate_provider_comment_encounter
        ),
        migrations.RunPython(
            populate_patient_coping_strategy_encounter
        ),
        migrations.RunPython(
            populate_action_encounter
        ),
        migrations.RunPython(
            populate_amendment_encounter
        ),
        migrations.RunPython(
            create_assigned_activities
        ),
        migrations.RunPython(
            populated_assignment_locks_activity
        ),
    ]