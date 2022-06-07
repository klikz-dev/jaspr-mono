from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from fernet_fields import EncryptedCharField
from jaspr.apps.common.fields import EncryptedPhoneNumberField
from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel
from knox.settings import CONSTANTS as KNOX_CONSTANTS
from model_utils import Choices
from simple_history.models import HistoricalRecords

from .security import generate_multiple_unique_secure_random_strings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Basic user account."""

    ALL_MESSAGE_TYPES = ("email", "sms")
    PREFERRED_MESSAGE_TYPES = (
        ("email", "Email"),
        ("sms", "Text Message"),
        ("email and sms", "Email and Text Message"),
    )
    SECURITY_CHARS_MAX_LENGTH: int = 100

    # NOTE: `email`, `is_staff`, `is_active`, and `date_joined` copied over from
    # `django-authtools`'s `AbstractEmailUser`
    # (https://github.com/fusionbox/django-authtools/blob/6ea614ed2bba56cd8fa7209896b0e20cba45b367/authtools/models.py#L27).
    email = models.EmailField("Email Address", max_length=255, unique=True)
    is_staff = models.BooleanField(
        "Is Staff?",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "Is Active?",
        default=True,
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField("Date Joined", default=timezone.now)

    password_changed = models.DateTimeField(
        "Password Last Changed At", default=timezone.now, null=True, blank=True
    )
    account_locked_at = models.DateTimeField("Account Locked At", null=True, blank=True)
    password_complex = models.BooleanField("Password Complex?", default=False)
    mobile_phone = EncryptedPhoneNumberField("Mobile Phone", blank=True)
    # * NOTE/TODO: At the time of writing, not in use. I think worth keeping in though?
    # * Assuming Jaspr notifications come up? Or are we going to just push notify?
    preferred_message_type = models.CharField(
        "Preferred Message Type",
        max_length=35,
        choices=PREFERRED_MESSAGE_TYPES,
        default="email",
        blank=True,
    )

    current_security_chars = EncryptedCharField(
        "Current Security Chars",
        max_length=SECURITY_CHARS_MAX_LENGTH,
        editable=False,
        help_text=(
            "This is a 'hidden' field that shouldn't show up in the admin or anywhere else. "
            "It is used for making the activation, setup, and reset password token flows more "
            "secure."
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        if (
            not self.current_security_chars
            or len(self.current_security_chars) != self.SECURITY_CHARS_MAX_LENGTH
        ):
            self.generate_and_set_current_security_chars()
        self.email = self.email.casefold()
        return super().save(*args, **kwargs)

    def get_full_name(self) -> str:
        return self.email

    def get_short_name(self) -> str:
        return self.email

    def set_password(self, raw_password: str) -> None:
        super().set_password(raw_password)

        self.generate_and_set_current_security_chars()

    def generate_and_set_current_security_chars(self) -> None:
        # Grab `4` unique random strings each of length `25`.
        security_chars_list = generate_multiple_unique_secure_random_strings(4, 25)
        security_chars = "".join(security_chars_list)
        assert (
            isinstance(security_chars, str)
            and len(security_chars) == self.SECURITY_CHARS_MAX_LENGTH
        )
        self.current_security_chars = security_chars

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this `User`."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # * NOTE/TODO: This seems safe to do for now and enhances performance and all tests
    # * pass. However, could potentially run into issues in a debugger if evaluated in
    # * variables # pane before actually being evaluated in a regular run in the code.
    @cached_property
    def group_names(self):
        return self.groups.all().values_list("name", flat=True)

    # * NOTE/TODO: Same as in `group_names` above.
    @cached_property
    def is_technician(self):
        return settings.TECHNICIAN_GROUP_NAME in self.group_names

    # * NOTE/TODO: Same as in `group_names` above.
    @cached_property
    def is_patient(self):
        return settings.PATIENT_GROUP_NAME in self.group_names

    @cached_property
    def system(self):
        if self.is_patient and hasattr(self, "patient"):
            return self.patient.current_encounter.department.clinic.system
        elif self.is_technician and hasattr(self, "technician"):
            return self.technician.system
        else:
            return None

    @cached_property
    def clinic(self):
        if self.is_patient and hasattr(self, "patient"):
            return self.patient.current_encounter.department.clinic
        return None

    @cached_property
    def department(self):
        if self.is_patient and hasattr(self, "patient"):
            return self.patient.current_encounter.department
        return None

    def add_to_preferred_message_type(
        self, message_type: str, db_save: bool = True
    ) -> None:
        if message_type not in self.ALL_MESSAGE_TYPES:
            raise ValueError(
                f"Provided `message_type` {message_type} not in {self.ALL_MESSAGE_TYPES}"
            )
        if message_type == "email":
            if "sms" in self.preferred_message_type:
                self.preferred_message_type = "email and sms"
            else:
                self.preferred_message_type = "email"
        elif message_type == "sms":
            if "email" in self.preferred_message_type:
                self.preferred_message_type = "email and sms"
            else:
                self.preferred_message_type = "sms"
        if db_save:
            self.save()

    def remove_from_preferred_message_type(
        self, message_type: str, db_save: bool = True
    ) -> None:
        if message_type not in self.ALL_MESSAGE_TYPES:
            raise ValueError(
                f"Provided `message_type` {message_type} not in {self.ALL_MESSAGE_TYPES}"
            )
        if message_type == "email":
            if "sms" in self.preferred_message_type:
                self.preferred_message_type = "sms"
            else:
                self.preferred_message_type = ""
        elif message_type == "sms":
            if "email" in self.preferred_message_type:
                self.preferred_message_type = "email"
            else:
                self.preferred_message_type = ""
        if db_save:
            self.save()


class LogUserLoginAttempts(models.Model):
    """
    Log user interaction with api-auth-token, used for tracking ip address and
    failed password attempts.

    Attributes:
        date_time (TYPE): Description
        ip_address (TYPE): Description
        locked_out (TYPE): Description
        user (TYPE): Description
        was_successful (TYPE): Description
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True)
    was_successful = models.BooleanField()
    locked_out = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Log"
        verbose_name_plural = "User Logs"

    def __str__(self):
        return "%s, %s, %s, %s" % (
            self.id,
            self.ip_address,
            self.was_successful,
            self.date_time,
        )


class LoggedOutAuthToken(models.Model):
    """
    Holds old (deleted) expiring auth token digests (and token keys) for
    users that have logged out. This table should be cleaned regularly.
    """

    user = models.ForeignKey(
        User, related_name="+", verbose_name="User", on_delete=models.CASCADE
    )
    digest = models.CharField(
        max_length=KNOX_CONSTANTS.DIGEST_LENGTH, verbose_name="Digest"
    )
    token_key = models.CharField(
        max_length=KNOX_CONSTANTS.TOKEN_KEY_LENGTH, verbose_name="Token Key"
    )
    logged_out_at = models.DateTimeField(verbose_name="Logged Out At")

    class Meta:
        verbose_name = "Logged Out Expiring Token"
        verbose_name_plural = "Logged Out Expiring Tokens"

    def __str__(self):
        return f"{self.digest}, {self.token_key}, {self.logged_out_at}"
