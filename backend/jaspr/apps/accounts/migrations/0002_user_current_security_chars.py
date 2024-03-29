# Generated by Django 2.2.13 on 2020-07-31 21:59

import fernet_fields.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="current_security_chars",
            field=fernet_fields.fields.EncryptedCharField(
                default="ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24ab24",
                editable=False,
                help_text="This is a 'hidden' field that shouldn't show up in the admin or anywhere else. It is used for making the activation, setup, and reset password token flows more secure.",
                max_length=100,
                verbose_name="Current Security Chars",
            ),
            preserve_default=False,
        ),
    ]
