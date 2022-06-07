# Generated by Django 2.2.13 on 2020-09-04 17:57
import uuid
from itertools import chain

from django.db import migrations


def set_patient_and_technician_analytics_token_uuid(apps, schema_editor):
    Patient = apps.get_model("kiosk", "Patient")
    Technician = apps.get_model("kiosk", "Technician")
    for instance in chain(Patient.objects.iterator(), Technician.objects.iterator()):
        instance.analytics_token = uuid.uuid4()
        instance.save(update_fields=["analytics_token"])


class Migration(migrations.Migration):

    dependencies = [
        ("kiosk", "0016_auto_20200904_1057"),
    ]

    operations = [migrations.RunPython(set_patient_and_technician_analytics_token_uuid)]