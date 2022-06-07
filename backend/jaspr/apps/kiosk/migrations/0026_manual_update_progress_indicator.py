from django.db import migrations

# copied from assessment.
INTERVIEW_PROGRESS_SECTION_INITIAL = (
    "Initial"  # instead of None -  (when user has not gone past shame_yes_no_describe)
)
INTERVIEW_PROGRESS_SECTION_SSFAB = (
    "SSF-A/B"  # (when the user has gone past shame_yes_no_describe)
)
INTERVIEW_PROGRESS_SECTION_LETHAL_MEANS = (
    "Lethal Means"  # (when the user has gone past crisis_desc)
)
INTERVIEW_PROGRESS_SECTION_COPE = "Plan to Cope"
INTERVIEW_PROGRESS_SECTION_TUPLE = (
    INTERVIEW_PROGRESS_SECTION_INITIAL,
    INTERVIEW_PROGRESS_SECTION_SSFAB,
    INTERVIEW_PROGRESS_SECTION_LETHAL_MEANS,
    INTERVIEW_PROGRESS_SECTION_COPE,
)


def update_assessment(assessment):
    pass


def update_interview_progress_section(apps, schema_editor):
    Assessment = apps.get_model("kiosk", "Assessment")
    HistoricalAssessment = apps.get_model("kiosk", "HistoricalAssessment")

    for assessment in Assessment.objects.all():
        update_assessment(assessment)

    for ha in HistoricalAssessment.objects.filter():
        update_assessment(ha)


class Migration(migrations.Migration):
    dependencies = [
        ("kiosk", "0025_auto_20201214_1834"),
    ]

    operations = [
        migrations.RunPython(
            update_interview_progress_section,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        )
    ]
