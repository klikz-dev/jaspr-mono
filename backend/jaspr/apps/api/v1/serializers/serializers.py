import datetime
import logging
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

from django.contrib.auth import authenticate
from django.db import IntegrityError, models, transaction
from django.utils import timezone
from django.utils.functional import cached_property
from djangorestframework_camel_case.util import camelize
from ipware import get_client_ip
from knox.models import AuthToken
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from jaspr.apps.accounts.authentication import log_login_attempt
from jaspr.apps.accounts.models import LogUserLoginAttempts, User
from jaspr.apps.clinics.models import Department
from jaspr.apps.common.functions import check_password_complexity
from jaspr.apps.common.jobs.rq import enqueue_in
from jaspr.apps.common.phonenumbers.verify import (
    VerificationException,
    check_phonenumber_verification,
    send_phonenumber_verification,
)
from jaspr.apps.common.validators import JasprPasswordValidator
from jaspr.apps.kiosk.authentication import login_patient, login_technician
from jaspr.apps.kiosk.emails import (
    send_technician_activation_confirmation_email,
    send_technician_set_password_confirmation_email,
    send_tools_to_go_confirmation_email,
    send_tools_to_go_setup_email,
)
from jaspr.apps.kiosk.jobs import check_and_resend_tools_to_go_setup_email
from jaspr.apps.kiosk.models import (
    Action,
    Activity,
    Amendment,
    CopingStrategy,
    CopingStrategyCategory,
    Encounter,
    GuideMessage,
    Helpline,
    JasprSession,
    Patient,
    PatientActivity,
    PatientVideo,
    Person,
    SharedStory,
    Technician,
    Topic,
)
from jaspr.apps.jah.models import CrisisStabilityPlan, JAHAccount
from jaspr.apps.kiosk.validators import (
    validate_action_that_is_jah_only,
    validate_action_with_extra,
    validate_action_with_section_uid,
)

