# Generated by Django 2.2.24 on 2021-10-11 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0062_merge_20210831_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='crisisstabilityplan',
            name='note_generated',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Last Note Generated Time'),
        ),
        migrations.AddField(
            model_name='historicalcrisisstabilityplan',
            name='note_generated',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Last Note Generated Time'),
        ),
        migrations.AddField(
            model_name='historicalsrat',
            name='note_generated',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Last Note Generated Time'),
        ),
        migrations.AddField(
            model_name='srat',
            name='note_generated',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Last Note Generated Time'),
        ),
    ]