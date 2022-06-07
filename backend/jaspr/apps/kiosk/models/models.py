from __future__ import annotations

import logging
import uuid
from datetime import date, timedelta
from typing import List, Literal, Optional, Tuple, Union

from colorful.fields import RGBColorField
from django.apps import apps
from django.conf import settings

from django.core.validators import (
    MaxValueValidator,
    RegexValidator,
    ValidationError,
)
from django.db import models, transaction
from django.db.models import OuterRef, Prefetch, Q, Subquery

from django.utils import timezone
from django.utils.functional import cached_property
from fernet_fields import (
    EncryptedCharField,
    EncryptedDateField,
)
from knox.models import AuthToken
from model_utils import Choices
from model_utils.fields import AutoCreatedField, MonitorField
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from jaspr.apps.accounts.models import User
from jaspr.apps.common.constraints import EnhancedUniqueConstraint

from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel

from .patient_department_sharing import PatientDepartmentSharing
from ...awsmedia.models import Media, PrivacyScreenImage
from ..constants import ActionNames
from ..validators import (
    validate_action_that_is_jah_only,
    validate_action_with_extra,
    validate_action_with_section_uid,
)
from ...clinics.models import Department, Clinic, HealthcareSystem

logger = logging.getLogger(__name__)

JasprUserTypeString = Literal["Technician", "Patient"]


class Helpline(JasprAbstractBaseModel):
    STATUS = Choices(
        ("active", "Active"),
    )
    name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    text = models.CharField(max_length=25)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Helpline"
        verbose_name_plural = "Helplines"

    def __str__(self):
        return self.name


class CopingStrategyCategory(JasprAbstractBaseModel):
    """ Categories for Coping Strategies"""

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    why_text = models.TextField(
        blank=True,
        help_text="Text that will appear after clicking 'The why behind this'",
    )

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Coping Strategy Category"
        verbose_name_plural = "Coping Strategy Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class CopingStrategy(JasprAbstractBaseModel):
    """ Coping Strategies """

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Administrative name.",
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        help_text="Public title of this coping strategy, currently used to connect frontend to backend as a key.",
    )
    image = models.ImageField()
    category = models.ForeignKey(CopingStrategyCategory, on_delete=models.PROTECT)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Coping Strategy"
        verbose_name_plural = "Coping Strategies"
        ordering = ["title"]

    def __str__(self):
        return self.name


class GuideMessage(JasprAbstractBaseModel):
    STATUS = Choices(
        ("active", "Active"),
    )
    name = models.CharField(
        max_length=100, unique=True, help_text="Administrative name."
    )
    message = models.TextField(
        blank=True,
        help_text="Text that will appear after clicking 'The why behind this'",
    )

    class Meta:
        verbose_name = "Guide Message"
        verbose_name_plural = "Guide Messages"
        ordering = ["name"]

    history = HistoricalRecords(bases=[RoutableModel])

    def __str__(self):
        return self.name


class Technician(JasprAbstractBaseModel):

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    user = models.OneToOneField(
        User, related_name="technician", on_delete=models.CASCADE, verbose_name="User"
    )
    system = models.ForeignKey(
        "clinics.HealthcareSystem",
        on_delete=models.PROTECT,
        verbose_name="Healthcare System",
    )
    role = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        default="",
        help_text="This is the technician's role or title at the assigned clinic",
    )

    fhir_id = models.CharField(max_length=256, verbose_name="FHIR IDs", null=True, blank=True)

    first_name = models.CharField(blank=True, null=True, max_length=150, default="")
    last_name = models.CharField(blank=True, null=True, max_length=150, default="")

    primary_department = models.ForeignKey(
        "clinics.Department",
        on_delete=models.PROTECT,
        verbose_name="Primary Department",
        blank=True,
        null=True,
    )

    activation_email_last_sent_at = models.DateTimeField(
        "Activation Email Last Sent At", blank=True, null=True
    )
    activated = models.BooleanField("Activated", default=False)
    first_activated_at = MonitorField(
        "First Activated At",
        monitor="activated",
        when=[True],
        null=True,
        default=None,
        blank=True,
        editable=False,
        help_text="The time the Technician was first activated at.",
    )
    last_activated_at = models.DateTimeField(
        "Last Activated At",
        null=True,
        default=None,
        blank=True,
        help_text="The time the Technician was last activated at.",
    )
    analytics_token = models.UUIDField(
        "Analytics Token", unique=True, editable=False, default=uuid.uuid4
    )
    training_complete = models.BooleanField(verbose_name="Education/Training Completed", default=False,
                                            help_text="Has the technician completed their Jaspr education and training?")
    coach_modeling_complete = models.BooleanField(verbose_name="Jaspr Coach Modeling", default=False,
                                                  help_text="Has this technician been provided with \"At Elbow\" support by a Jaspr Coach?")
    practice_with_support_complete = models.BooleanField(verbose_name="Practice with Support", default=False,
                                                         help_text="Has the technician shared positive feedback")

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Technician"
        verbose_name_plural = "Technicians"

    def __str__(self):
        return f"Technician: {self.last_name}, {self.first_name} ({self.user.email})"


