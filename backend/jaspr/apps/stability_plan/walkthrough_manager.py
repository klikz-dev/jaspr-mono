import logging

from django.db import transaction
from django.db.models import Q
from simple_history.utils import bulk_create_with_history, bulk_update_with_history

from jaspr.apps.api.v1.serializers import (
    MediaSerializer,
    ReadOnlyActivitySerializer,
    ReadOnlyCopingStrategySerializer,
    ReadOnlyGenericCopingStrategySerializer,
    ReadOnlyGuideMessageSerializer,
    ReadOnlyHelplineSerializer,
    ReadOnlySharedStorySerializer,
)
from jaspr.apps.awsmedia.models import Media
from jaspr.apps.jah.models import CrisisStabilityPlan, JAHAccount
from jaspr.apps.kiosk.models import (
    Activity,
    CopingStrategy,
    CopingStrategyCategory,
    GuideMessage,
    Helpline,
    Patient,
    PatientVideo,
    SharedStory,
)
from jaspr.apps.jah.models import PatientCopingStrategy
from jaspr.apps.stability_plan.models import (
    PatientWalkthrough,
    PatientWalkthroughStep,
    Step,
    Walkthrough,
    WalkthroughStep,
)

logger = logging.getLogger(__name__)

FRONTEND_RENDER_MAP = {
    "activity": {
        "model_class": Activity,
        "serializer_class": ReadOnlyActivitySerializer,
    },
    "breathe": {
        "model_class": None,
        "serializer_class": None,
    },
    "copingStrategy": {
        "model_class": CopingStrategy,
        "serializer_class": ReadOnlyCopingStrategySerializer,
    },
    "guide": {
        "model_class": GuideMessage,
        "serializer_class": ReadOnlyGuideMessageSerializer,
    },
    "lethalMeans": {
        "model_class": None,
        "serializer_class": None,
    },
    "nationalHotline": {
        "model_class": Helpline,
        "serializer_class": ReadOnlyHelplineSerializer,
    },
    "personalizedLethalMeans": {
        "model_class": None,
        "serializer_class": None,
        "function": "personalized_lethal_means",
    },
    "copingStrategy": {
        "model_class": CopingStrategy,
        "serializer_class": ReadOnlyCopingStrategySerializer,
    },
    "recap": {
        "model_class": None,
        "serializer_class": None,
    },
    "reasonsForLiving": {
        "model_class": None,
        "serializer_class": None,
        "function": "reasons_for_living",
    },
    "sharedStory": {
        "model_class": SharedStory,
        "serializer_class": ReadOnlySharedStorySerializer,
    },
    "supportivePeople": {
        "model_class": None,
        "serializer_class": None,
        "function": "supportive_people",
    },
    "video": {"model_class": Media, "serializer_class": MediaSerializer},
    "videoDescription": {
        "model_class": Media,
        "serializer_class": MediaSerializer,
    },
}


