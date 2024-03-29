# Generated by Django 2.2.24 on 2021-08-18 00:18

from django.db import migrations
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0058_assessmentlocks_acknowledged'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpatientsession',
            name='crisis_stability_plan_status',
            field=fernet_fields.fields.EncryptedCharField(blank=True, choices=[('Not Assigned', 'Not Assigned'), ('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Updated', 'Updated')], max_length=20, null=True, verbose_name='Crisis Stability Plan Status'),
        ),
        migrations.AddField(
            model_name='historicalpatientsession',
            name='crisis_stability_plan_status_timestamp',
            field=fernet_fields.fields.EncryptedDateTimeField(blank=True, null=True, verbose_name='Crisis Stability Plan Status Change Timestamp'),
        ),
        migrations.AddField(
            model_name='historicalpatientsession',
            name='jah_setup_timestampt',
            field=fernet_fields.fields.EncryptedDateTimeField(blank=True, null=True, verbose_name='JAH Setup Timestamp'),
        ),
        migrations.AddField(
            model_name='historicalpatientsession',
            name='lethal_means_status',
            field=fernet_fields.fields.EncryptedCharField(blank=True, choices=[('Not Assigned', 'Not Assigned'), ('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20, null=True, verbose_name='Lethal Means Status'),
        ),
        migrations.AddField(
            model_name='historicalpatientsession',
            name='lethal_means_status_timestamp',
            field=fernet_fields.fields.EncryptedDateTimeField(blank=True, null=True, verbose_name='Lethal Means Status Change Timestamp'),
        ),
        migrations.AddField(
            model_name='historicalpatientsession',
            name='review_status',
            field=fernet_fields.fields.EncryptedCharField(blank=True, choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20, null=True, verbose_name='Review Status'),
        ),
        migrations.AddField(
            model_name='historicalpatientsession',
            name='review_status_timestamp',
            field=fernet_fields.fields.EncryptedDateTimeField(blank=True, null=True, verbose_name='Review Status Change Timestamp'),
        ),
        migrations.AddField(
            model_name='historicalpatientsession',
            name='srat_status',
            field=fernet_fields.fields.EncryptedCharField(blank=True, choices=[('Not Assigned', 'Not Assigned'), ('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Updated', 'Updated')], max_length=20, null=True, verbose_name='SSI Status'),
        ),
        migrations.AddField(
            model_name='historicalpatientsession',
            name='srat_status_timestamp',
            field=fernet_fields.fields.EncryptedDateTimeField(blank=True, null=True, verbose_name='SSI Status Change Timestamp'),
        ),
        migrations.AddField(
            model_name='patientsession',
            name='crisis_stability_plan_status',
            field=fernet_fields.fields.EncryptedCharField(blank=True, choices=[('Not Assigned', 'Not Assigned'), ('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Updated', 'Updated')], max_length=20, null=True, verbose_name='Crisis Stability Plan Status'),
        ),
        migrations.AddField(
            model_name='patientsession',
            name='crisis_stability_plan_status_timestamp',
            field=fernet_fields.fields.EncryptedDateTimeField(blank=True, null=True, verbose_name='Crisis Stability Plan Status Change Timestamp'),
        ),
        migrations.AddField(
            model_name='patientsession',
            name='jah_setup_timestamp',
            field=fernet_fields.fields.EncryptedDateTimeField(blank=True, null=True, verbose_name='JAH Setup Timestamp'),
        ),
        migrations.AddField(
            model_name='patientsession',
            name='lethal_means_status',
            field=fernet_fields.fields.EncryptedCharField(blank=True, choices=[('Not Assigned', 'Not Assigned'), ('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20, null=True, verbose_name='Lethal Means Status'),
        ),
        migrations.AddField(
            model_name='patientsession',
            name='lethal_means_status_timestamp',
            field=fernet_fields.fields.EncryptedDateTimeField(blank=True, null=True, verbose_name='Lethal Means Status Change Timestamp'),
        ),
        migrations.AddField(
            model_name='patientsession',
            name='review_status',
            field=fernet_fields.fields.EncryptedCharField(blank=True, choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20, null=True, verbose_name='Review Status'),
        ),
        migrations.AddField(
            model_name='patientsession',
            name='review_status_timestamp',
            field=fernet_fields.fields.EncryptedDateTimeField(blank=True, null=True, verbose_name='Review Status Change Timestamp'),
        ),
        migrations.AddField(
            model_name='patientsession',
            name='srat_status',
            field=fernet_fields.fields.EncryptedCharField(blank=True, choices=[('Not Assigned', 'Not Assigned'), ('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Updated', 'Updated')], max_length=20, null=True, verbose_name='SSI Status'),
        ),
        migrations.AddField(
            model_name='patientsession',
            name='srat_status_timestamp',
            field=fernet_fields.fields.EncryptedDateTimeField(blank=True, null=True, verbose_name='SSI Status Change Timestamp'),
        ),
    ]