class Patient(JasprAbstractBaseModel):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))
    # NOTE: Leaving first elements of tuples capitalized because
    # it makes more sense for frontend given that these are names
    # and the serializer(s) will hand over the first value of the tuple
    # by default.
    GUIDE_CHOICES = Choices(("Jaz", "Jaz"), ("Jasper", "Jasper"))

    TOOLS_TO_GO_NOT_STARTED = "Not Started"
    TOOLS_TO_GO_EMAIL_SENT = "Email Sent"
    TOOLS_TO_GO_PHONE_NUMBER_VERIFIED = "Phone Number Verified"
    TOOLS_TO_GO_SETUP_FINISHED = "Setup Finished"
    # The `Choices` are described in the order of the flow
    # for setting up tools to go. "Not Started" is the first,
    # and it ends at "Setup Finished".
    TOOLS_TO_GO_STATUS_CHOICES = Choices(
        TOOLS_TO_GO_NOT_STARTED,
        TOOLS_TO_GO_EMAIL_SENT,
        TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
        TOOLS_TO_GO_SETUP_FINISHED,
    )

    first_name = EncryptedCharField("First Name", blank=True, max_length=150)
    last_name = EncryptedCharField("Last Name", blank=True, max_length=150)
    date_of_birth = EncryptedDateField("Date of Birth", blank=True, null=True)
    mrn = EncryptedCharField(
        "Medical Record Number",
        blank=True,
        max_length=255,
        help_text=(
            "An MRN is constant for one patient to represent them from a clinical data "
            "perspective for their entire life for an individual hospital. However there "
            "may be more than one if hospital transfers are made. It is PID.3 in HL7 "
            "parlance, 'id' on Patient in FHIR. Unique together per clinic. Note this "
            "example: https://www.hl7.org/fhir/patient-example-a.json.html. We're going to"
            "use the value from 'identifier'."
        ),
    )

    user = models.OneToOneField(
        User, related_name="patient", on_delete=models.CASCADE, verbose_name="User"
    )
    beta = models.BooleanField(
        "Can See Beta Questionnaire Versions?",
        default=False,
        help_text=(
            "Designates that this Patient has permission to view test "
            "Questionnaire Versions marked with Beta = True."
        ),
    )

    ssid = models.CharField(
        "SSID",
        max_length=25,
        blank=True,
        null=True,
        default=None,
        unique=True,
        # NOTE: If we ever change the regex validator, at the time of writing the exact
        # same regex shows up in:
        # 1. here
        # 2. `jaspr.apps.api.v1.urls`
        # 3. `jaspr.apps.api.v1.serializers`
        # Make sure to change it in all places if it does change. Also, change
        # `error_messages` to match the `message` below in
        # `jaspr.apps.api.v1.serializers` if it changes.
        validators=[
            RegexValidator(
                regex=r"^[-a-zA-Z0-9_]+\Z",
                message="SSIDs can only contain letters, numbers, hyphens, and underscores.",
            )
        ],
        help_text="This is the subject study id for patients. Set by Technicians upon patient creation/onboarding.",
    )
    guide = models.CharField(
        "Guide",
        max_length=15,
        choices=GUIDE_CHOICES,
        blank=True,
        help_text="This is the currently preferred guide.",
    )

    current_privacy_screen_images = models.ManyToManyField(
        "awsmedia.PrivacyScreenImage",
        help_text="Privacy Screen Images used during validation (must include chosen).",
        blank=True,
        related_name="+",
        verbose_name="Current Privacy Screen Images",
    )

    tour_complete = models.BooleanField(
        "Tour Complete",
        help_text="When a patient has completed the intro tour, this will get marked True.",
        default=False,
    )
    onboarded = models.BooleanField(
        "JAH Onboarding",
        default=False,
        help_text="Has the patient been onboarded (currently in JAH)?",
    )

    tools_to_go_status = models.CharField(
        "Tools to Go Status",
        max_length=31,
        choices=TOOLS_TO_GO_STATUS_CHOICES,
        default=TOOLS_TO_GO_NOT_STARTED,
        help_text=(
            "The current status for tools to go. "
            "The flow starts at 'Not Started' and ends at 'Setup Finished'."
        ),
    )

    ## TODO JACOB Move to JAH Account
    current_walkthrough_step = models.ForeignKey(
        "stability_plan.WalkthroughStep",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Current Walkthrough Step",
        help_text="Most recent stored Walkthrough Step. Can be overridden when field is old.",
    )

    ## TODO JACOB Move to JAH Account
    current_walkthrough_step_changed = MonitorField(
        "Current Walkthrough Step Last Changed At",
        monitor="current_walkthrough_step_id",
        blank=True,
        null=True,
        editable=False,
        help_text="This field changes programatically when current_walkthrough_step is modified.",
    )

    analytics_token = models.UUIDField(
        "Analytics Token", unique=True, editable=False, default=uuid.uuid4
    )

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        # NOTE/TODO: EBPI-866 added some constraints for new `Patient` creation that
        # are in `clean` and should be in associated API endpoint(s). If/once they're
        # really solidified it might be nice to add database constraint(s) here too.
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        if self.ssid:
            return f"{self.__class__.__name__}(pk={self.pk}, ssid={self.ssid})"
        else:
            return (
                f"{self.__class__.__name__}(pk={self.pk}, mrn={self.mrn})"
            )

    def clean(self) -> None:
        self.validate_required_fields_together(
            ssid=self.ssid,
            first_name=self.first_name,
            last_name=self.last_name,
            date_of_birth=self.date_of_birth,
            mrn=self.mrn,
        )

    def save(self, *args, **kwargs):
        # Important: Make sure `ssid` is set to `None` if empty to keep the unique
        # constraint consistent (we don't want the empty string because the database
        # will enforce uniqueness on that).
        self.ssid = self.ssid or None
        creating: bool = False
        if self.pk is None or self._state.adding:
            creating = True
        with transaction.atomic():
            super().save(*args, **kwargs)

            if creating:
                images = PrivacyScreenImage.objects.filter(status="active").order_by(
                    "?"
                )[:3]
                self.current_privacy_screen_images.add(*images)

    @property
    def departments(self):
        result = [pds.department.pk for pds in self.patientdepartmentsharing_set.all() if pds.status == 'active']
        #result = PatientDepartmentSharing.objects.filter(patient=self, status="active").values_list("department", flat=True)
        return result

    @property
    def ssid_string(self) -> str:
        """
        At the time of writing, used in analytics to export `ssid` as the empty
        string instead of `None` when it's not present.
        """
        return self.ssid or ""

    @classmethod
    def get_related_query(cls, query):
        Encounter = apps.get_model('kiosk.Encounter')
        return query.prefetch_related(
            Prefetch(
                "encounter_set",
                queryset=Encounter.objects.filter(id__in=Subquery(
                    Encounter.objects.filter(
                        patient_id=OuterRef('patient_id')
                    ).values_list('id', flat=True)[:1]
                )),
                to_attr='latest_encounter'
            )
        )

    @cached_property
    def current_encounter(self):
        Encounter = apps.get_model("kiosk.Encounter")
        AssignedActivity = apps.get_model('kiosk.AssignedActivity')

        try:
            encounter = (
                Encounter.objects.select_related('department', 'department__clinic',
                                                 'department__clinic__system').prefetch_related(Prefetch(
                    "assignedactivity_set",
                    queryset=AssignedActivity.objects.order_by("-created").select_related(
                        'stability_plan', 'suicide_assessment', 'comfort_and_skills', 'intro', 'outro', 'lethal_means'
                    ).all()
                )).filter(patient=self).order_by("-created")[:1].get()
            )
            return encounter
        except Encounter.DoesNotExist:
            return None


    def get_current_department(self) -> Department:
        encounter = self.current_encounter
        if encounter is not None and encounter.department is not None:
            return encounter.department
        return None

    def get_current_clinic(self) -> Clinic:
        department = self.get_current_department()
        if department is not None:
            return department.clinic
        return None

    def get_current_system(self) -> HealthcareSystem:
        clinic = self.get_current_clinic()
        if clinic is not None:
            return clinic.system
        return None

    def has_internal_email(self):
        return self.user.email.endswith('jaspr@jasprhealth.com')

    @property
    def email(self) -> str:
        return "" if self.has_internal_email() else self.user.email

    @property
    def mobile_phone(self) -> str:
        mobile_phone = self.user.mobile_phone
        return "" if not mobile_phone else mobile_phone.as_e164

    @staticmethod
    def validate_required_fields_together(
        ssid: Optional[str],
        first_name: str,
        last_name: str,
        date_of_birth: Optional[date],
        mrn: str,
    ) -> None:
        if ssid:
            if first_name or last_name or date_of_birth or mrn:
                raise ValidationError(
                    "Patients cannot have an SSID and any of 'First Name', 'Last Name', 'Date of Birth', or 'MRN'."
                )
        elif not (first_name and last_name and date_of_birth and mrn):
            if mrn:
                raise ValidationError(
                    "When MRN is provided 'First Name', 'Last Name', and 'Date of Birth', are required."
                )
            else:
                raise ValidationError(
                    "When SSID is not provided 'First Name', 'Last Name', 'Date of Birth', and 'MRN' are required."
                )