class WalkthroughManager:
    """ Manage relationships between Walkthrough, Patient and Steps """

    def __init__(
        self, patient, walkthrough=None, use_existing_patient_walkthrough=False
    ):
        """  Initialize state here, not making any database changes."""

        self.use_existing_patient_walkthrough = use_existing_patient_walkthrough
        self.walkthrough = walkthrough
        self.patient = patient
        self.jah_account = patient.jahaccount
        self.new_patient_walkthrough_steps = []

        # initializing these attributes here; defined further in setup
        self.crisis_stability_plan = None
        self.existing_patient_walkthrough = None
        self.physical_coping_strategy_category = None
        self.paced_breathing_activity = None

    def setup(self):
        """ Set up all attributes that require a database call. """

        # We meed to be able to reference the paced breathing activity
        self.paced_breathing_activity = Activity.objects.filter(
            target_url="/breathe",
            status="active",
        ).first()
        assert self.paced_breathing_activity, "Missing a Paced Breathing activity."

        assert (
            Activity.objects.filter(target_url="/breathe").count() == 1
        ), "More than 1 Paced Breathing activities found."

        self.physical_coping_strategy_category = CopingStrategyCategory.objects.filter(
            status="active",
            slug="physical",
        ).first()
        assert (
            self.physical_coping_strategy_category
        ), "Missing a Physical Coping Strategy Category with a slug of 'physical'."

        # for clarification: allow walkthrough XOR use_existing_patient_walkthrough, not both
        assert not (
            self.walkthrough and self.use_existing_patient_walkthrough
        ), "Only set walkthrough or use_existing_patient_walkthrough"

        self.existing_patient_walkthrough = PatientWalkthrough.objects.filter(
            patient=self.patient, status="active"
        ).first()

        # If we need to use an existing walkthrough, we need to have one to use.
        if self.use_existing_patient_walkthrough:
            assert (
                self.existing_patient_walkthrough
            ), "If we need to use an existing walkthrough, we need to have one to use"

            self.walkthrough = self.existing_patient_walkthrough.walkthrough

        self.crisis_stability_plan = self.jah_account.crisisstabilityplan

        assert (
            self.crisis_stability_plan
        ), "A Crisis Stability Plan is required for this patient to build a patient walkthrough."

    def deactivate_old_records(self):
        """ Mark as archived and inactive various related records. """

        # if there is an existing patient walkthrough, let's mark records related to it as inactive.
        if self.existing_patient_walkthrough:

            pws_qs = PatientWalkthroughStep.objects.filter(
                patient_walkthrough__patient=self.patient
            )

            for pws in pws_qs:
                pws.status = "inactive"

            bulk_update_with_history(
                pws_qs,
                PatientWalkthroughStep,
                ["status"],
                batch_size=500,
                default_user=self.patient.user,
            )

            self.existing_patient_walkthrough.status = "inactive"
            self.existing_patient_walkthrough._history_user = self.patient.user

            self.existing_patient_walkthrough.save()

    def set_walkthrough(self):
        # Use most recent Walkthrough if we don't already have a walkthrough.
        if not self.walkthrough:
            self.walkthrough = (
                Walkthrough.objects.filter(status="active").order_by("-created").first()
            )
            assert self.walkthrough, "Could not find an active Walkthrough"

    def create_patient_walkthrough(self):
        """
        Create a new, active patient_walkthrough to contain our new PatientWalkthroughStep records.
        """
        self.patient_walkthrough = PatientWalkthrough.objects.create(
            patient=self.patient,
            _history_user=self.patient.user,
            walkthrough=self.walkthrough,
            status="active",
        )

    def get_steps(self):
        # use the steps of this walkthrough to create the patient steps
        return Step.objects.filter(
            walkthroughstep__status="active",
            walkthroughstep__walkthrough__status="active",
            walkthroughstep__walkthrough=self.walkthrough,
        ).order_by("walkthroughstep__order")

    def is_step_special(self, step):
        if step.function:
            return True

        if "function" in FRONTEND_RENDER_MAP[step.frontend_render_type]:
            return True
        return False

    def skip_step(self, step):
        """ Determine if we need to skip a step. """
        # if no object_id present and skip_if_blank is True, do not create a patient_step if no special function.

        if (
            step.skip_if_blank
            and step.object_id is None
            and not self.is_step_special(step)
        ):
            return True
        return False

    def _prepare_standard_patient_walkthrough_step(self, step):
        """ Create Standard Patient Walkthrough Step (no functions) based on a step"""
        if step.content_object:
            # get serialized version of content_object
            serializer_class = FRONTEND_RENDER_MAP[step.frontend_render_type][
                "serializer_class"
            ]
            serialized_obj = serializer_class(step.content_object).data
        else:
            serialized_obj = None

        return PatientWalkthroughStep(
            patient_walkthrough=self.patient_walkthrough,
            step=step,
            value=serialized_obj,
            frontend_render_type=step.frontend_render_type,
            status="active",
        )

    def favorite_shared_story(self, step):
        """ Find a favorited video that is also a video on a shared story and make a PatientWalkthroughStep"""

        favorited_video_ids = PatientVideo.objects.filter(
            save_for_later=True,
            status="active",
        ).values_list("video_id", flat=True)

        shared_story = (
            SharedStory.objects.filter(video_id__in=favorited_video_ids)
            .order_by("-created")
            .first()
        )

        if shared_story:
            serialized_obj = MediaSerializer(shared_story.video).data

        elif step.content_object:
            if step.content_object.__class__ == SharedStory:
                serialized_obj = MediaSerializer(step.content_object.video).data
            elif step.content_object.__class__ == Media:
                serialized_obj = MediaSerializer(step.content_object).data
            else:
                return
        else:
            # no content object, just exit
            logger.error(
                f"No content_object was found for step #{step.pk}. "
                "This is likely due to a mismatch between object id and chosen content type."
            )
            return

        return PatientWalkthroughStep(
            patient_walkthrough=self.patient_walkthrough,
            step=step,
            value=serialized_obj,
            frontend_render_type="video",
            status="active",
        )

    def top_non_physical_coping_strategies(self, step):
        """
        If there are non-physical coping strategies in coping_top, use up to 3,
        But only if none have been added as steps from this step with this function.
        If there are none, use the default given.
        """
        original_coping_strategies = []
        processed_coping_strategies = []

        if coping_top := self.crisis_stability_plan.coping_top:
            q_qs = Q()
            for title in coping_top:
                q_qs |= Q(title__iexact=title)

            # Let's first establish if there are, in fact, any non-physical coping strategies selected.
            for coping_strategy in CopingStrategy.objects.filter(q_qs, status="active"):
                if coping_strategy.category != self.physical_coping_strategy_category:
                    original_coping_strategies.append(coping_strategy)

            # Now find non-physical patient coping strategies
            for coping_strategy in PatientCopingStrategy.objects.filter(
                q_qs, jah_account=self.jah_account, status="active"
            ):
                if coping_strategy.category != self.physical_coping_strategy_category:
                    original_coping_strategies.append(coping_strategy)

            # Sort by order in coping_top
            original_coping_strategies = sorted(
                original_coping_strategies,
                key=lambda strategy: coping_top.index(strategy.title),
            )

        # If we found originals then make steps.
        if original_coping_strategies:
            # get other steps that have this function in this walkthrough
            step_ids = (
                WalkthroughStep.objects.filter(
                    walkthrough=self.walkthrough,
                    step__function="top_non_physical_coping_strategies",
                    status="active",
                )
                .exclude(step=step)
                .values_list("step__id", flat=True)
            )

            num_pws = len(
                [
                    new_step
                    for new_step in self.new_patient_walkthrough_steps
                    if new_step.step_id in step_ids
                ]
            )

            # if None, let's get ready to make some
            if num_pws == 0:
                processed_coping_strategies = original_coping_strategies

        # If no originals, then substitute with defaults if available.
        elif not original_coping_strategies and step.content_object:
            processed_coping_strategies.append(step.content_object)

        # do nothing if step.content_object is None
        else:
            pass

        new_steps = []
        for coping_strategy in processed_coping_strategies[:3]:
            serialized_obj = ReadOnlyCopingStrategySerializer(coping_strategy).data
            new_steps.append(
                PatientWalkthroughStep(
                    patient_walkthrough=self.patient_walkthrough,
                    step=step,
                    value=serialized_obj,
                    frontend_render_type="copingStrategy",
                    status="active",
                )
            )
        return new_steps

    def top_physical_coping_strategy(self, step):
        """ Use coping_body or content object or Breathe app."""

        if self.crisis_stability_plan.coping_body:
            title = self.crisis_stability_plan.coping_body[0]
            try:
                coping_strategy = CopingStrategy.objects.get(title__iexact=title)
            except CopingStrategy.DoesNotExist:
                # Get or create -- although should never have to create --
                # a related custom coping strategy, since we weren't able to find
                # a matching Pre-defined one.  We expect it to be a custom one at this point,
                # because custom coping strategies are made when Frontend alters coping strategy fields
                # on crisis_stability_plan.
                coping_strategy = PatientCopingStrategy.objects.get_or_create(
                    jah_account=self.jah_account,
                    title=title,
                    defaults={
                        "category": self.physical_coping_strategy_category,
                        "status": "active",
                    },
                )[0]
                # we should never have to hit this code,
                # but if for some reason, status is archived, may need to be changed.
                if coping_strategy.status == "archived":
                    coping_strategy.status = "active"
                    coping_strategy.save()
                    logger.error(
                        f"System found patient_coping_strategy `{coping_strategy.title}`"
                        f"with status of archived while attempting to generate patient walkthrough step for {step.name}"
                    )
        elif step.content_object:
            coping_strategy = step.content_object
        else:
            # ignoring skip if blank for the time being
            coping_strategy = None

        if coping_strategy:
            # We'll use the ReadOnlyGenericCopingStrategySerializer for both
            # classes of objects: PatientCopingStrategy and CopingStrategy
            serialized_obj = ReadOnlyGenericCopingStrategySerializer(
                coping_strategy
            ).data
            return PatientWalkthroughStep(
                patient_walkthrough=self.patient_walkthrough,
                step=step,
                value=serialized_obj,
                frontend_render_type="copingStrategy",
                status="active",
            )
        else:
            return PatientWalkthroughStep(
                patient_walkthrough=self.patient_walkthrough,
                step=step,
                value=None,
                frontend_render_type="breathe",
                status="active",
            )

    def favorite_activity(self, step):

        patient_activity = (
            self.patient.patientactivity_set.filter(
                save_for_later=True, status="active"
            )
            .order_by("-rating", "-created")
            .first()
        )

        if not patient_activity:
            activity = None
        else:
            activity = patient_activity.activity

        # Substitute content_object, if activity is not found.
        if not activity and step.content_object:
            activity = step.content_object

        # skip step if no activity and skip_if_blank True
        if not activity and step.skip_if_blank:
            return

        # If no activity, but skip_if_blank is False - make a paced breathing step.
        if not activity and not step.skip_if_blank:
            return PatientWalkthroughStep(
                patient_walkthrough=self.patient_walkthrough,
                step=step,
                value=None,
                frontend_render_type="breathe",
                status="active",
            )

        # Make a paced breathing step if activity is the paced breathing activity.
        elif activity == self.paced_breathing_activity:
            return PatientWalkthroughStep(
                patient_walkthrough=self.patient_walkthrough,
                step=step,
                value=None,
                frontend_render_type="breathe",
                status="active",
            )

        # If we have just a regular activity, figure out if it's a `Media` or an
        # `Activity` and render a `Media` regardless.
        elif activity:
            if isinstance(activity, Media):
                media = activity
            else:
                # Assume `activity` is an instance of `Activity` in this case.
                media = activity.video
            serialized_obj = MediaSerializer(media).data
            return PatientWalkthroughStep(
                patient_walkthrough=self.patient_walkthrough,
                step=step,
                value=serialized_obj,
                frontend_render_type="video",
                status="active",
            )

    def supportive_people(self, step):
        """ Create a Supportive People step for each supportive person. """
        supportive_people = self.crisis_stability_plan.supportive_people
        new_steps = []
        if supportive_people:
            for support in supportive_people:
                new_steps.append(
                    PatientWalkthroughStep(
                        patient_walkthrough=self.patient_walkthrough,
                        step=step,
                        value=support,
                        frontend_render_type=step.frontend_render_type,
                        status="active",
                    )
                )
        return new_steps

    def reasons_for_living(self, step):
        """ Create a step that has a value of crisis_stability_plan.reasons_live """

        if self.crisis_stability_plan.reasons_live:

            return PatientWalkthroughStep(
                patient_walkthrough=self.patient_walkthrough,
                step=step,
                value=self.crisis_stability_plan.reasons_live,
                frontend_render_type=step.frontend_render_type,
                status="active",
            )

    def personalized_lethal_means(self, step):

        strategies = {
            "strategies_general": self.crisis_stability_plan.strategies_general,
            "strategies_firearm": self.crisis_stability_plan.strategies_firearm,
            "strategies_medicine": self.crisis_stability_plan.strategies_medicine,
            "strategies_places": self.crisis_stability_plan.strategies_places,
            "strategies_other": self.crisis_stability_plan.strategies_other,
            "strategies_custom": self.crisis_stability_plan.strategies_custom,
            "means_support_who": self.crisis_stability_plan.means_support_who,
        }

        if any(strategies.values()):
            return PatientWalkthroughStep(
                patient_walkthrough=self.patient_walkthrough,
                step=step,
                value=strategies,
                frontend_render_type=step.frontend_render_type,
                status="active",
            )

    def _prepare_custom_patient_walkthrough_step(self, step):
        """ Create Patient Walkthrough Steps with special considerations. """

        # TODO: Not the greatest, would be nice when we think about how to make step UI better
        # To tighten this up.
        if "function" in FRONTEND_RENDER_MAP[step.frontend_render_type]:
            step.function = FRONTEND_RENDER_MAP[step.frontend_render_type]["function"]

        if step.function:
            function = getattr(self, step.function)
            return function(step)

    def create_patient_walkthrough_steps(self):
        """ Create PatientWalkthroughStep for a patient. """
        # use the steps of this walkthrough to create the patient steps
        for step in self.get_steps():
            if self.skip_step(step):
                continue

            # if no special instructions on step, just create a normal patient_step
            if not self.is_step_special(step):
                pws = self._prepare_standard_patient_walkthrough_step(step)

            # Special considerations on step
            else:
                pws = self._prepare_custom_patient_walkthrough_step(step)

            if pws and isinstance(pws, list):
                self.new_patient_walkthrough_steps.extend(pws)
            elif pws:
                self.new_patient_walkthrough_steps.append(pws)

        for counter, pws in enumerate(self.new_patient_walkthrough_steps):
            pws.order = counter

        bulk_create_with_history(
            self.new_patient_walkthrough_steps,
            PatientWalkthroughStep,
            batch_size=500,
            default_user=self.patient.user,
        )

    def handle(self):
        """ Handling changes here """
        # setting this to [] here as well as init in case of calling multiple times with same instantiation.
        self.new_patient_walkthrough_steps = []
        try:
            with transaction.atomic():
                # prevent race conditions by locking down patient record
                self.patient = (
                    Patient.objects.filter(pk=self.patient.pk).select_for_update().get()
                )
                self.setup()
                self.deactivate_old_records()
                self.set_walkthrough()
                self.create_patient_walkthrough()
                self.create_patient_walkthrough_steps()
        except Exception as e:
            logger.exception(
                "Caught exception in Walkthrough Manager.\n" "Exception: %s",
                str(e),
            )
            raise
