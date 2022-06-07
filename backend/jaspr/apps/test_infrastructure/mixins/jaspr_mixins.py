from typing import Generator

from model_bakery.recipe import seq
from taggit.utils import parse_tags

from jaspr.apps.accounts.models import User
from jaspr.apps.awsmedia.models import Media, PrivacyScreenImage
from jaspr.apps.jah.models import CommonConcern, ConversationStarter, PatientCopingStrategy as JAHPatientCopingStrategy
from jaspr.apps.kiosk.models import (
    Action,
    ActivateRecord,
    Activity,
    Amendment,
    CopingStrategy,
    CopingStrategyCategory,
    Encounter,
    GuideMessage,
    Helpline,
    JasprSession,
    JasprUserTypeString,
    Patient,
    PatientActivity,
    PatientCopingStrategy as KioskPatientCopingStrategy,
    PatientVideo,
    Person,
    ProviderComment,
    SharedStory,
    Technician,
    Topic,

)

from jaspr.apps.stability_plan.models import (
    PatientWalkthrough,
    PatientWalkthroughStep,
    Step,
    Walkthrough,
    WalkthroughStep,
)
from jaspr.apps.test_infrastructure.enhanced_baker import baker
from jaspr.apps.test_infrastructure.mixins.jaspr_base_mixins import (
    JasprBaseTestCaseMixin,
)


class JasprTestCaseMixin(JasprBaseTestCaseMixin):
    """
    Collection of helper methods for tests involving kiosk.
    Useful for both API and non-API tests. Inherits from
    `JasprBaseTestCaseMixin`, where the critical methods that
    involve creating user types (I.E. `Technician`s, `Patient`s, etc.)
    are defined. The methods here involve creating test instances
    of various models defined across kiosk.
    """

    @classmethod
    def create_patient_video(cls, **kwargs) -> PatientVideo:
        if "video" not in kwargs:
            kwargs.setdefault("video__file_type", "video")
        return baker.make(PatientVideo, **kwargs)

    @classmethod
    def create_activity(cls, **kwargs) -> Activity:
        return baker.make(Activity, **kwargs)

    @classmethod
    def create_person(cls, **kwargs) -> Person:
        return baker.make(Person, **kwargs)

    @classmethod
    def create_provider_comment(cls, **kwargs) -> ProviderComment:
        return baker.make(ProviderComment, **kwargs)

    @classmethod
    def create_topic(cls, **kwargs) -> Topic:
        return baker.make(Topic, **kwargs)

    @classmethod
    def create_shared_story(cls, **kwargs) -> Person:
        if "video" not in kwargs:
            kwargs.setdefault("video__file_type", "video")
        return baker.make(SharedStory, **kwargs)

    @classmethod
    def create_patient_activity(cls, **kwargs) -> PatientActivity:
        return baker.make(PatientActivity, **kwargs)

    @classmethod
    def create_privacy_screen_image(cls, **kwargs) -> PrivacyScreenImage:
        return baker.make(PrivacyScreenImage, **kwargs)

    @classmethod
    def create_patient_encounter(cls, **kwargs) -> Encounter:
        if "patient" not in kwargs:
            kwargs["patient"] = cls.create_patient()
        if "department" not in kwargs:
            kwargs["department"] = cls.create_department()
        return baker.make(Encounter, **kwargs)

    @classmethod
    def create_security_question(cls, **kwargs) -> Encounter:
        if "patient" not in kwargs:
            kwargs["patient"] = cls.create_patient()
        return baker.make(Encounter, **kwargs)

    @classmethod
    def create_action(cls, **kwargs) -> Action:
        return baker.make(Action, **kwargs)

    @classmethod
    def create_activate_record(cls, **kwargs) -> ActivateRecord:
        return baker.make(ActivateRecord, **kwargs)

    @classmethod
    def create_media(cls, file_type="video", **kwargs) -> Media:
        tags = kwargs.pop("tags", None)
        media_obj = baker.make(Media, _create_files=True, file_type=file_type, **kwargs)
        if tags:
            media_obj.tags.add(*parse_tags(tags))

        return media_obj

    @classmethod
    def create_common_concern(cls, **kwargs) -> CommonConcern:
        return baker.make(CommonConcern, **kwargs)

    @classmethod
    def create_conversation_starter(cls, **kwargs) -> ConversationStarter:
        return baker.make(ConversationStarter, **kwargs)

    @classmethod
    def create_walkthrough(cls, **kwargs) -> Walkthrough:
        return baker.make(Walkthrough, **kwargs)

    @classmethod
    def create_patient_walkthrough(cls, **kwargs) -> PatientWalkthrough:
        return baker.make(PatientWalkthrough, **kwargs)

    @classmethod
    def create_patient_wakthrough_step(cls, **kwargs) -> PatientWalkthroughStep:
        return baker.make(PatientWalkthroughStep, **kwargs)

    @classmethod
    def create_step(cls, **kwargs) -> Step:
        return baker.make(Step, **kwargs)

    @classmethod
    def create_walkthrough_step(cls, **kwargs) -> WalkthroughStep:
        return baker.make(WalkthroughStep, **kwargs)

    @classmethod
    def create_guide_message(cls, **kwargs) -> GuideMessage:
        return baker.make(GuideMessage, **kwargs)

    @classmethod
    def create_coping_strategy(cls, **kwargs) -> CopingStrategy:
        return baker.make(CopingStrategy, _create_files=True, **kwargs)

    @classmethod
    def create_coping_strategy_category(cls, **kwargs) -> CopingStrategyCategory:
        return baker.make(CopingStrategyCategory, **kwargs)

    @classmethod
    def create_helpline(cls, **kwargs) -> Helpline:
        return baker.make(Helpline, **kwargs)

    @classmethod
    def create_kiosk_patient_coping_strategy(cls, **kwargs) -> KioskPatientCopingStrategy:
        return baker.make(KioskPatientCopingStrategy, **kwargs)

    @classmethod
    def create_jah_patient_coping_strategy(cls, **kwargs) -> JAHPatientCopingStrategy:
        return baker.make(JAHPatientCopingStrategy, **kwargs)

    @classmethod
    def create_amendment(cls, **kwargs) -> Amendment:
        return baker.make(Amendment, **kwargs)

    uid_seq: Generator[str, None, None] = seq("Test-UID")