class Amendment(JasprAbstractBaseModel):
    STATUS = Choices(
        ("active", "Active"),
        ("archived", "Archived"),
        # NOTE: At the moment, `"deleted"` means deleted by the `Technician`.
        ("deleted", "Deleted"),
    )

    NOTE_TYPES = Choices(("stability-plan", "Stability Plan"), ("narrative-note", "Narrative Note"))

    encounter = models.ForeignKey("kiosk.Encounter", on_delete=models.CASCADE, null=True, blank=True)

    technician = models.ForeignKey(
        Technician, on_delete=models.CASCADE, verbose_name="Technician"
    )
    note_type = models.CharField("Tag", max_length=31, choices=NOTE_TYPES)
    comment = models.CharField("Comment", max_length=10000)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Amendment"
        verbose_name_plural = "Amendments"

    def __str__(self) -> str:
        field_names = ("technician_id", "created")
        values = tuple(getattr(self, field_name) for field_name in field_names)
        display = tuple(f"{name}={value}" for name, value in zip(field_names, values))
        return f"{self.__class__.__name__}({', '.join(display)})"


class Activity(JasprAbstractBaseModel):

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    name = models.CharField(max_length=150, unique=True)
    video = models.ForeignKey(
        Media, blank=True, default=None, null=True, on_delete=models.SET_NULL
    )
    main_page_image = models.ImageField(
        verbose_name="Main Page Image",
        max_length=510,
        null=True,
        blank=True,
        help_text="High resolution image: Run through tiny png before uploading here.",
    )
    thumbnail_image = models.ImageField(
        verbose_name="Thumbnail Image",
        max_length=510,
        null=True,
        blank=True,
        help_text="High resolution image: Run through tiny png before uploading here.",
    )
    target_url = models.CharField(
        verbose_name="Target URL",
        max_length=150,
        blank=True,
        help_text="This is a relative URL.",
    )
    label_color = RGBColorField(verbose_name="Label Color", blank=True)
    order = models.PositiveSmallIntegerField(verbose_name="Order", default=0)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

        constraints = (
            EnhancedUniqueConstraint(
                fields=["target_url"],
                condition=Q(status="active") & ~Q(target_url=""),
                name="activity_unique_target_url_ignoring_blank",
                description="Target URLs should be unique if not blank.",
            ),
        )

    def __str__(self):
        return self.name


