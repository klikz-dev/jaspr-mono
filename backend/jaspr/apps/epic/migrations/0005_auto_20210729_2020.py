# Generated by Django 2.2.24 on 2021-07-30 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epic', '0004_auto_20210610_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epicdepartmentsettings',
            name='location_code',
            field=models.CharField(blank=True, help_text='Key used to determine the location during oauth', max_length=64, null=True, unique=True, verbose_name='Location Code (FHIR ID)'),
        ),
    ]