class JasprApiTokenMixin:
    """
    Mixin for use with testcases that query the Jaspr API and need token based
    authentication/credentials.
    """

    def set_creds(
        self,
        user: User,
        user_type: JasprUserTypeString,
        in_er: bool,
        from_native: bool,
        long_lived: bool,
        encounter: Encounter = None,
    ) -> str:
        jaspr_session, token = JasprSession.create(
            user=user,
            user_type=user_type,
            in_er=in_er,
            from_native=from_native,
            long_lived=long_lived,
            encounter=encounter,
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        return token

    def set_patient_creds(
        self,
        patient: Patient,
        in_er: bool = False,
        from_native: bool = None,
        long_lived: bool = None,
        encounter: Encounter = None,
    ) -> str:
        if in_er:
            if from_native is None:
                # The default in the ER for `Patient`s is to be on the web app
                # (activated via a `Technician`).
                from_native = False
            if long_lived is None:
                # In the ER, tokens aren't `long_lived`.
                long_lived = False
            # if encounter is None:
            #    encounter = patient.current_encounter
        else:
            if from_native is None:
                # `Patient`s, right now, if not in the ER, can only currently
                # access/use Jaspr from the native app.
                from_native = True
            if long_lived is None:
                # When `Patient`s aren't in the ER `long_lived` tokens are used right
                # now by the frontend, so we'll default to that.
                long_lived = True
        return self.set_creds(
            patient.user,
            user_type="Patient",
            in_er=in_er,
            from_native=from_native,
            long_lived=long_lived,
            encounter=encounter,
        )

    def set_technician_creds(
        self,
        technician: Technician,
        in_er: bool = True,
    ) -> str:
        return self.set_creds(
            # NOTE: This is the only currently allowed combination of `in_er`,
            # `from_native`, and `long_lived` for `Technician`s.
            technician.user,
            user_type="Technician",
            in_er=in_er,
            from_native=False,
            long_lived=False,
        )

    @property
    def epic_authorize_url(self):
        return "https://fakeprovider.com/fhir/oauth2/authorize"

    @property
    def epic_token_url(self):
        return "https://fakeprovider.com/fhir/oauth2/token"

    @property
    def epic_iss_metadata(self):
        return {
        "rest": [
            {
                "security": {
                    "extension": [
                        {
                            "extension": [
                                {
                                    "valueUri": self.epic_authorize_url,
                                    "url": "authorize"
                                },
                                {
                                    "valueUri": self.epic_token_url,
                                    "url": "token"
                                }
                            ],
                        }
                    ],
                }
            }
        ]
    }