class Person(JasprAbstractBaseModel):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    name = models.CharField("Name", max_length=40, unique=True)
    image_1x = models.ImageField(
        verbose_name="Image @ 1X",
        max_length=510,
        help_text="Low resolution image: Run through tiny png before uploading here.",
    )
    image_2x = models.ImageField(
        verbose_name="Image @ 2X",
        max_length=510,
        help_text="Medium resolution image: Run through tiny png before uploading here.",
    )
    image_3x = models.ImageField(
        verbose_name="Image @ 3X",
        max_length=510,
        help_text="High resolution image: Run through tiny png before uploading here.",
    )
    label_color = RGBColorField(verbose_name="Label Color", blank=True)
    order = models.PositiveSmallIntegerField("Order", default=0)

    history = HistoricalRecords(bases=[RoutableModel])

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"


class Topic(JasprAbstractBaseModel):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    name = models.CharField("Name", unique=True, max_length=40)
    order = models.PositiveSmallIntegerField("Order", unique=True, default=0)
    label_color = RGBColorField(verbose_name="Label Color", blank=True)

    history = HistoricalRecords(bases=[RoutableModel])

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"


class SharedStory(JasprAbstractBaseModel):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    person = models.ForeignKey(Person, on_delete=models.PROTECT, verbose_name="Person")
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, verbose_name="Topic")
    video = models.ForeignKey(
        Media,
        on_delete=models.PROTECT,
        limit_choices_to=Q(file_type="video"),
        verbose_name="Video",
    )
    order = models.PositiveSmallIntegerField("Order", default=0)

    history = HistoricalRecords(bases=[RoutableModel])

    def __str__(self) -> str:
        # NOTE: Potentially nice/helpful for admin, debugging, and other places, but if
        # relevant `select_related` calls aren't applied and/or foreign key instances
        # aren't already fetched, this could generate extra queries.
        return f"{self.person} - {self.topic}"

    class Meta:
        constraints = [
            EnhancedUniqueConstraint(
                fields=["person", "topic"],
                condition=Q(status="Active"),
                name="shared_story_active_unique_together_person_topic",
                description="Active shared stories should have a unique person and topic together.",
            ),
            EnhancedUniqueConstraint(
                fields=["person", "video"],
                condition=Q(status="Active"),
                name="shared_story_active_unique_together_person_video",
                description="Active shared stories should have a unique person and video together.",
            ),
        ]
        verbose_name = "Shared Story"
        verbose_name_plural = "Shared Stories"


