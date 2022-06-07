from django.db import migrations
from django.utils.text import slugify


def slugify_names(apps, schema_editor):
    Clinic = apps.get_model("clinics", "Clinic")
    HistoricalClinic = apps.get_model("clinics", "HistoricalClinic")

    clinics = Clinic.objects.all()
    for clinic in clinics:
        organization_code = slugify(clinic.name)
        historical_clinics = HistoricalClinic.objects.filter(id=clinic.pk)
        historical_clinics.update(organization_code=organization_code)

        clinic.organization_code = organization_code
        clinic.save()


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0004_auto_20200914_1432"),
    ]

    operations = [
        migrations.RunPython(
            slugify_names, reverse_code=migrations.RunPython.noop, elidable=True
        )
    ]
