from django.db import models
from fernet_fields import EncryptedCharField
from jaspr.apps.accounts.models import User
from jaspr.apps.common.models import JasprAbstractBaseModel
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField


class EmailLog(JasprAbstractBaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user that was emailed."
    )
    # This is the recorded email when the email was sent. The user
    # since could have changed his/her email.
    user_email = models.EmailField(
        help_text="The email of the user at the time the email delivery was attempted."
    )
    from_email = models.EmailField(
        help_text="The email address that the email was sent from. Introduced because Jaspr can have different sending emails."
    )
    date = models.DateTimeField(
        help_text="The specific time the email delivery was attempted.",
        null=True,
        blank=True,
    )
    subject = models.TextField(help_text="The subject of the email.")
    text_body = models.TextField(
        help_text="The text body of the email. Used if the html body isn't present or the email is viewed with an email client that doesn't support HTML."
    )
    html_body = models.TextField(
        blank=True,
        help_text="The html body of the email. Used if present and the email is viewed with an email client that supports HTML.",
    )
    email_response = models.TextField(
        blank=True,
        help_text="The response from Django's `send_mail` function. Currently returns the number of emails successfully delivered (I.E. '0' or '1').",
    )

    # Don't want to inherit the `status` field from the abstract parent.
    status = None

    class Meta:
        verbose_name = "Email Log"
        verbose_name_plural = "Email Logs"
        get_latest_by = "date"

    def __str__(self):
        return f"To user id {self.user_id} ({self.user_email}) on {self.date} (Log ID: {self.id})."


class SMSLog(JasprAbstractBaseModel):
    STATUS = Choices("pending", "sent", "retry", "failed")

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user that was texted."
    )
    mobile_phone = EncryptedCharField(
        max_length=15,
        help_text="The phone number (encrypted) of the user the time message delivery was first attempted.",
    )
    title = models.TextField(
        help_text="Not sent to the user. A helpful description for use in filtering, sorting, searching logs, etc."
    )
    body = models.TextField(
        help_text="The actual body/text of the text message sent to the user."
    )
    message_id = models.CharField(
        max_length=256, blank=True, help_text="The message SID from Twilio."
    )
    # NOTE: `StatusField` sets the default to the first choice which should be `pending`.
    status = StatusField(
        max_length=30,
        help_text="Used internally to handle retrying of text messages that didn't send and mark sent messages. Don't change unless you know what you're doing.",
    )
    sent = MonitorField(
        monitor="status",
        when=["sent"],
        null=True,
        default=None,
        blank=True,
        help_text="The time the text message was sent. If it hasn't been sent, this will be `None`.",
    )
    times_retried = models.IntegerField(
        default=0,
        help_text="The number of times the code has retried sending the text message due to some error/exception. The last attempted send time should be the `updated` field.",
    )

    class Meta:
        verbose_name = "SMS Log"
        verbose_name_plural = "SMS Logs"
        # NOTE: In Django 2.0, we can pass a list here and do something like
        # ['created', 'sent'] if we wanted to.
        get_latest_by = "created"

    def __str__(self):
        return f"To user id {self.recipient_id} at {self.created} (status: {self.status}) (Log ID: {self.id})."
