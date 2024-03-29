# Generated by Django 2.2.13 on 2020-12-15 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kiosk", "0024_auto_20201006_1758"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessment",
            name="interview_progress_section",
            field=models.CharField(
                choices=[
                    ("Initial", "Initial"),
                    ("SSF-A/B", "SSF-A/B"),
                    ("Lethal Means", "Lethal Means"),
                    ("Plan to Cope", "Plan to Cope"),
                ],
                default="Initial",
                max_length=12,
                verbose_name="Interview Progress Section",
            ),
        ),
        migrations.AddField(
            model_name="historicalassessment",
            name="interview_progress_section",
            field=models.CharField(
                choices=[
                    ("Initial", "Initial"),
                    ("SSF-A/B", "SSF-A/B"),
                    ("Lethal Means", "Lethal Means"),
                    ("Plan to Cope", "Plan to Cope"),
                ],
                default="Initial",
                max_length=12,
                verbose_name="Interview Progress Section",
            ),
        ),
    ]
