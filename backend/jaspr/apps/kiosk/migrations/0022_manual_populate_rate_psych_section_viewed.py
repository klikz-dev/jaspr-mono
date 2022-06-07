from django.db import migrations


def update_rate_psych_section_viewed(apps, schema_editor):
    Action = apps.get_model("kiosk", "Action")
    Assessment = apps.get_model("kiosk", "Assessment")

    for assessment in Assessment.objects.all():
        action = (
            Action.objects.filter(patient=assessment.patient, action="Arrive")
            .order_by("-created")
            .first()
        )
        if action:
            assessment.rate_psych_section_viewed = action.timestamp
            assessment.save()


class Migration(migrations.Migration):

    dependencies = [
        ("kiosk", "0021_auto_20201001_1831"),
    ]

    operations = [
        migrations.RunPython(
            update_rate_psych_section_viewed,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        )
    ]