class PatientActivity(JasprAbstractBaseModel):

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, verbose_name="Patient"
    )
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(null=True, default=None)
    save_for_later = models.BooleanField("Save For Later", null=True, default=None)
    viewed = models.DateTimeField(null=True, default=None)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Patient Activity"
        verbose_name_plural = "Patient Activities"
        constraints = (
            EnhancedUniqueConstraint(
                fields=["patient", "activity"],
                condition=Q(status="active"),
                name="unique_active_patient_activity",
                description="Can only have one active patient activity at a time.",
            ),
        )

    def __str__(self):
        return f"{self.patient}: {self.activity}"


class PatientVideo(JasprAbstractBaseModel):

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, verbose_name="Patient"
    )
    video = models.ForeignKey(Media, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(null=True, default=None)
    save_for_later = models.BooleanField("Save For Later", null=True, default=None)
    viewed = models.DateTimeField(null=True, default=None)
    progress = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)], default=0
    )

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Patient Video"
        verbose_name_plural = "Patient Videos"
        constraints = (
            EnhancedUniqueConstraint(
                fields=["patient", "video"],
                condition=Q(status="active"),
                name="unique_active_patient_video",
                description="Can only have one active patient video at a time.",
            ),
        )

    def __str__(self):
        return f"{self.patient}: {self.video}"


