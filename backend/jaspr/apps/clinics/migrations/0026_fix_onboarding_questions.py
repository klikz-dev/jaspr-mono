# Generated by Django 2.2.24 on 2021-06-10 18:57

from django.db import migrations


def update_departments(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0025_fix_dept_tech_ids'),
    ]

    operations = [
        migrations.RunPython(update_departments),
    ]
