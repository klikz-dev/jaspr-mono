# Generated by Django 2.2.13 on 2020-08-11 22:10

import jaspr.apps.common.fields.encrypted_boolean_field
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kiosk", "0012_auto_20200810_1505"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assessment",
            name="jaspr_recommend",
            field=jaspr.apps.common.fields.encrypted_boolean_field.EncryptedBooleanField(
                null=True
            ),
        ),
        migrations.AlterField(
            model_name="historicalassessment",
            name="jaspr_recommend",
            field=jaspr.apps.common.fields.encrypted_boolean_field.EncryptedBooleanField(
                null=True
            ),
        ),
    ]