class Action(JasprAbstractBaseModel):
    STATUS = Choices(("active", "Active"))

    ACTION_CHOICES = Choices(
        (ActionNames.ARRIVE, "Time of arriving @ CAMS section"),
        (ActionNames.CARE_PLANNING_REPORT_CLOSED, "Time user closes Planning Report."),
        (ActionNames.CARE_PLANNING_REPORT_OPEN, "Time user opens Planning Report."),
        (
            ActionNames.EXPLORE,
            "Time of selecting Explore on my own button after tutorial",
        ),
        (
            ActionNames.GUIDE,
            "Time of selecting Continue Guidance button after tutorial",
        ),
        (ActionNames.GUIDE_JASPER, "Time of selecting Jasper as the guide."),
        (ActionNames.GUIDE_JAZ, "Time of selecting Jaz as the guide."),
        (ActionNames.HAMBURGER_CAMS, "Time of selecting CAMS button on hamburger menu"),
        (
            ActionNames.HAMBURGER_CS,
            "Time of selecting comfort and skills button on hamburger menu",
        ),
        (ActionNames.HAMBURGER_HOME, "Time of selecting Home button on hamburger menu"),
        (
            ActionNames.HAMBURGER_MY_ACCOUNT,
            "Time of selecting My Account button on hamburger menu",
        ),
        (
            ActionNames.HAMBURGER_SS,
            "Time of selecting Shared Stories button on hamburger menu",
        ),
        (
            ActionNames.HAMBURGER_TK,
            "Time of selecting Takeaway Kit button on hamburger menu",
        ),
        (
            ActionNames.HAMBURGER_STABILITY_PLAN,
            "Time of selecting Stability Plan button on hamburger menu",
        ),
        (
            ActionNames.HAMBURGER_CONTACTS,
            "Time of selecting Contacts button on hamburger menu",
        ),
        (
            ActionNames.HAMBURGER_WALKTHROUGH,
            "Time of selecting the Distress Survival Guide button on hamburger menu",
        ),
        (ActionNames.INTERVIEW_SUMMARY_CLOSED, "Time user closes Interview Summary."),
        (ActionNames.INTERVIEW_SUMMARY_OPEN, "Time user opens Interview Summary."),
        (ActionNames.LOCKOUT, "Time of lockout (10 min inactivity)"),
        (ActionNames.LOG_OUT_BY_USER, "Time of logout initiated by user"),
        (ActionNames.LOG_OUT_TIMEOUT, "Time of logout (60 min inactivity)"),
        (ActionNames.MENU_CAMS, "Time of selecting CAMS button on side menu"),
        (
            ActionNames.MENU_CS,
            "Time of selecting comfort and skills button on side menu",
        ),
        (ActionNames.MENU_HOME, "Time of selecting Home button on side menu"),
        (ActionNames.MENU_SS, "Time of selecting Shared Stories button on side menu"),
        (ActionNames.MENU_TK, "Time of selecting Takeaway Kit button on side menu"),
        (ActionNames.SESSION_START, "Time of log in initiated by technician"),
        (ActionNames.SKIP_WTE, "Time of pressing 'Skip' before WTE video"),
        (ActionNames.SUBMIT, "Time of submitting CAMS section"),
        (ActionNames.STABILITY_PLAN_CLOSED, "Time user closes Stability Plan."),
        (ActionNames.STABILITY_PLAN_OPEN, "Time user opens Stability Plan."),
        (ActionNames.SUMMARIES_CLOSED, "Time user closes Summaries drawer."),
        (ActionNames.SUMMARIES_OPEN, "Time user opens Summaries drawer."),
        (
            ActionNames.WATCH,
            "Time user finishes (~95% progress at the time of writing) watching a video.",
        ),
        # --- JAH Walkthrough --- #
        (
            ActionNames.JAH_WALKTHROUGH_START,
            "Time user clicks to start the Walkthrough.",
        ),
        (
            ActionNames.JAH_WALKTHROUGH_ARRIVE,
            "Time user arrives at specific content in the Walkthrough.",
        ),
        (
            ActionNames.JAH_WALKTHROUGH_CLICKED_MORE_INFO,
            "Time user clicks more info on a page of the Walkthrough.",
        ),
        (
            ActionNames.JAH_WALKTHROUGH_ARRIVE_RECAP,
            "Time user gets to the list of their steps at the end of the Walkthrough and can choose to go back.",
        ),
        (ActionNames.JAH_WALKTHROUGH_END, "Time user leaves the Walkthrough."),
        # --- JAH Contacts --- #
        (
            ActionNames.JAH_ARRIVE_CONTACTS,
            "Time user goes to their supportive people page.",
        ),
        (
            ActionNames.JAH_ARRIVE_PEOPLE,
            "Time user clicks into page with their supportive people contacts.",
        ),
        (
            ActionNames.JAH_CONTACT_EDITED,
            "Time user edited a supportive contact",
        ),
        (
            ActionNames.JAH_CONTACT_MODIFIED,
            "Time user edited a supportive contact",
        ),
        (
            ActionNames.JAH_CONTACT_DELETED,
            "Time user deleted a supportive contact",
        ),
        (
            ActionNames.JAH_ARRIVE_CONTACT_EDIT,
            "Time user gets to the contact edit page",
        ),
        (
            ActionNames.JAH_ARRIVE_SUPPORTIVE_PERSON,
            "Time user clicks into a specific supportive person from either the home page or the contacts page.",
        ),
        (
            ActionNames.JAH_ARRIVE_CRISIS_LINE,
            "Time user goes to specific crisis line page.",
        ),
        (
            ActionNames.JAH_ARRIVE_PEOPLE_MORE,
            'Time user clicks into "more about supportive people".',
        ),
        (
            ActionNames.JAH_ARRIVE_CONVO_STARTERS,
            'Time user clicks into "Conversation Starters".',
        ),
        (
            ActionNames.JAH_USER_COPY,
            "Time user copies a starter, with the order number of the starter they copied specified.",
        ),
        (
            ActionNames.JAH_ARRIVE_COMMON_CONCERNS,
            'Time user clicks into "Common Concerns".',
        ),
        (
            ActionNames.JAH_OPEN_CONCERN,
            "Time user opens up a common concern, with the order number of the concern they opened specified.",
        ),
        (
            ActionNames.JAH_ARRIVE_SS_SUPPORTIVE_PEOPLE,
            "Time user clicks into Shared Stories: Supportive People.",
        ),
        (
            ActionNames.JAH_ARRIVE_SS_HOTLINES,
            "Time user clicks into Shared Stories: Hotlines.",
        ),
        (
            ActionNames.JAH_CALL_HOTLINE,
            "Time user clicks button to call the hotline (accessible from multiple screens).",
        ),
        (
            ActionNames.JAH_TEXT_HOTLINE,
            "Time user clicks button to text hotline (accessible from multiple screens).",
        ),
        (
            ActionNames.JAH_CALL_SUPPORTIVE_PERSON,
            "Time user clicks button to call a supportive person (accessible from multiple screens).",
        ),
        (
            ActionNames.JAH_TEXT_SUPPORTIVE_PERSON,
            "Time user clicks button to text a supportive person (accessible from multiple screens).",
        ),
    )

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, verbose_name="Patient"
    )
    encounter = models.ForeignKey("kiosk.Encounter", on_delete=models.SET_NULL, null=True, blank=True)

    in_er = models.BooleanField(verbose_name="In Emergency Room?")
    action = models.CharField(
        max_length=63, choices=ACTION_CHOICES, verbose_name="Action"
    )
    screen = models.CharField(
        max_length=63,
        blank=True,
        verbose_name="Screen",
        help_text=(
            "(If relevant) What screen was the user on when the action was taken?"
        ),
    )
    extra = models.CharField(
        max_length=127,
        blank=True,
        verbose_name="Extra",
        help_text=(
            "Some analytics provide extra information. This is where that extra "
            "information gets stored. If it's more than 127 characters, it gets "
            "trimmed down to 127 characters."
        ),
    )
    section_uid = models.CharField(
        max_length=63,
        blank=True,
        verbose_name="Section UID",
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name="Timestamp",
        help_text="The time the action was submitted to the backend.",
        db_index=True,
    )
    client_timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Client Timestamp",
        help_text="The time the client (web browser) said the action occurred at.",
    )

    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"

    def clean(self):
        validate_action_with_section_uid(self.action, self.section_uid)
        validate_action_with_extra(self.action, self.extra)
        validate_action_that_is_jah_only(self.action, self.in_er)

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.action == ActionNames.ARRIVE:
            try:
                self.encounter.update_section_uid(self.section_uid)
            except AttributeError:
                # JAH Users do not have an encounter
                pass