from ....awsmedia.models import Media, PrivacyScreenImage
from ....jah.models import CommonConcern, ConversationStarter
from ....stability_plan.models import PatientWalkthroughStep
from ..permissions import (
    SatisfiesClinicIPWhitelisting,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from ..serializer_fields import (
    ContextDefault,
    ContextUserDefault,
    CurrentPatientDefault,
    CurrentPatientEncounterDefault,
    CurrentTechnicianDefault,
    ViewedTimestampField,
)
from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from .base import JasprBaseModelSerializer, JasprBaseSerializer

import hmac
from hashlib import md5
from time import time

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponseRedirect
from django.utils.http import urlencode
from django.conf import settings

logger = logging.getLogger(__name__)


class ConversationStarterSerializer(JasprBaseModelSerializer):
    class Meta:
        model = ConversationStarter
        fields = (
            "id",
            "content",
        )


class CommonConcernSerializer(JasprBaseModelSerializer):
    class Meta:
        model = CommonConcern
        fields = (
            "id",
            "title",
            "content",
        )


class LoginBaseSerializer(JasprBaseSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    pre_ip_permission_check: Optional[Callable[[User], bool]] = None
    ip_permission_class: Optional[Type[SatisfiesClinicIPWhitelisting]] = None

    default_error_messages = {
        "ip_not_permitted": "You are not permitted to login from this location."
    }

    def _get_login_attempts(self, user, was_successful, date_time=None):
        # date_time must have a value so if not set by call, set here;
        # cannot set before the call
        if not date_time:
            date_time = timezone.make_aware(
                datetime.datetime.strptime("10/01/15 00:00", "%m/%d/%y %H:%M")
            )

        log = LogUserLoginAttempts.objects.filter(
            user=user, was_successful=was_successful, date_time__gte=date_time
        ).order_by("date_time")

        return log

    def validate_authenticated_user(self, user):
        if not user.is_active:
            return False, False, "User account is disabled."

        if user.account_locked_at:
            reset_time = user.account_locked_at + datetime.timedelta(minutes=30)
            if reset_time < timezone.now():
                user.account_locked_at = None
                user.save()
                return True, False, None
            return False, True, "User account is locked."
        return True, False, None

    def validate_unauthenticated_user(self, credentials):
        user = None
        try:
            user = User.objects.get(email=credentials["email"])
        except User.DoesNotExist:
            pass

        if user is None:
            return user, False, False, "Credentials invalid."

        if user.account_locked_at:
            return user, False, True, "Credentials invalid."

        # Check for lock out conditions
        # Only fails since last successful
        last_success_datetime = list(
            self._get_login_attempts(user.id, was_successful=True)
        )

        if last_success_datetime:
            last_success_datetime = last_success_datetime[-1].date_time
        else:
            last_success_datetime = None

        total_failed_attempts = list(
            self._get_login_attempts(user.id, False, last_success_datetime)
        )

        if len(total_failed_attempts) >= 4:
            # Lock after five attempts, when there are four
            # unsuccessful attempts, that is the 5th attempt
            # since the failed attempt is not logged until after
            # this check
            if (
                    timezone.now() - total_failed_attempts[-1].date_time
            ).seconds / 60 <= 15:
                user.account_locked_at = timezone.now()
                user.save()

            return user, False, True, "Credentials invalid."
        else:
            return user, False, False, "Credentials invalid."

    def validate(self, attrs):
        attrs["email"] = attrs.get("email").casefold()
        credentials = {
            "email": attrs.get("email"),
            "password": attrs.get("password"),
        }

        if not all(credentials.values()):
            msg = "Need both password and user name."
            raise serializers.ValidationError(msg)

        user = authenticate(self.context["request"], **credentials)

        if user:
            # Set the `User` instance on the request so that the permission can
            # retrieve it.
            self.context["request"].user = user
            if (
                    self.ip_permission_class is not None
                    and (
                    self.pre_ip_permission_check is None
                    or self.pre_ip_permission_check(user)
                    )
                    and not self.ip_permission_class().has_permission(
                        self.context["request"], self.context["view"]
                    )
            ):
                self.fail("ip_not_permitted")
            was_successful, locked_out, msg = self.validate_authenticated_user(user)
        else:
            user, was_successful, locked_out, msg = self.validate_unauthenticated_user(
                credentials
            )

        # TODO Should we also log attempts that were not associated with a valid user?
        if user:
            ip = get_client_ip(self.context["request"])[0]
            log_login_attempt(user.pk, ip, was_successful, locked_out)

        if not was_successful:
            raise serializers.ValidationError(msg)

        return {"user": user, **attrs}


class TechnicianUserLoginSerializer(LoginBaseSerializer):
    organization_code = serializers.SlugField(
        max_length=50, required=False, write_only=True
    )

    def pre_ip_permission_check(self, user: User) -> bool:
        return user.is_technician and hasattr(user, "technician")

    ip_permission_class = SatisfiesClinicIPWhitelistingFromTechnician


class PatientUserLoginSerializer(LoginBaseSerializer):
    from_native = serializers.BooleanField(default=False)
    long_lived = serializers.BooleanField(default=False)


class UserTypeMixin(JasprBaseSerializer):
    user_type = serializers.SerializerMethodField()

    def get_user_type(self, obj: models.Model):
        class_name = obj.__class__.__name__
        name = class_name[0].lower() + class_name[1:]
        return [*camelize({name: ""})][0]


class MeTechnicianSerializer(UserTypeMixin, JasprBaseModelSerializer):

    id = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    support_url = serializers.SerializerMethodField()

    def get_id(self, obj: Technician):
        return obj.user.pk

    def get_location(self, obj: Technician) -> Dict[str, Dict[str, Union[str, Type[int]]]]:
        return {
            "system": {
                "name": obj.system.name,
                "id": obj.system_id,
            }
        }

    def get_email(self, obj):
        return obj.user.email

    def get_support_url(self, obj):
        return settings.FRESHDESK_SUPPORT_URL

    class Meta:
        model = Technician
        # NOTE: `id` here corresponds to the user id intentionally right now.
        fields = (
            "id",
            "location",
            "user_type",
            "analytics_token",
            "first_name",
            "last_name",
            "email",
            "role",
            "support_url"
        )
        read_only_fields = (
            "id",
            "user_type",
            "analytics_token",
            "location",
            "role",
            "support_url"
        )


class PrivacyScreenSelectedImageSerializer(JasprBaseModelSerializer):
    """ For setting the active patient privacy screen image. """

    class Meta:
        model = Encounter
        fields = ["privacy_screen_image"]

    extra_kwargs = {"privacy_screen_image": {"write_only": True}}


class MePatientSerializer(UserTypeMixin, JasprBaseModelSerializer):
    id = serializers.SerializerMethodField()
    has_security_steps = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    mobile_phone = serializers.SerializerMethodField()
    # TODO: Remove once the frontend does not need anymore. Check after 03/15/2020.
    # Also remove method and value from `fields` and `read_only_fields`.
    in_er = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()
    technician_operated = serializers.SerializerMethodField()

    def get_id(self, obj: Patient) -> int:
        return obj.user.pk

    # TODO Jacob make context consistent
    def get_has_security_steps(self, obj: Patient) -> bool:
        if "request" in self.context:
            encounter = self.context["request"].auth.jaspr_session.encounter
        else:
            encounter = self.context.get("encounter")

        if encounter:
            return encounter.has_security_steps
        return False

    def get_email(self, obj: Patient) -> str:
        return "" if obj.has_internal_email() else obj.user.email

    def get_mobile_phone(self, obj: Patient) -> str:
        mobile_phone = obj.user.mobile_phone
        return "" if not mobile_phone else mobile_phone.as_e164

    def get_in_er(self, obj: Patient) -> bool:
        context_in_er = self.context.get("in_er")
        if context_in_er is not None:
            return context_in_er
        return self.context["request"].auth.jaspr_session.in_er

    def get_location(self, obj: Patient):
        system = obj.get_current_system()
        clinic = obj.get_current_clinic()
        department = obj.get_current_department()

        if department:
            return {
                "system": {
                    "id": system.id,
                    "name": system.name,
                },
                "clinic": {
                    "id": clinic.id,
                    "name": clinic.name,
                },
                "department": {
                    "id": department.id,
                    "name": department.name,
                },
            }
        return None

    def get_technician_operated(self, obj: Patient):
        if "request" in self.context:
            return self.context["request"].auth.jaspr_session.technician_operated
        return False

    def get_activities(self, obj: Patient):
        ## TODO DeDup with Patient serializer
        encounter = obj.current_encounter
        if encounter:
            return {
                "csa": encounter.has_activity(ActivityType.SuicideAssessment),
                "csp": encounter.has_activity(ActivityType.StabilityPlan),
                "skills": encounter.has_activity(ActivityType.ComfortAndSkills),
            }
        return {
            "csa": None,
            "csp": None,
            "skills": None,
        }


    class Meta:
        model = Patient
        # NOTE: `id` here corresponds to the user id intentionally right now.
        fields = (
            "id",
            "user_type",
            "guide",
            "tour_complete",
            "technician_operated",
            "onboarded",
            "has_security_steps",
            "email",
            "location",
            "mobile_phone",
            "tools_to_go_status",
            "in_er",
            "current_walkthrough_step",
            "current_walkthrough_step_changed",
            "analytics_token",
            "mrn",
            "ssid",
            "date_of_birth",
            "first_name",
            "last_name",
            "activities",
        )
        read_only_fields = (
            "id",
            "user_type",
            "has_security_steps",
            "location",
            "email",
            "mobile_phone",
            "tools_to_go_status",
            "in_er",
            "system",
            "clinic",
            "department",
            "current_walkthrough_step_changed",
            "analytics_token",
            "mrn",
            "ssid",
            "date_of_birth",
            "first_name",
            "last_name",
        )


class JasprSessionCreateSerializer(JasprBaseSerializer):
    # These are optional fields that can be entered in order for the requesting client
    # to specify if the request is coming from a native app, and to ask for a long
    # lived token. They default to `False` if not provided. They can also be overriden
    # from the context, see the `validate` method for more details on that.
    from_native = serializers.BooleanField(default=False)
    long_lived = serializers.BooleanField(default=False)

    def validate(self, attrs: dict) -> dict:
        """
        Validate adds three fields from the context:
        1. `user`
        2. `user_type`
        3. `in_er`

        This can make easy to move and/or perform other validation in here in the
        future if we ever want/need to, and makes it easy to call
        `JasprSession.create(**serializer.validated_data)` directly with the
        validated data.

        The reason we opted to access `user` directly from `self.context['user']`
        instead of from `self.context['request'].user` is in places like `Technician`s
        activating `Patient`s, the `request.user` wouldn't be what we'd want.
        """
        user = self.context.get("user")
        assert user is not None and isinstance(
            user, User
        ), "`user` must be provided in the context and be a valid `User` instance."
        user_type = self.context.get("user_type")
        assert user_type in (
            "Technician",
            "Patient",
        ), "`user_type` must be provided in the context and be a valid value."
        in_er = self.context.get("in_er")
        assert in_er in (
            False,
            True,
        ), "`in_er` must be provided in the context and be a valid boolean."
        # Allow the passed in context to override the provided `from_native` and
        # `long_lived` if specified.
        from_native = attrs["from_native"]
        long_lived = attrs["long_lived"]
        if self.context.get("from_native") is not None:
            from_native = self.context["from_native"]
        if self.context.get("long_lived") is not None:
            long_lived = self.context["long_lived"]
        return {
            "user": user,
            "user_type": user_type,
            "in_er": in_er,
            "from_native": from_native,
            "long_lived": long_lived,
        }

    def create(self, validated_data) -> Tuple[JasprSession, str]:
        user = validated_data["user"]
        user_type = validated_data["user_type"]
        login_kwargs = {
            "request": self.context["request"],
            "log_user_login_attempt": self.context["log_user_login_attempt"],
            "in_er": validated_data["in_er"],
            "from_native": validated_data["from_native"],
            "long_lived": validated_data["long_lived"],
            "save": self.context.get("save", True),
        }
        if user_type == "Technician":
            return login_technician(user.technician, **login_kwargs)
        return login_patient(user.patient, **login_kwargs)


class ReadOnlyJasprSessionSerializer(JasprBaseModelSerializer):
    class Meta:
        model = JasprSession
        fields = ["user_type", "in_er", "from_native", "long_lived", "encounter"]
        read_only_fields = fields


class ReadOnlyAuthTokenSerializer(JasprBaseModelSerializer):
    class Meta:
        model = AuthToken
        # NOTE: See `to_representation` below. The `token`, `session` and either `technician` or
        # `patient` are also included.
        fields = ["expiry"]
        read_only_fields = fields

    def to_representation(self, obj: AuthToken) -> dict:
        representation = super().to_representation(obj)
        user = obj.user
        jaspr_session = obj.jaspr_session
        representation["token"] = self.context["token_string"]
        representation["session"] = ReadOnlyJasprSessionSerializer(jaspr_session).data
        if jaspr_session.user_type == "Technician":
            representation["technician"] = MeTechnicianSerializer(user.technician).data
        else:
            representation["technician_operated"] = jaspr_session.technician_operated
            representation["patient"] = MePatientSerializer(
                user.patient,
                context={
                    "in_er": jaspr_session.in_er,
                    "encounter": jaspr_session.encounter,
                },
            ).data
        return representation


class TechnicianEpicNoteToEhrSerializer(JasprBaseSerializer):
    encounter_id = serializers.IntegerField()


class MediaSerializer(JasprBaseModelSerializer):
    tags = serializers.SerializerMethodField()
    file_field = serializers.SerializerMethodField()

    def get_file_field(self, obj):
        if obj.file_field:
            return obj.file_field.url
        else:
            return ""

    def get_tags(self, obj: Media):
        # Use this method to avoid refetching the tags when they have been prefetched.  See this issue:
        # https://github.com/jazzband/django-taggit/issues/687#issuecomment-819206255
        return [tag.name for tag in obj.tags.all()]


    class Meta:
        model = Media
        fields = (
            "id",
            "name",
            "description",
            "file_field",
            "subtitle_file",
            "transcript",
            "poster",
            "thumbnail",
            "fpm4_transcode",
            "mp4_transcode",
            "mp3_transcode",
            "tips",
            "completion_time",
            "hls_playlist",
            "dash_playlist",
            "duration",
            "file_type",
            "tags",
        )


class TechnicianDepartmentSerializer(JasprBaseSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(status="active")
    )

    default_error_messages = {
        "improper_department": "Submitted department is not one of the available departments for this technician.",
    }

    @cached_property
    def available_department_ids(self):
        if "technician" in self.context:
            technician = self.context["technician"]
        else:
            technician = self.context["request"].user.technician
        available_departments = technician.departmenttechnician_set.filter(
            status="active"
        ).values_list("department", flat=True)
        return available_departments

    def validate_department(
            self, department: Department
    ) -> Department:
        available_department_ids = self.available_department_ids

        if department.pk not in available_department_ids:
            return self.fail("improper_department")

        return department



class ReadOnlyPatientActivitySerializer(JasprBaseModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs["read_only"] = True
        super().__init__(*args, **kwargs)

    class Meta:
        model = PatientActivity
        fields = ["id", "rating", "save_for_later", "viewed"]


class ReadOnlyActivitySerializer(JasprBaseModelSerializer):
    video = MediaSerializer(read_only=True)

    class Meta:
        model = Activity
        # NOTE: See `to_representation` below. The `patient_activity`
        # is also included, and if it's not `None`, then fields from
        # that are flattened into here.
        fields = [
            "id",
            "name",
            "video",
            "main_page_image",
            "thumbnail_image",
            "target_url",
            "label_color",
            "order",
        ]
        read_only_fields = fields

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        # NOTE: We expect a prefetched list of patient activities
        # to the attribute `patient_activities`. Because of unique
        # together constraints, and since `Activity` objects are always
        # retrieved right now from a corresponding authenticated user,
        # we know that this prefetched list has either zero or one instance within it.
        if not obj.patient_activities:
            representation["patient_activity"] = None
            return representation
        nested_data = ReadOnlyPatientActivitySerializer(obj.patient_activities[0]).data
        representation["patient_activity"] = nested_data.pop("id")
        representation.update(nested_data)
        return representation


class ReadOnlyPersonSerializer(JasprBaseModelSerializer):
    class Meta:
        model = Person
        fields = [
            "id",
            "name",
            "image_1x",
            "image_2x",
            "image_3x",
            "label_color",
            "order",
        ]
        read_only_fields = fields


class ReadOnlyTopicSerializer(JasprBaseModelSerializer):
    class Meta:
        model = Topic
        fields = [
            "id",
            "name",
            "label_color",
            "order",
        ]
        read_only_fields = fields


class ReadOnlyVideoSerializer(JasprBaseModelSerializer):
    file_field = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_tags(self, obj: Media):
        return [tag.name for tag in obj.tags.all()]

    class Meta:
        model = Media
        fields = [field for field in MediaSerializer.Meta.fields]
        read_only_fields = fields

    def get_file_field(self, obj):
        if obj.file_field:
            return obj.file_field.url
        else:
            return ""


class ReadOnlySharedStorySerializer(JasprBaseModelSerializer):
    person = ReadOnlyPersonSerializer(read_only=True)
    topic = ReadOnlyTopicSerializer(read_only=True)
    video = ReadOnlyVideoSerializer(read_only=True)

    class Meta:
        model = SharedStory
        fields = [
            "id",
            "person",
            "topic",
            "video",
            "order",
        ]
        read_only_fields = fields


class PatientActivitySerializer(JasprBaseModelSerializer):
    patient = serializers.HiddenField(default=CurrentPatientDefault())
    viewed = ViewedTimestampField()

    class Meta:
        model = PatientActivity
        fields = [
            "id",
            "patient",
            "activity",
            "rating",
            "save_for_later",
            "viewed",
        ]

    default_error_messages = {
        "activity_update_disallowed": "Not allowed to update `activity`."
    }

    def update(self, instance, validated_data):
        if (
                "activity" in validated_data
                and instance.activity != validated_data["activity"]
        ):
            raise serializers.ValidationError(
                {"activity": [self.error_messages["activity_update_disallowed"]]}
            )
        return super().update(instance, validated_data)


class PatientVideoSerializer(JasprBaseModelSerializer):
    patient = serializers.HiddenField(default=CurrentPatientDefault())
    viewed = ViewedTimestampField()

    class Meta:
        model = PatientVideo
        fields = [
            "id",
            "patient",
            "video",
            "rating",
            "save_for_later",
            "viewed",
            "progress",
        ]

    default_error_messages = {
        "video_update_disallowed": "Not allowed to update `video`."
    }

    def update(self, instance, validated_data):
        if "video" in validated_data and instance.video != validated_data["video"]:
            raise serializers.ValidationError(
                {"video": [self.error_messages["video_update_disallowed"]]}
            )
        with transaction.atomic():
            # NOTE: This probably isn't the most efficient way to do it (opens an
            # additional transaction plus one additional query it seems). If we had
            # atomic requests we could avoid opening a transaction, and if we could
            # find a way to "lock" the video upon retrieving it that could potentially
            # improve speed. Probably not a priority right now though, but just wanted
            # to document this (potentially same applies to other places we do this).
            instance = (
                PatientVideo.objects.filter(pk=instance.pk).select_for_update().get()
            )
            return super().update(instance, validated_data)


class PrivacyScreenImageSerializer(JasprBaseModelSerializer):
    """ For the privacy-screen-image endpoint. """

    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return ""

    class Meta:
        model = PrivacyScreenImage
        fields = ("id", "url")


class SecurityQuestionSerializer(JasprBaseModelSerializer):
    """
    Serializer for updating Security questions
    """

    answer = serializers.CharField(
        write_only=True, max_length=255, source="encrypted_answer"
    )
    question = serializers.CharField(max_length=255, source="encrypted_question")

    class Meta:
        model = Encounter
        fields = ("answer", "question")


class ValidateSessionSerializer(JasprBaseSerializer):
    """ Used for validating POST from validate-session """

    image = serializers.PrimaryKeyRelatedField(
        queryset=PrivacyScreenImage.objects.filter(status="active"), write_only=True
    )
    security_question_answer = serializers.CharField(write_only=True, max_length=255)




class ActionSerializer(JasprBaseModelSerializer):
    """
    Serializes a Jaspr `Action`.
    """

    patient = serializers.HiddenField(default=CurrentPatientDefault())
    encounter = serializers.HiddenField(default=CurrentPatientEncounterDefault())


    def validate(self, attrs: dict) -> dict:
        validate_action_with_section_uid(attrs["action"], attrs.get("section_uid"))
        attrs["in_er"] = self.context["request"].auth.jaspr_session.in_er
        encounter = self.context["request"].auth.jaspr_session.encounter
        attrs["encounter"] = None
        if encounter:
             attrs["encounter"] = encounter
        validate_action_with_extra(attrs["action"], attrs.get("extra"))
        validate_action_that_is_jah_only(attrs["action"], attrs["in_er"])
        return attrs

    class Meta:
        model = Action
        fields = (
            "patient",
            "encounter",
            "action",
            "screen",
            "extra",
            "section_uid",
            "client_timestamp",
        )


class ResetPasswordSerializer(JasprBaseSerializer):
    email = serializers.EmailField(max_length=255, write_only=True)


class ToolsToGoVerificationSetupSerializer(JasprBaseModelSerializer):
    email = serializers.EmailField(max_length=255, write_only=True)
    mobile_phone = PhoneNumberField(write_only=True)

    def update(self, instance: Patient, validated_data: dict) -> Patient:
        email = validated_data["email"]
        mobile_phone = validated_data["mobile_phone"]

        # Check if the patient has previously set an email by confirming
        # user is no longer using internally generated jaspr email address
        already_set_email = not instance.has_internal_email()

        email_unique = True
        initial_email = instance.user.email
        with transaction.atomic():
            with transaction.atomic():
                try:
                    instance.user.email = email
                    instance.user.save()
                except IntegrityError:
                    # Re-set the email back to its original value.
                    instance.user.email = initial_email
                    email_unique = False
                    logger.warning(
                        "For Jaspr at Home setup for Patient pk %d, email %s was given but was already "
                        "present in the database.",
                        instance.pk,
                        email,
                    )
            instance.user.mobile_phone = mobile_phone
            instance.user.save()
            instance.tools_to_go_status = Patient.TOOLS_TO_GO_EMAIL_SENT
            instance.save()
        # NOTE: Only send the email if we successfully set the email to a unique value
        # across users (excluding the current user).
        if email_unique:
           # NOTE: We are sending the email in the serializer right now since the
           # serializer is doing the transition of `tools_to_go_status` to
           # `Patient.TOOLS_TO_GO_EMAIL_SENT`. We do it outside of the
           # transaction because we want to make sure we have the updated user.

           # Send or Resend the initial setup email if the email address has changed
            if initial_email != instance.user.email:
                send_tools_to_go_setup_email(instance.user)

            # NOTE: Per specifications at the time of writing, email should be resent
            # after three days, and then after one week if the tools to go account
            # hasn't been set up yet.
            # NOTE: If the user is updating their email address, we do not need to requeue
            # the reminder email jobs as the job will pull the current email address during
            # execution
            if not already_set_email:
                enqueue_in(
                    datetime.timedelta(days=3),
                    check_and_resend_tools_to_go_setup_email,
                    instance.pk,
                    1,
                )
                enqueue_in(
                    datetime.timedelta(days=7),
                    check_and_resend_tools_to_go_setup_email,
                    instance.pk,
                    2,
                )
        return instance

    class Meta:
        model = Patient
        fields = ("email", "mobile_phone")


class CheckPasswordSerializerMixin(JasprBaseSerializer):
    # Matching `accounts.User` model's password field's
    # `max_length` of 128.
    current_password = serializers.CharField(max_length=128, write_only=True)

    default_error_messages = {"current_password": "Current password does not match."}

    def validate_current_password(self, value):
        if not self.instance.user.check_password(value):
            self.fail("current_password")
        return value


class SetPasswordSerializerMixin(JasprBaseSerializer):
    # Matching `accounts.User` model's password field's `max_length` of 128.
    password = serializers.CharField(min_length=1, max_length=128, write_only=True)

    @staticmethod
    def set_new_password(user: User, password: str) -> None:
        """
        Sets the `password` and other relevant fields on the `user`. Does not save
        the `user`.
        """
        user.set_password(password)
        user.password_changed = timezone.now()
        user.password_complex = check_password_complexity(password)


class PatientSetPasswordSerializer(
    SetPasswordSerializerMixin, JasprBaseModelSerializer
):
    """
    Allow a `Patient` to set his/her password.

    NOTE: At the time of writing this is typically used at the end of the tools to go
    setup flow or the reset password flow for Jaspr `Patient`s.
    """

    def update(self, instance: Patient, validated_data: dict) -> Patient:
        self.set_new_password(instance.user, validated_data["password"])
        # If the `Patient` is at "Phone Number Verified" for their tools to go
        # status right now, transition their status to "Setup Finished", since setting
        # the password is currently the last thing that needs to be done to finish the
        # flow.
        if instance.tools_to_go_status == Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED:
            instance.tools_to_go_status = Patient.TOOLS_TO_GO_SETUP_FINISHED
            with transaction.atomic():
                # Get the most recent encounter, irregardless of if the encounter has ended.
                encounter = Encounter.objects.filter(patient=instance).order_by("created").last()

                try:
                    jah_account = instance.jahaccount
                except JAHAccount.DoesNotExist:
                    jah_account = JAHAccount.objects.create(patient=instance)
                    jah_csp = CrisisStabilityPlan.objects.create(jah_account=jah_account)

                    try:
                        # TODO Get CSP from AssignedActivities
                        crisis_stability_plan = encounter.get_activity(ActivityType.StabilityPlan)
                        jah_csp_data = jah_csp.get_serializer()(crisis_stability_plan).data
                        jah_csp_serializer = jah_csp.get_serializer()(jah_csp, data=jah_csp_data)
                        jah_csp_serializer.is_valid(raise_exception=True)
                        jah_csp_serializer.save()

                        # TODO Missing Custom Coping Strategy copying

                    except AttributeError:
                        logger.exception(f"No crisis stability plan is available for patient {instance.pk}")
                        print("No crisis stability plan is available.  Starting with a blank plan")

                instance.user.save()
                instance.save()
            send_tools_to_go_confirmation_email(instance.user)
        else:
            instance.user.save()
        return instance

    class Meta:
        model = Patient
        fields = ("password",)


class PatientChangePasswordSerializer(
    CheckPasswordSerializerMixin, SetPasswordSerializerMixin, JasprBaseModelSerializer
):
    """
    Allow a `Patient` to change his/her password. Requires `current_password` to
    be provided and checks it.
    """

    def update(self, instance: Patient, validated_data: dict) -> Patient:
        self.set_new_password(instance.user, validated_data["password"])
        instance.user.save()
        return instance

    class Meta:
        model = Patient
        fields = ("current_password", "password")


class TechnicianSetPasswordSerializer(
    SetPasswordSerializerMixin, JasprBaseModelSerializer
):
    """
    Allow a `Technician` to set his/her password. This *should not* be used for
    _changing a `Technician`s password_ but only for setting it as part of a reset
    password type flow right now.
    """

    password_validator = JasprPasswordValidator(
        min_characters=8,
        require_upper_case=True,
        require_lower_case=True,
        require_number=True,
        require_special_character=False,
    )

    def validate_password(self, password: str) -> str:
        self.password_validator(password)
        return password

    def update(self, instance: Technician, validated_data: dict) -> Technician:
        self.set_new_password(instance.user, validated_data["password"])
        instance.activated = True
        # NOTE: This means `last_activated_at` may be slightly earlier than
        # `first_activated_at` (due to the `MonitorField`). This is ok. Still easy to
        # query and/or see `Technicians` that have only activated once (and multiple
        # ways to do so).
        instance.last_activated_at = timezone.now()
        instance.user.save()
        instance.save()
        # Two different views call this serializer.  We need to determine which flow
        # in order to return correct confirmation email.
        if "TechnicianResetPasswordSetPasswordView" in str(self.root.context["view"]):
            send_technician_set_password_confirmation_email(instance.user.technician)
        else:
            send_technician_activation_confirmation_email(instance.user.technician)

        return instance

    class Meta:
        model = Technician
        fields = ("password",)


class VerifyPhoneNumberSerializer(JasprBaseSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    mobile_phone = PhoneNumberField(write_only=True)

    default_error_messages = {
        "mobile_phone_mismatch": (
            "The phone number entered does not match the one we have on record."
        ),
    }

    @classmethod
    def send_verification(cls, user: User) -> None:
        send_phonenumber_verification(user.mobile_phone.as_e164, user_id=user.pk)

    def validate(self, attrs: dict) -> dict:
        user = attrs["user"]
        if user.mobile_phone != attrs["mobile_phone"]:
            self.fail("mobile_phone_mismatch")
        try:
            self.send_verification(attrs["user"])
        except VerificationException as e:
            raise serializers.ValidationError(e.error_message)
        return {"sent": True}


class NativeVerifyPhoneNumberFieldCheckSerializer(JasprBaseSerializer):
    """
    For this serializer, just check that `email` and `mobile_phone` are a valid
    (formatting wise) email and phone number respectively. Don't do any extra logic,
    let the view do that.
    """

    email = serializers.EmailField(max_length=255, write_only=True)
    mobile_phone = PhoneNumberField(write_only=True)


class NativeCheckPhoneNumberFieldCheckSerializer(
    NativeVerifyPhoneNumberFieldCheckSerializer
):
    """
    NOTE: See the docstring in `PatientNativeCheckPhoneNumberCodeView` as to why this
    serializer is here.
    """

    code = serializers.RegexField(r"^[0-9]{4,10}$", write_only=True)


class CheckPhoneNumberVerificationSerializer(JasprBaseSerializer):
    user = serializers.HiddenField(default=ContextUserDefault())
    code = serializers.RegexField(r"^[0-9]{4,10}$", write_only=True)

    def validate(self, attrs: dict) -> dict:
        try:
            check_phonenumber_verification(
                phone_number=attrs["user"].mobile_phone.as_e164,
                code=attrs["code"],
                user_id=attrs["user"].pk,
            )
        except VerificationException as e:
            raise serializers.ValidationError(e.error_message)
        return {"valid": True}


class ReadOnlyPatientWalkthroughStepSerializer(JasprBaseModelSerializer):
    step_name = serializers.CharField(source="step.name")

    class Meta:
        model = PatientWalkthroughStep
        fields = (
            "step_name",
            "frontend_render_type",
            "value",
        )

        read_only_fields = fields


class ReadOnlyGuideMessageSerializer(JasprBaseModelSerializer):
    message = serializers.CharField()

    class Meta:
        model = GuideMessage
        fields = ("message",)

        read_only_fields = fields


class ReadOnlyHelplineSerializer(JasprBaseModelSerializer):
    class Meta:
        model = Helpline
        fields = (
            "name",
            "phone",
            "text",
        )

        read_only_fields = fields


class ReadOnlyCopingStrategyCategorySerializer(JasprBaseModelSerializer):
    class Meta:
        model = CopingStrategyCategory
        fields = (
            "id",
            "name",
            "why_text",
        )

        read_only_fields = fields


class ReadOnlyCopingStrategySerializer(JasprBaseModelSerializer):
    category = ReadOnlyCopingStrategyCategorySerializer(read_only=True)

    class Meta:
        model = CopingStrategy
        fields = (
            "id",
            "title",
            "image",
            "category",
        )

        read_only_fields = fields


class ReadOnlyGenericCopingStrategySerializer(JasprBaseSerializer):
    """ This is a serializer intended to serialize both CopingStrategy and PatientCopingStrategy records. """

    category = ReadOnlyCopingStrategyCategorySerializer(read_only=True)
    title = serializers.CharField()
    image = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "title",
            "image",
            "category",
        )

        read_only_fields = fields

    def get_image(self, obj):
        if hasattr(obj, "image"):
            return obj.image.url
        else:
            try:
                url = Media.objects.get(name="Custom Coping Strategy").file_field.url

            except Media.DoesNotExist:
                url = ""
            return url


class ActivateTechnicianSerializer(JasprBaseSerializer):
    default_error_messages = {
        "invalid": "Invalid email and/or activation code provided.",
    }

    technician = serializers.HiddenField(default=CurrentTechnicianDefault())
    email = serializers.EmailField(max_length=255, write_only=True)
    activation_code = serializers.CharField(max_length=63, write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)
        technician = data["technician"]
        email = data["email"]
        activation_code = data["activation_code"]
        user = technician.user
        clinic = technician.system
        # NOTE: In this use case, we're just checking against the value of the passed
        # in email. Hence it's okay to do this, and we don't currently have to worry
        # about any security concerns with respect to a case-folded email being sent to
        # a different email address, etc
        # (https://eng.getwisdom.io/hacking-github-with-unicode-dotless-i/).
        user_email_lower = user.email.casefold()
        email_lower = email.casefold()
        if user_email_lower != email_lower:
            self.fail("invalid")
        if clinic.activation_code != activation_code:
            self.fail("invalid")
        return data

    def create(self, validated_data: Dict[str, Any]) -> Technician:
        # Right now we don't do anything here, but we could later down the road.
        return validated_data["technician"]


class AmendmentSerializer(JasprBaseModelSerializer):
    ## TODO Check that we are getting encounter from context
    encounter = serializers.HiddenField(default=ContextDefault("encounter"))
    technician = serializers.HiddenField(default=CurrentTechnicianDefault())

    def to_representation(self, obj: Amendment) -> Dict[str, Any]:
        can_edit = self.context["request"].user.technician.pk == obj.technician_id

        return {
            **super().to_representation(obj),
            "technician": {
                "id": obj.technician_id,
                "email": obj.technician.user.email,
                "can_edit": can_edit,
            },
        }

    class Meta:
        model = Amendment
        fields = [
            "id",
            "encounter",
            "note_type",
            "technician",
            "comment",
            "created",
            "modified",
        ]
        read_only_fields = ["created", "modified"]

