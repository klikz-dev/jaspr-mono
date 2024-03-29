# Generated by Django 2.2.13 on 2021-01-20 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0027_merge_20201216_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltechnician',
            name='role',
            field=models.CharField(blank=True, default='', help_text="This is the technician's role or title at the assigned clinic", max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='technician',
            name='role',
            field=models.CharField(blank=True, default='', help_text="This is the technician's role or title at the assigned clinic", max_length=256, null=True),
        ),
    ]
