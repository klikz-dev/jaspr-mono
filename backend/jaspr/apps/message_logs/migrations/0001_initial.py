# Generated by Django 2.2.13 on 2020-06-19 21:32

import django.db.models.deletion
import django.utils.timezone
import fernet_fields.fields
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SMSLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "mobile_phone",
                    fernet_fields.fields.EncryptedCharField(
                        help_text="The phone number (encrypted) of the user the time message delivery was first attempted.",
                        max_length=15,
                    ),
                ),
                (
                    "title",
                    models.TextField(
                        help_text="Not sent to the user. A helpful description for use in filtering, sorting, searching logs, etc."
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        help_text="The actual body/text of the text message sent to the user."
                    ),
                ),
                (
                    "message_id",
                    models.CharField(
                        blank=True,
                        help_text="The message SID from Twilio.",
                        max_length=256,
                    ),
                ),
                (
                    "status",
                    model_utils.fields.StatusField(
                        choices=[
                            ("pending", "pending"),
                            ("sent", "sent"),
                            ("retry", "retry"),
                            ("failed", "failed"),
                        ],
                        default="pending",
                        help_text="Used internally to handle retrying of text messages that didn't send and mark sent messages. Don't change unless you know what you're doing.",
                        max_length=30,
                        no_check_for_status=True,
                    ),
                ),
                (
                    "sent",
                    model_utils.fields.MonitorField(
                        blank=True,
                        default=None,
                        help_text="The time the text message was sent. If it hasn't been sent, this will be `None`.",
                        monitor="status",
                        null=True,
                        when={"sent"},
                    ),
                ),
                (
                    "times_retried",
                    models.IntegerField(
                        default=0,
                        help_text="The number of times the code has retried sending the text message due to some error/exception. The last attempted send time should be the `updated` field.",
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        help_text="The user that was texted.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "SMS Log",
                "verbose_name_plural": "SMS Logs",
                "get_latest_by": "created",
            },
        ),
        migrations.CreateModel(
            name="EmailLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "user_email",
                    models.EmailField(
                        help_text="The email of the user at the time the email delivery was attempted.",
                        max_length=254,
                    ),
                ),
                (
                    "from_email",
                    models.EmailField(
                        help_text="The email address that the email was sent from. Introduced because Jaspr can have different sending emails.",
                        max_length=254,
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        blank=True,
                        help_text="The specific time the email delivery was attempted.",
                        null=True,
                    ),
                ),
                ("subject", models.TextField(help_text="The subject of the email.")),
                (
                    "text_body",
                    models.TextField(
                        help_text="The text body of the email. Used if the html body isn't present or the email is viewed with an email client that doesn't support HTML."
                    ),
                ),
                (
                    "html_body",
                    models.TextField(
                        blank=True,
                        help_text="The html body of the email. Used if present and the email is viewed with an email client that supports HTML.",
                    ),
                ),
                (
                    "email_response",
                    models.TextField(
                        blank=True,
                        help_text="The response from Django's `send_mail` function. Currently returns the number of emails successfully delivered (I.E. '0' or '1').",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="The user that was emailed.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Email Log",
                "verbose_name_plural": "Email Logs",
                "get_latest_by": "date",
            },
        ),
    ]
