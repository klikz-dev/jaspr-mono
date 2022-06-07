# Generated by Django 2.2.13 on 2020-10-01 23:31

import fernet_fields.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kiosk", "0020_amendment_historicalamendment"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessment",
            name="rate_psych_section_viewed",
            field=fernet_fields.fields.EncryptedDateTimeField(
                blank=True,
                help_text="rate_psych section first viewed at this datetime.",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalassessment",
            name="rate_psych_section_viewed",
            field=fernet_fields.fields.EncryptedDateTimeField(
                blank=True,
                help_text="rate_psych section first viewed at this datetime.",
                null=True,
            ),
        ),
    ]