class ActivateRecord(models.Model):
    """
    Stores logs of when a `Technician` activates/logs in a `Patient`.

    NOTE: If we change this model (I.E. adding new fields, changing values in
    migrations, etc.), we should check if we want to add Simple History to this
    if needed.
    """

    technician = models.ForeignKey(
        Technician, on_delete=models.CASCADE, verbose_name="Technician"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, verbose_name="Patient"
    )
    encounter = models.ForeignKey(
        "kiosk.Encounter", null=True, on_delete=models.CASCADE, verbose_name="Encounter"
    )
    timestamp = AutoCreatedField(verbose_name="Timestamp")
    new = models.BooleanField(
        "New?",
        help_text=(
            "Was this from activating a new Patient? Otherwise it'd be from activating "
            "an existing Patient."
        ),
    )

    class Meta:
        verbose_name = "Activate Record"
        verbose_name_plural = "Activate Records"


class JasprSession(models.Model):
    USER_TYPES = Choices(("Technician", "Technician"), ("Patient", "Patient"))

    auth_token = models.OneToOneField(
        AuthToken,
        on_delete=models.CASCADE,
        related_name="jaspr_session",
        related_query_name="jaspr_session",
        verbose_name="Auth Token",
    )
    user_type = models.CharField(
        choices=USER_TYPES, max_length=31, verbose_name="User Type"
    )
    in_er = models.BooleanField(verbose_name="In ER?")
    from_native = models.BooleanField(verbose_name="From Native?")
    long_lived = models.BooleanField(verbose_name="Long Lived?")
    technician_operated = models.BooleanField(verbose_name="Technician operating on behalf of patient?")
    encounter = models.ForeignKey(
        "kiosk.Encounter",
        on_delete=models.CASCADE,
        verbose_name="Encounter",
        default=None,
        null=True,
    )
    '''
    technician_department = models.ForeignKey(
        "clinics.Department",
        
    )
    '''

    class Meta:
        verbose_name = "Jaspr Session"
        verbose_name_plural = "Jaspr Sessions"

    def apply_policies(self) -> None:
        assert (
            self.pk is not None
        ), "Should only call this method once created with a primary key."
        if self.user_type == "Patient" and self.in_er:
            user = self.auth_token.user
            auth_token_pk = self.auth_token.pk
            # If this `JasprSession` is for a `Patient` in the ER, all other
            # `AuthToken`s, and hence `JasprSession`s, should be deleted if they don't
            # match this one. This enforces the single `Patient` ER session at a
            # time policy.
            transaction.on_commit(
                lambda: AuthToken.objects.filter(
                    user=user,
                    jaspr_session__user_type="Patient",
                    jaspr_session__in_er=True,
                )
                .exclude(pk=auth_token_pk)
                .delete()
            )

    @classmethod
    def create(
        cls,
        user: User,
        user_type: JasprUserTypeString,
        in_er: bool,
        from_native: bool,
        long_lived: bool,
        technician_operated: bool = False,
        encounter=None,  # Encounter
        department=None
    ) -> Tuple["JasprSession", str]:
        """
        ! IMPORTANT: This method should be wrapped in `transaction.atomic()` from
        ! somewhere higher up in the call stack.
        """
        if encounter is not None:
            if department is not None:
                assert encounter.department == department, "Encounter department and department argument must match. " \
                                                           "There can be only one valid department at a time. "

            department = encounter.department

        create_parameters = {
            "encounter": encounter,
            "user_type": user_type,
            "in_er": in_er,
            "from_native": from_native,
            "long_lived": long_lived,
            "technician_operated": technician_operated
            #"department": department
        }
        cls.validate_create_parameters(user=user, **create_parameters)
        expiry = cls.expiration_timedelta_for(**create_parameters)
        auth_token, token = AuthToken.objects.create(user, expiry=expiry)
        jaspr_session = cls.objects.create(auth_token=auth_token, **create_parameters)
        jaspr_session.apply_policies()
        return jaspr_session, token

    @staticmethod
    def validate_create_parameters(
        user: User,
        user_type: JasprUserTypeString,
        in_er: bool,
        from_native: bool,
        long_lived: bool,
        technician_operated: bool=False,
        encounter=None,  #: Encounter
    ) -> None:
        error_parameters = {
            "user": user,
            "user_type": user_type,
            "in_er": in_er,
            "from_native": from_native,
            "long_lived": long_lived,
            "technician_operated": technician_operated,
        }
        if user_type == "Technician":
            if not in_er:
                raise JasprSessionUserFacingError(
                    "Technicians can only access Jaspr in the ER right now.",
                    **error_parameters,
                )
            if from_native:
                raise JasprSessionUserFacingError(
                    "Technicians cannot access native Jaspr apps right now.",
                    **error_parameters,
                )
            if long_lived:
                raise JasprSessionError(
                    "Technicians cannot have long lived tokens.",
                    **error_parameters,
                    internal=True,
                )
        if from_native:
            if in_er:
                raise JasprSessionUserFacingError(
                    "Patients cannot access Jaspr in the ER from native apps right now.",
                    **error_parameters,
                )
        if in_er:
            if long_lived:
                raise JasprSessionError(
                    "Patients cannot have long lived tokens in the ER.",
                    **error_parameters,
                    internal=True,
                )

    @classmethod
    def expiration_timedelta_for(
        cls,
        user_type: JasprUserTypeString,
        in_er: bool,
        from_native: bool,
        long_lived: bool,
        technician_operated: bool = False,
        encounter=None,
    ) -> timedelta:
        """
        Important: It is assumed that `validate_create_parameters` is called before
        calling this method in order to make sure the combination of parameters is
        valid for the given user type.
        """
        if user_type == "Technician":
            return settings.IN_ER_TECHNICIAN_DEFAULT_TOKEN_EXPIRES_AFTER
        if in_er:
            return settings.IN_ER_PATIENT_DEFAULT_TOKEN_EXPIRES_AFTER
        if long_lived:
            return settings.AT_HOME_PATIENT_LONG_LIVED_TOKEN_EXPIRES_AFTER
        return settings.AT_HOME_PATIENT_DEFAULT_TOKEN_EXPIRES_AFTER

    @classmethod
    def expiration_min_refresh_interval_for(
        cls,
        user_type: JasprUserTypeString,
        in_er: bool,
        from_native: bool,
        long_lived: bool,
        technician_operated: bool = False,
    ) -> int:
        """
        Important: It is assumed that `validate_create_parameters` is called before
        calling this method in order to make sure the combination of parameters is
        valid for the given user type.
        """
        if user_type == "Technician":
            return settings.IN_ER_TECHNICIAN_DEFAULT_TOKEN_MIN_REFRESH_INTERVAL_SECONDS
        if in_er:
            return settings.IN_ER_PATIENT_DEFAULT_TOKEN_MIN_REFRESH_INTERVAL_SECONDS
        if long_lived:
            return (
                settings.AT_HOME_PATIENT_LONG_LIVED_TOKEN_MIN_REFRESH_INTERVAL_SECONDS
            )
        return settings.AT_HOME_PATIENT_DEFAULT_TOKEN_MIN_REFRESH_INTERVAL_SECONDS


