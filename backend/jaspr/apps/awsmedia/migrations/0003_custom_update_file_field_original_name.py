from django.db import migrations
from django.db.models import Q


def update_file_field_original_name_on_historical_records(apps, schema_editor):
    HistoricalMedia = apps.get_model("awsmedia", "HistoricalMedia")

    # Deal with orphaned deleted media records.
    historical_media = HistoricalMedia.objects.filter(
        Q(file_field_original_name__isnull=True) | Q(file_field_original_name="")
    )

    for media in historical_media:
        # not media.file_field.name because historical records save file_field as string.
        original_name = media.file_field
        HistoricalMedia.objects.filter(pk=media.history_id).update(
            file_field_original_name=original_name
        )


def update_file_field_original_name_on_extant_records(apps, schema_editor):
    Media = apps.get_model("awsmedia", "Media")

    media_records = Media.objects.all()

    for media in media_records:
        original_name = media.file_field.name
        Media.objects.filter(pk=media.pk).update(file_field_original_name=original_name)


class Migration(migrations.Migration):

    dependencies = [
        ("awsmedia", "0002_auto_20201026_1437"),
    ]

    operations = [
        migrations.RunPython(
            update_file_field_original_name_on_historical_records,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.RunPython(
            update_file_field_original_name_on_extant_records,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
