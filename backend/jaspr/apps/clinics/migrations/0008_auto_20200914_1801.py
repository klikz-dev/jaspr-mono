# Generated by Django 2.2.13 on 2020-09-14 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clinics", "0007_custom_update_orphaned_historicalclinics"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clinic",
            name="organization_code",
            field=models.SlugField(
                help_text="Code used in subdomain of clinic portal.", unique=True
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinic",
            name="organization_code",
            field=models.SlugField(
                help_text="Code used in subdomain of clinic portal."
            ),
        ),
    ]