class JasprSessionError(Exception):
    """
    Special note about `internal`: If `True`, it indicates something has probably
    gone wrong internally, and a higher level interface creating or accessing
    `JasprSession`s, etc. may have forgotten to do some basic validation or
    permissions checking, etc. An example is if a 'Patient' `user_type` is
    specified with `in_er=True` and `long_lived=True`. That should never be
    allowed/happen in the code at the time of writing (and no user-facing
    parameters/specifications should ever be able to override that, etc.), so we put
    `internal=True`.
    """

    def __init__(
        self,
        error_message: str,
        *args,
        user: User,
        user_type: JasprUserTypeString,
        in_er: bool,
        from_native: bool,
        long_lived: bool,
        technician_operated: bool = False,
        internal: bool = True,
        **kwargs,
    ):
        self.error_message = error_message
        self.user = user
        self.user_type = user_type
        self.in_er = in_er
        self.from_native = from_native
        self.long_lived = long_lived
        self.technician_operated = technician_operated
        self.internal = internal
        super().__init__(error_message, *args, **kwargs)
        if internal:
            logger.exception(
                "Saw `internal=True` %s for user_id=%d, user_type=%s, in_er=%s, "
                "from_native=%s, long_lived=%s",
                self.__class__.__name__,
                user.id,
                user_type,
                str(in_er),
                str(from_native),
                str(long_lived),
            )


class JasprSessionUserFacingError(JasprSessionError):
    """
    Indicates that it could have been user error (I.E. asking for `long_lived` or
    `from_native` when that might not be allowed for that access point, etc.) that
    caused it, and an appropriate action can be taken to not cause the error to
    happen, etc.
    """

    def __init__(
        self,
        error_message: str,
        *args,
        user: User,
        user_type: JasprUserTypeString,
        in_er: bool,
        from_native: bool,
        long_lived: bool,
        **kwargs,
    ):
        super().__init__(
            error_message,
            *args,
            user=user,
            user_type=user_type,
            in_er=in_er,
            from_native=from_native,
            long_lived=long_lived,
            internal=False,
            **kwargs,
        )
