# Generated by Django 3.1.14 on 2022-02-17 00:06

from django.db import migrations, models
import jaspr.apps.common.fields.encrypted_array_field


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0067_auto_20220110_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crisisstabilityplan',
            name='supportive_people',
            field=jaspr.apps.common.fields.encrypted_array_field.EncryptedArrayField(base_field=models.JSONField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='historicalcrisisstabilityplan',
            name='supportive_people',
            field=jaspr.apps.common.fields.encrypted_array_field.EncryptedArrayField(base_field=models.JSONField(), blank=True, null=True, size=None),
        ),
    ]