# Generated by Django 3.0.14 on 2022-02-16 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jah', '0003_historicalprivacypolicyacceptance_privacypolicyacceptance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commonconcern',
            options={'ordering': ['order'], 'verbose_name': 'Common Concern', 'verbose_name_plural': 'Common Concerns'},
        ),
        migrations.AlterModelOptions(
            name='conversationstarter',
            options={'ordering': ['order'], 'verbose_name': 'Conversation Starter', 'verbose_name_plural': 'Conversation Starters'},
        ),
        migrations.AlterModelOptions(
            name='patientcopingstrategy',
            options={'ordering': ['title'], 'verbose_name': 'Patient Coping Strategy', 'verbose_name_plural': 'Patient Coping Strategies'},
        ),
    ]