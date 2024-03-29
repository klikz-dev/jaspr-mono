# Generated by Django 2.2.24 on 2021-09-09 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epic', '0010_auto_20210909_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='epicsettings',
            name='authorize_url',
        ),
        migrations.RemoveField(
            model_name='epicsettings',
            name='fhir_version',
        ),
        migrations.RemoveField(
            model_name='epicsettings',
            name='metadata',
        ),
        migrations.RemoveField(
            model_name='epicsettings',
            name='private_key',
        ),
        migrations.RemoveField(
            model_name='epicsettings',
            name='public_key',
        ),
        migrations.RemoveField(
            model_name='epicsettings',
            name='token_url',
        ),
        migrations.AddField(
            model_name='epicsettings',
            name='name',
            field=models.CharField(default='NAME', help_text='Label for this Epic instance', max_length=50, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
