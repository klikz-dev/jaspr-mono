# Generated by Django 2.2.19 on 2021-05-07 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_manual_current_security_chars'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='securityquestion',
            name='user',
        ),
        migrations.DeleteModel(
            name='HistoricalSecurityQuestion',
        ),
        migrations.DeleteModel(
            name='SecurityQuestion',
        ),
    ]
