# Generated by Django 2.2.19 on 2021-04-21 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0012_auto_20210420_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliniclocationtechnician',
            name='fhir_id',
        ),
        migrations.RemoveField(
            model_name='historicalcliniclocationtechnician',
            name='fhir_id',
        ),
    ]
