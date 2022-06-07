# Generated by Django 2.2.13 on 2020-08-04 15:13

from django.db import migrations
from django.db.models import F


def set_technician_last_activated_at(apps, schema_editor):
    Technician = apps.get_model("kiosk", "Technician")

    Technician.objects.filter(activated=True).update(
        last_activated_at=F("first_activated_at")
    )


class Migration(migrations.Migration):

    dependencies = [
        ("kiosk", "0010_auto_20200804_0813"),
    ]

    operations = [migrations.RunPython(set_technician_last_activated_at, elidable=True)]
