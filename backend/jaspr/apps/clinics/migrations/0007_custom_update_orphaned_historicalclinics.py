from django.db import migrations
from django.db.models import Q


def populate_null_organization_code(apps, schema_editor):
    HistoricalClinic = apps.get_model("clinics", "HistoricalClinic")

    historical_clinics = HistoricalClinic.objects.filter(
        Q(organization_code__isnull=True) | Q(organization_code="")
    )
    for num, clinic in enumerate(historical_clinics):
        organization_code = f"deleted-{num}"
        HistoricalClinic.objects.filter(pk=clinic.history_id).update(
            organization_code=organization_code
        )


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0006_custom_fake_migration"),
    ]

    operations = [
        migrations.RunPython(
            populate_null_organization_code,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        )
    ]
