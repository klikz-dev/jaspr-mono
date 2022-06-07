from collections import Counter

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError

from jaspr.apps.api.v1.serializers import (
    MediaSerializer,
    ReadOnlyPersonSerializer,
    ReadOnlyTopicSerializer,
    ReadOnlyVideoSerializer,
)
from jaspr.apps.jah.models import JAHAccount, CrisisStabilityPlan
from jaspr.apps.stability_plan.constants import FRONTEND_RENDER_TYPE_CHOICES
from jaspr.apps.stability_plan.models import (
    PatientWalkthrough,
    PatientWalkthroughStep,
    get_walkthrough_content_types_filter,
)
from jaspr.apps.test_infrastructure.testcases import JasprTestCase

from ..walkthrough_manager import FRONTEND_RENDER_MAP, WalkthroughManager


class TestCreatePatientWalkthroughSteps(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.paced_breathing_activity = self.create_activity(
            name="Paced Breathing",
            target_url="/breathe",
        )
        self.physical_coping_strategy_category = self.create_coping_strategy_category(
            name="Physical", slug="physical"
        )
        self.patient = self.create_patient(
            ssid="test-patient-1"
        )
        self.jah_account = JAHAccount.objects.create(patient=self.patient)
        self.jah_csp = CrisisStabilityPlan.objects.create(jah_account=self.jah_account)

        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )

        self.walkthrough = self.create_walkthrough(name="Default")
        self.manager = WalkthroughManager(
            patient=self.patient, walkthrough=self.walkthrough
        )

    def test_walkthough_step_unique_constraint(self):
        """ Is a user forbidden from having multiple walkthroughstep objects with same walkthrough and step? """
        ple_video = self.create_media(
            file_type="video",
            name="Welcome Video",
            description="This is the description for the Welcome Video",
        )

        media_content_type = ContentType.objects.get(
            model="media", app_label="awsmedia"
        )

        step = self.create_step(
            name="PLE Video",
            content_type=media_content_type,
            object_id=ple_video.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="videoDescription",
        )

        # join the step to the walkthrough
        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        with self.assertRaisesMessage(
            IntegrityError, "duplicate key value violates unique constraint"
        ) as e:
            self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

    def test_frontend_render_map(self):
        """ Is FRONTEND_RENDER_TYPE_CHOICES consistent with FRONTEND_RENDER_MAP"""

        self.assertEqual(
            Counter([choice[0] for choice in FRONTEND_RENDER_TYPE_CHOICES]),
            Counter(FRONTEND_RENDER_MAP.keys()),
        )

    def test_limit_choices_to_consistent_with_frontend_render_map(self):
        """ Is FRONTEND_RENDER_TYPE_CHOICES consistent with FRONTEND_RENDER_MAP"""
        # make a list of classes used in the FRONTEND_RENDER_MAP
        classes = list(
            set(
                [
                    render_map[1]["model_class"]
                    for render_map in FRONTEND_RENDER_MAP.items()
                    if render_map[1]["model_class"] != None
                ]
            )
        )

        # make a list of classes specified in get_walkthrough_content_types_filter
        # for use by the limit_choices_to attribute on Content Type
        filter_q = get_walkthrough_content_types_filter()
        content_types = ContentType.objects.filter(filter_q)

        ct_classes = [apps.get_model(ct.app_label, ct.model) for ct in content_types]
        self.assertEqual(
            Counter(classes),
            Counter(ct_classes),
        )

    def test_ple_video(self):
        """ can the PLE video (an example of video with description) be added as a PatientWalkthroughStep?"""

        ple_video = self.create_media(
            file_type="video",
            name="Welcome Video",
            description="This is the description for the Welcome Video",
        )

        media_content_type = ContentType.objects.get(
            model="media", app_label="awsmedia"
        )

        step = self.create_step(
            name="PLE Video",
            content_type=media_content_type,
            object_id=ple_video.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="videoDescription",
        )

        # join the step to the walkthrough
        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value["id"], step.content_object.id)

    def test_comfort_skills_puppies(self):
        """ Can the Comfort & Skill Video: Puppies (an example of video without description) be added as a PatientWalkthroughStep?"""
        puppy_video = self.create_media(
            file_type="video",
            name="Puppies",
            description="",
        )

        media_content_type = ContentType.objects.get(
            model="media", app_label="awsmedia"
        )

        step = self.create_step(
            name="Comfort & Skills Video",
            content_type=media_content_type,
            object_id=puppy_video.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="video",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value["id"], step.content_object.id)
        self.assertEqual(
            patient_walkthrough_step.value["name"], step.content_object.name
        )

    def test_paced_breathing(self):
        """ Can Paced Breathing be added as a PatientWalkthroughStep? """

        step = self.create_step(
            name="Paced Breathing",
            content_type=None,
            object_id=None,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="breathe",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value, None)

    def test_guide_message(self):
        """ Can Guide Message step be added as a PatientWalkthroughStep? """

        guide_message = self.create_guide_message(
            name="test guide message", message="text to display."
        )

        guide_content_type = ContentType.objects.get(
            model="guidemessage", app_label="kiosk"
        )

        step = self.create_step(
            name="Message from your Virtual Guide",
            content_type=guide_content_type,
            object_id=guide_message.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="guide",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(
            patient_walkthrough_step.value["message"], step.content_object.message
        )

    def test_physical_coping_strategy_uses_default_when_coping_body_empty(self):
        """ Can a physical coping strategy step be added as a PatientWalkthroughStep even without coping_bdoy data?"""

        go_for_a_walk = self.create_coping_strategy(
            name="Admin Name: Perambulate",  # not sure if there is a reason to have this field at this time...
            title="Go for a walk.",
            category=self.physical_coping_strategy_category,
        )

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        step = self.create_step(
            name="Physical Coping Strategy",
            content_type=coping_strategy_content_type,
            object_id=go_for_a_walk.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="copingStrategy",
            function="top_physical_coping_strategy",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(
            patient_walkthrough_step.value["title"], step.content_object.title
        )
        self.assertEqual(
            patient_walkthrough_step.value["image"],
            step.content_object.image.url,
        )

    def test_physical_coping_strategy_uses_breathe_when_no_default(self):
        """ Can a breathe app step be added when no default data and skip if blank =False?"""

        go_for_a_walk = self.create_coping_strategy(
            name="Admin Name: Perambulate",  # not sure if there is a reason to have this field at this time...
            title="Go for a walk.",
            category=self.physical_coping_strategy_category,
        )

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        step = self.create_step(
            name="Physical Coping Strategy",
            content_type=coping_strategy_content_type,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_physical_coping_strategy",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(patient_walkthrough_step.frontend_render_type, "breathe")
        self.assertEqual(patient_walkthrough_step.value, None)

    def test_physical_coping_strategy_chosen_from_crisis_stability_plan(self):
        """ Can a physical coping strategy step be chosen from coping_body as a PatientWalkthroughStep?"""

        go_for_a_walk = self.create_coping_strategy(
            name="Admin Name: Perambulate",  # not sure if there is a reason to have this field at this time...
            title="Go for a walk.",
            category=self.physical_coping_strategy_category,
        )

        sing = self.create_coping_strategy(
            name="Admin Name: Make Nice Sounds",  # not sure if there is a reason to have this field at this time...
            title="Sing.",
            category=self.physical_coping_strategy_category,
        )

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.coping_body = [go_for_a_walk.title, sing.title]
        crisis_stability_plan.save()
        self.manager.crisis_stability_plan = crisis_stability_plan

        step = self.create_step(
            name="Physical Coping Strategy",
            content_type=coping_strategy_content_type,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_physical_coping_strategy",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value["title"], go_for_a_walk.title)
        self.assertEqual(
            patient_walkthrough_step.value["image"],
            go_for_a_walk.image.url,
        )

    def test_physical_coping_strategy_be_found_in_patientcopingstrategy_if_in_crisis_stability_plan(
        self,
    ):
        """ Can a physical coping strategy step be chosen from PatientCopingStrategy for a PatientWalkthroughStep?"""

        sing = self.create_jah_patient_coping_strategy(
            jah_account=self.jah_account,
            title="Sing.",
            category=self.physical_coping_strategy_category,
        )

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy",
            app_label="kiosk",
        )

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.coping_body = [sing.title]
        crisis_stability_plan.save()
        self.manager.crisis_stability_plan = crisis_stability_plan

        step = self.create_step(
            name="Physical Coping Strategy",
            content_type=coping_strategy_content_type,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_physical_coping_strategy",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value["title"], sing.title)
        self.assertEqual(patient_walkthrough_step.value["image"], "")

    def test_image_found_on_readonlygenericcopingstrategyserializer(self):
        """ Is image url found on serializer??"""

        # this default image is sought by name and is required in the system.
        default_image = self.create_media(name="Custom Coping Strategy")

        sing = self.create_jah_patient_coping_strategy(
            jah_account=self.jah_account,
            title="Sing.",
            category=self.physical_coping_strategy_category,
        )

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy",
            app_label="kiosk",
        )

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.coping_body = [sing.title]
        crisis_stability_plan.save()
        self.manager.crisis_stability_plan = crisis_stability_plan

        step = self.create_step(
            name="Physical Coping Strategy",
            content_type=coping_strategy_content_type,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_physical_coping_strategy",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.value["image"], default_image.file_field.url
        )

    def test_lethal_means(self):
        """ Can My Steps to Make Home Safer step be added as a PatientWalkthroughStep? """

        step = self.create_step(
            name="My Steps to Make Home Safer",
            content_type=None,
            object_id=None,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="lethalMeans",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value, None)

    def test_generic_lethal_means(self):
        """ Can Making Home Safer step be added as a PatientWalkthroughStep? """

        make_home_safer_video = self.create_media(
            file_type="video",
            name="Make Home Safer",
            description="",
        )

        media_content_type = ContentType.objects.get(
            model="media", app_label="awsmedia"
        )

        step = self.create_step(
            name="Making Home Safer",
            content_type=media_content_type,
            object_id=make_home_safer_video.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="videoDescription",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value["id"], step.content_object.id)

    def test_national_hotline(self):
        """ Can a step to display a national hotline be added as a PatientWalkthroughStep? """

        national_hotline = self.create_helpline(
            name="National Hotline", phone="206 555 1212", text="206 777 1212"
        )

        helpline_content_type = ContentType.objects.get(
            model="helpline", app_label="kiosk"
        )

        step = self.create_step(
            name="Making Home Safer",
            content_type=helpline_content_type,
            object_id=national_hotline.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="nationalHotline",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(
            patient_walkthrough_step.value["name"], step.content_object.name
        )
        self.assertEqual(
            patient_walkthrough_step.value["phone"], step.content_object.phone
        )
        self.assertEqual(
            patient_walkthrough_step.value["text"], step.content_object.text
        )

    def test_recap(self):
        """ Can Recap step be added as a PatientWalkthroughStep? """

        step = self.create_step(
            name="Recap",
            content_type=None,
            object_id=None,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="recap",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value, None)

    def test_shared_stories(self):
        """ Can a step to display a shared story be added as a PatientWalkthroughStep? """

        shared_story = self.create_shared_story(
            person__name="Topher",
            topic__name="hope",
            video__name="Hope Video",
            video__description="something about this video",
        )

        sharedstory_content_type = ContentType.objects.get(
            model="sharedstory", app_label="kiosk"
        )

        step = self.create_step(
            name="Making Home Safer",
            content_type=sharedstory_content_type,
            object_id=shared_story.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="sharedStory",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )

        person_data = ReadOnlyPersonSerializer(shared_story.person).data
        topic_data = ReadOnlyTopicSerializer(shared_story.topic).data
        video_data = ReadOnlyVideoSerializer(shared_story.video).data

        self.assertEqual(patient_walkthrough_step.value["person"], person_data)
        self.assertEqual(patient_walkthrough_step.value["topic"], topic_data)
        self.assertEqual(patient_walkthrough_step.value["video"], video_data)

    def test_supportive_people_with_data_present(self):
        """ Can a step to display a supportive people be added as a PatientWalkthroughStep? """

        supportive_people = [
            {"name": "Daffy Duck", "phone": "415-555-2671"},
            {"name": "Buggz Bunny", "phone": ""},  # Should be valid.
            {"name": "", "phone": "415-555-2671"},  # Should be valid as well.
        ]

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.supportive_people = supportive_people
        crisis_stability_plan.save()

        # update the manager with the changes to crisis_stability_plan
        self.manager.crisis_stability_plan = crisis_stability_plan

        step = self.create_step(
            name="Supportive People",
            content_type=None,
            object_id=None,
            skip_if_blank=True,
            frontend_render_type="supportivePeople",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_steps = PatientWalkthroughStep.objects.filter(step=step)

        self.assertEqual(patient_walkthrough_steps.count(), 3)

        for index, supportive_person_step in enumerate(patient_walkthrough_steps):
            with self.subTest(supportive_person_step=supportive_person_step):

                self.assertEqual(
                    supportive_person_step.patient_walkthrough.walkthrough,
                    self.walkthrough,
                )
                self.assertEqual(
                    supportive_person_step.patient_walkthrough.patient, self.patient
                )
                self.assertEqual(
                    supportive_person_step.frontend_render_type,
                    step.frontend_render_type,
                )
                self.assertEqual(supportive_person_step.value, supportive_people[index])

    def test_supportive_people_with_no_supportive_people_empty_list(self):
        """ Will a step to display a supportive people be ignored when no data present (empty list)? """

        supportive_people = []

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.supportive_people = supportive_people
        crisis_stability_plan.save()

        step = self.create_step(
            name="Supportive People",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="supportivePeople",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)
        self.manager.handle()

        patient_walkthrough_steps = PatientWalkthroughStep.objects.filter(step=step)
        self.assertEqual(patient_walkthrough_steps.count(), 0)

    def test_supportive_people_with_no_supportive_people_none(self):
        """ Will a step to display a supportive people be ignored when no data present? """

        supportive_people = None

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.supportive_people = supportive_people
        crisis_stability_plan.save()

        step = self.create_step(
            name="Supportive People",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="supportivePeople",
        )
        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)
        self.manager.handle()

        patient_walkthrough_steps = PatientWalkthroughStep.objects.filter(step=step)
        self.assertEqual(patient_walkthrough_steps.count(), 0)

    def test_favorite_comfort_and_skill_defaults(self):
        """ Can a dynamically chosen favorite comfort and skill / activity be added to PatientWalkthroughStep? """

        puppy_video = self.create_media(
            file_type="video",
            name="Puppies",
            description="",
        )

        activity = self.create_activity(
            name="Puppies",
            video=puppy_video,
        )

        activity_content_type = ContentType.objects.get(
            model="activity", app_label="kiosk"
        )

        patient_activity = self.create_patient_activity(
            patient=self.patient,
            activity=activity,
            save_for_later=True,
        )

        step = self.create_step(
            name="Favorite Comfort & Skill",
            content_type=None,
            object_id=None,
            skip_if_blank=True,
            frontend_render_type="activity",
            function="favorite_activity",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough,
            self.walkthrough,
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type,
            "video",
        )
        self.assertEqual(
            patient_walkthrough_step.value, MediaSerializer(puppy_video).data
        )

    # TODO:  Need tests for ranking by rating, created,
    # TODO:  Need tests skip if blank with no activity favorited
    # TODO:  Need tests skip if blank -- false with no activity favorited, but rated returns paced breathing.

    def test_favorite_activity_no_favorite_no_skip(self):
        """ If no favorite, and not skip, will paced breathing be created as a PatientWalkthroughStep? """

        step = self.create_step(
            name="Favorite Comfort & Skill",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="activity",
            function="favorite_activity",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough,
            self.walkthrough,
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type,
            "breathe",
        )
        self.assertEqual(patient_walkthrough_step.value, None)
        self.assertEqual(patient_walkthrough_step.step, step)

    def test_favorite_activity_paced_breathing(self):
        """ Can a dynamically chosen favorite comfort and skill be added to PatientWalkthroughStep if it is paced breathing? """

        self.create_patient_activity(
            patient=self.patient,
            activity=self.paced_breathing_activity,
            save_for_later=True,
        )

        step = self.create_step(
            name="Favorite Comfort & Skill",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="activity",
            function="favorite_activity",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough,
            self.walkthrough,
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type,
            "breathe",
        )
        self.assertEqual(patient_walkthrough_step.value, None)
        self.assertEqual(patient_walkthrough_step.step, step)

    def test_favorite_activity_no_favorite_skip_if_blank(self):
        """ If no favorite, and skip, will no PatientWalkthroughStep be created? """

        step = self.create_step(
            name="Favorite Comfort & Skill",
            content_type=None,
            object_id=None,
            skip_if_blank=True,
            frontend_render_type="activity",
            function="favorite_activity",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.filter(
            step=step
        ).first()

        self.assertEqual(
            patient_walkthrough_step,
            None,
        )

    def test_top_three_non_physical_coping_strategies_single(self):
        """ Is top non physical coping strategy added as PatientWalkthroughStep """
        go_for_a_walk = self.create_coping_strategy(
            name="Admin Name: Perambulate",  # not sure if there is a reason to have this field at this time...
            title="Go for a walk.",
            category=self.physical_coping_strategy_category,
        )

        clean = self.create_coping_strategy(
            name="Clean a shared space",
            title="Clean a shared space",
        )

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.coping_top = [go_for_a_walk.title, clean.title]
        crisis_stability_plan.coping_senses = [clean.title]
        crisis_stability_plan.coping_body = [go_for_a_walk.title]
        crisis_stability_plan.save()
        self.manager.crisis_stability_plan = crisis_stability_plan

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        step = self.create_step(
            name="Top 3 Non-Physical Coping Strategies",
            content_type=coping_strategy_content_type,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_non_physical_coping_strategies",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value["title"], clean.title)
        self.assertEqual(
            patient_walkthrough_step.value["image"],
            clean.image.url,
        )

    def test_top_three_non_physical_coping_strategies_multiple(self):
        """ Are up to three physical coping strategies added as PatientWalkthroughStep """

        clean1 = self.create_coping_strategy(
            name="Clean a shared space1",
            title="Clean a shared space1",
        )
        clean2 = self.create_coping_strategy(
            name="Clean a shared space2",
            title="Clean a shared space2",
        )
        clean3 = self.create_coping_strategy(
            name="Clean a shared space3",
            title="Clean a shared space3",
        )
        clean4 = self.create_coping_strategy(
            name="Clean a shared space4",
            title="Clean a shared space4",
        )

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.coping_top = [
            clean1.title,
            clean2.title,
            clean3.title,
            clean4.title,
        ]
        crisis_stability_plan.coping_senses = [
            clean1.title,
            clean2.title,
            clean3.title,
            clean4.title,
        ]
        crisis_stability_plan.save()
        self.manager.crisis_stability_plan = crisis_stability_plan

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        step = self.create_step(
            name="Top 3 Non-Physical Coping Strategies",
            content_type=coping_strategy_content_type,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_non_physical_coping_strategies",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        self.assertEqual(PatientWalkthroughStep.objects.filter(step=step).count(), 3)

    def test_three_non_physical_coping_strategies_added_with_defaults(self):
        """ Can three physical coping strategies be added as PatientWalkthroughStep records from default if no non-physical in coping_top """

        # out of order on purpose
        clean3 = self.create_coping_strategy(
            name="Clean a shared space3",
            title="Clean a shared space3",
        )

        clean1 = self.create_coping_strategy(
            name="Clean a shared space1",
            title="Clean a shared space1",
        )
        clean2 = self.create_coping_strategy(
            name="Clean a shared space2",
            title="Clean a shared space2",
        )

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        step1 = self.create_step(
            name="Top 3 Non-Physical Coping Strategies - First",
            content_type=coping_strategy_content_type,
            object_id=clean1.pk,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_non_physical_coping_strategies",
        )
        step2 = self.create_step(
            name="Top 3 Non-Physical Coping Strategies - Second",
            content_type=coping_strategy_content_type,
            object_id=clean2.pk,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_non_physical_coping_strategies",
        )
        step3 = self.create_step(
            name="Top 3 Non-Physical Coping Strategies - Third",
            content_type=coping_strategy_content_type,
            object_id=clean3.pk,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_non_physical_coping_strategies",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step1, order=1)
        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step2, order=2)
        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step3, order=3)

        self.manager.handle()

        self.assertEqual(
            PatientWalkthroughStep.objects.filter(
                step__in=[step1, step2, step3]
            ).count(),
            3,
        )

    def test_top_three_non_physical_coping_strategies_when_only_one_is_present_but_multiple_steps_exist_with_this_function(
        self,
    ):
        """ Is one non physical coping strategy added as PatientWalkthroughStep even when other defaults avail?  """

        clean1 = self.create_coping_strategy(
            name="Clean a shared space1",
            title="Clean a shared space1",
        )

        clean2 = self.create_coping_strategy(
            name="Clean a shared space2",
            title="Clean a shared space2",
        )

        clean3 = self.create_coping_strategy(
            name="Clean a shared space3",
            title="Clean a shared space3",
        )
        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.coping_top = [clean1.title]
        crisis_stability_plan.coping_senses = [clean1.title]
        crisis_stability_plan.save()
        self.manager.crisis_stability_plan = crisis_stability_plan

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        step1 = self.create_step(
            name="Top 3 Non-Physical Coping Strategies - First blah",
            content_type=coping_strategy_content_type,
            object_id=clean2.pk,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_non_physical_coping_strategies",
        )

        step2 = self.create_step(
            name="Top 3 Non-Physical Coping Strategies - Second blah",
            content_type=coping_strategy_content_type,
            object_id=clean3.pk,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_non_physical_coping_strategies",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step1, order=1)
        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step2, order=2)

        # this should just create 1 pws
        self.manager.handle()

        patient_walkthrough_steps = PatientWalkthroughStep.objects.filter(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step__in=[step1, step2],
        )

        self.assertEqual(patient_walkthrough_steps.count(), 1)

        patient_walkthrough_step = patient_walkthrough_steps.first()
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step1.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value["title"], clean1.title)
        self.assertEqual(
            patient_walkthrough_step.value["image"],
            clean1.image.url,
        )

    def test_top_three_non_physical_coping_strategies_with_patient_coping_strategies(
        self,
    ):
        """
        Are non-physical patient coping strategies integrated with top_three_non_physical_coping_strategies?

        This test helps to resolve EBPI-880.
        """

        non_physical_coping_strategy_category = self.create_coping_strategy_category(
            name="Non-Physical"
        )
        patient_coping_strategy = self.create_jah_patient_coping_strategy(
            title="Custom Non-Physical",
            category=non_physical_coping_strategy_category,
            jah_account=self.jah_account,
        )

        clean1 = self.create_coping_strategy(
            name="Clean a shared space1",
            title="Clean a shared space1",
        )
        clean2 = self.create_coping_strategy(
            name="Clean a shared space2",
            title="Clean a shared space2",
        )

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.coping_top = [
            clean1.title,
            patient_coping_strategy.title,
            clean2.title,
        ]
        crisis_stability_plan.coping_senses = [
            patient_coping_strategy.title,
            clean2.title,
            clean1.title,
        ]
        crisis_stability_plan.save()
        self.manager.crisis_stability_plan = crisis_stability_plan

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        step = self.create_step(
            name="Top 3 Non-Physical Coping Strategies",
            content_type=coping_strategy_content_type,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_non_physical_coping_strategies",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_steps = PatientWalkthroughStep.objects.filter(
            step=step
        ).order_by("order")
        self.assertEqual(patient_walkthrough_steps.count(), 3)
        self.assertEqual(patient_walkthrough_steps.first().value["title"], clean1.title)
        self.assertEqual(patient_walkthrough_steps.last().value["title"], clean2.title)

    def test_top_three_non_physical_coping_strategies_with_patient_coping_strategies_from_multiple_patients(
        self,
    ):
        """
        Are non-physical patient coping strategies associated with only one patient found/shown?

        Related to EBPI-1060.  This error only shows up if cases differ.
        """

        non_physical_coping_strategy_category = self.create_coping_strategy_category(
            name="Non-Physical"
        )

        # creata a Patient Coping Strategy of a different patient.
        # This is the Patient Coping Strategy that causes the error when found.
        self.create_jah_patient_coping_strategy(
            title="Listen to Music", category=non_physical_coping_strategy_category
        )

        # This is the matching coping strategy that is not found because it is physical.
        patient_coping_strategy_physical = self.create_jah_patient_coping_strategy(
            title="listen to music",
            category=self.physical_coping_strategy_category,
            jah_account=self.jah_account,
        )

        # creating this just so a step will be built.
        patient_coping_strategy_non_physical = self.create_jah_patient_coping_strategy(
            title="read",
            category=non_physical_coping_strategy_category,
            jah_account=self.jah_account,
        )

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.coping_top = [
            patient_coping_strategy_physical.title,
            patient_coping_strategy_non_physical.title,
        ]
        crisis_stability_plan.coping_body = [
            patient_coping_strategy_physical.title,
        ]
        crisis_stability_plan.coping_distract = [
            patient_coping_strategy_non_physical.title,
        ]
        crisis_stability_plan.save()
        self.manager.crisis_stability_plan = crisis_stability_plan

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        step = self.create_step(
            name="Top 3 Non-Physical Coping Strategies",
            content_type=coping_strategy_content_type,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_non_physical_coping_strategies",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_steps = PatientWalkthroughStep.objects.filter(step=step)
        self.assertEqual(patient_walkthrough_steps.count(), 1)

    def test_favorite_shared_story(self):
        """ Can a favorite shared story be added dynamically from patient video?"""

        ple_video1 = self.create_media(
            file_type="video", name="Someone sharing", description="Description text1"
        )

        ple_video2 = self.create_media(
            file_type="video",
            name="Someone else sharing",
            description="Description text2",
        )

        self.create_shared_story(video=ple_video2, order=1, topic__order=1)
        self.create_shared_story(video=ple_video1, order=2, topic__order=2)

        self.create_patient_video(
            patient=self.patient, video=ple_video2, save_for_later=True
        )

        media_content_type = ContentType.objects.get(
            model="media", app_label="awsmedia"
        )

        step = self.create_step(
            name="Favorite Shared Story",
            content_type=media_content_type,
            object_id=ple_video1.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="video",
            function="favorite_shared_story",
        )

        # join the step to the walkthroughs
        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value["name"], ple_video2.name)

    def test_favorite_shared_story_with_no_favorites(self):
        """ Can a favorite shared story be added from defaults?"""

        ple_video1 = self.create_media(
            file_type="video", name="Someone sharing", description="Description text1"
        )

        media_content_type = ContentType.objects.get(
            model="media", app_label="awsmedia"
        )

        step = self.create_step(
            name="Favorite Shared Story",
            content_type=media_content_type,
            object_id=ple_video1.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="video",
            function="favorite_shared_story",
        )

        # join the step to the walkthrough
        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value["name"], ple_video1.name)

    def test_reasons_for_living(self):
        """ Can reasons for living step be added as a PatientWalkthroughStep? """

        step = self.create_step(
            name="Personalized RFL",
            content_type=None,
            object_id=None,
            skip_if_blank=True,
            frontend_render_type="reasonsForLiving",
        )

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.reasons_live = ["thing1", "thing2", "thing3"]
        crisis_stability_plan.save()

        self.manager.crisis_stability_plan = crisis_stability_plan

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(patient_walkthrough_step.value, ["thing1", "thing2", "thing3"])

    def test_reasons_for_living_blank(self):
        """ When reasons for living blank, is it skipped? """

        step = self.create_step(
            name="Personalized RFL",
            content_type=None,
            object_id=None,
            skip_if_blank=True,
            frontend_render_type="reasonsForLiving",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        self.assertEqual(PatientWalkthroughStep.objects.filter(step=step).count(), 0)

    def test_personalized_lethal_means(self):
        """ Can Personalized lethal means step be added as a PatientWalkthroughStep? """

        step = self.create_step(
            name="Personalized Lethal Means",
            content_type=None,
            object_id=None,
            skip_if_blank=True,
            frontend_render_type="personalizedLethalMeans",
        )

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.strategies_general = [
            "Store with trusted person, Dispose of method",
        ]
        crisis_stability_plan.strategies_firearm = [
            "Shooting range",
        ]
        crisis_stability_plan.strategies_medicine = [
            "Dump the drugs",
        ]
        crisis_stability_plan.strategies_places = [
            "Avoid location",
        ]
        crisis_stability_plan.strategies_other = [
            "do something else",
        ]
        crisis_stability_plan.strategies_custom = [
            "do something custom",
        ]
        crisis_stability_plan.means_support_who = "A good friend"

        crisis_stability_plan.save()
        self.manager.crisis_stability_plan = crisis_stability_plan

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(step=step)

        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.walkthrough, self.walkthrough
        )
        self.assertEqual(
            patient_walkthrough_step.patient_walkthrough.patient, self.patient
        )
        self.assertEqual(
            patient_walkthrough_step.frontend_render_type, step.frontend_render_type
        )
        self.assertEqual(
            Counter(patient_walkthrough_step.value),
            Counter(
                {
                    "strategies_general": crisis_stability_plan.strategies_general,
                    "strategies_firearm": crisis_stability_plan.strategies_firearm,
                    "strategies_medicine": crisis_stability_plan.strategies_medicine,
                    "strategies_places": crisis_stability_plan.strategies_places,
                    "strategies_other": crisis_stability_plan.strategies_other,
                    "strategies_custom": crisis_stability_plan.strategies_custom,
                    "means_support_who": crisis_stability_plan.means_support_who,
                }
            ),
        )

    def test_personalized_lethal_means_blank(self):
        """ Can Personalized RFL step be skipped if blank? """

        step = self.create_step(
            name="Personalized RFL",
            content_type=None,
            object_id=None,
            skip_if_blank=True,
            frontend_render_type="personalizedLethalMeans",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        self.assertEqual(PatientWalkthroughStep.objects.filter(step=step).count(), 0)

    def test_ordering_of_patient_walkthrough_steps(self):
        """ Can PatientWalkthroughSteps be ordered by related WalkthroughStep order? """

        middle_step = self.create_step(
            name="Breathe 2",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="breathe",
        )

        last_step = self.create_step(
            name="Breathe 3",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="breathe",
        )

        first_step = self.create_step(
            name="Breathe 1",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="breathe",
        )

        self.create_walkthrough_step(
            walkthrough=self.walkthrough, step=last_step, order=10
        )
        self.create_walkthrough_step(
            walkthrough=self.walkthrough, step=first_step, order=1
        )
        self.create_walkthrough_step(
            walkthrough=self.walkthrough, step=middle_step, order=5
        )

        self.manager.handle()

        pws_qs = PatientWalkthroughStep.objects.all()

        self.assertEqual(pws_qs.count(), 3)
        self.assertEqual(pws_qs.last().step, last_step)
        self.assertEqual(pws_qs.first().step, first_step)

    def test_deep_ordering_of_patient_walkthrough_steps(self):
        """ Is PatientWalkthroughSteps be ordered by their order field, instead of just by order of creation? """

        middle_step = self.create_step(
            name="Breathe 2",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="breathe",
        )

        last_step = self.create_step(
            name="Breathe 3",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="breathe",
        )

        first_step = self.create_step(
            name="Breathe 1",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="breathe",
        )

        patient_walkthrough = self.create_patient_walkthrough(
            patient=self.patient, walkthrough=self.walkthrough
        )

        pws2 = self.create_patient_wakthrough_step(
            patient_walkthrough=patient_walkthrough,
            step=middle_step,
            order=2,
        )

        pws1 = self.create_patient_wakthrough_step(
            patient_walkthrough=patient_walkthrough,
            step=first_step,
            order=1,
        )

        pws3 = self.create_patient_wakthrough_step(
            patient_walkthrough=patient_walkthrough, step=last_step, order=3
        )

        pws_qs = PatientWalkthroughStep.objects.all()

        self.assertEqual(pws_qs.count(), 3)
        self.assertEqual(pws_qs.last(), pws3)
        self.assertEqual(pws_qs.first(), pws1)

    def test_calling_handle_twice_inactivates_past_patient_walkthrough_and_patientwalkthroughsteps(
        self,
    ):
        """ Do we find 1 inactive and 1 active patient_walkthrough? """

        ple_video = self.create_media(
            file_type="video",
            name="Welcome Video",
            description="This is the description for the Welcome Video",
        )

        media_content_type = ContentType.objects.get(
            model="media", app_label="awsmedia"
        )

        step = self.create_step(
            name="PLE Video",
            content_type=media_content_type,
            object_id=ple_video.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="videoDescription",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()
        patient_walk1 = PatientWalkthrough.objects.get(
            patient=self.patient, walkthrough=self.walkthrough
        )
        pws1 = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        WalkthroughManager(self.patient).handle()
        inactive_pw = PatientWalkthrough.objects.get(
            patient=self.patient, walkthrough=self.walkthrough, status="inactive"
        )
        active_pw = PatientWalkthrough.objects.get(
            patient=self.patient, walkthrough=self.walkthrough, status="active"
        )

        inactive_pws = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
            status="inactive",
        )
        active_pws = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
            status="active",
        )

        patient_walk1.refresh_from_db()
        self.assertEqual(patient_walk1.status, "inactive")
        self.assertEqual(patient_walk1, inactive_pw)

        pws1.refresh_from_db()
        self.assertEqual(pws1.status, "inactive")
        self.assertEqual(inactive_pws.patient_walkthrough, inactive_pw)

        self.assertEqual(active_pws.patient_walkthrough, active_pw)

    def test_calling_handle_doesnt_inactivate_other_patient_walkthroughs(self):

        """ Are other patient's walkthroughpatientstep and walkthroughpatient still active? """

        ple_video = self.create_media(
            file_type="video",
            name="Welcome Video",
            description="This is the description for the Welcome Video",
        )

        media_content_type = ContentType.objects.get(
            model="media", app_label="awsmedia"
        )

        step = self.create_step(
            name="PLE Video",
            content_type=media_content_type,
            object_id=ple_video.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="videoDescription",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        # need to create a pre-existing walkthrough that is in place already to see the potential problem
        WalkthroughManager(self.patient).handle()

        # create a different pre-existing patient with walkthrough data

        other_patient = self.create_patient()
        other_patient_walkthrough = self.create_patient_walkthrough(
            patient=other_patient, walkthrough=self.walkthrough
        )
        other_pws = self.create_patient_wakthrough_step(
            patient_walkthrough=other_patient_walkthrough, step=step
        )

        WalkthroughManager(self.patient).handle()

        # should still have only 1 active
        PatientWalkthrough.objects.get(
            patient=self.patient, walkthrough=self.walkthrough, status="active"
        )
        PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
            status="active",
        )

        other_patient_walkthrough.refresh_from_db()
        other_pws.refresh_from_db()
        self.assertEqual(other_patient_walkthrough.status, "active")
        self.assertEqual(other_pws.status, "active")

    def test_existing_but_archived_patient_coping_strategies_are_respected_by_top_physical_coping_strategy(
        self,
    ):
        """ When a patient coping strategy is present but archived, it is found and used by top_physical_coping_strategy."""

        patient_coping_strategy = self.create_jah_patient_coping_strategy(
            title="CUSTOM",
            category=self.physical_coping_strategy_category,
            jah_account=self.jah_account,
            status="archived",
        )

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.coping_body = [patient_coping_strategy.title]
        crisis_stability_plan.save()
        self.manager.crisis_stability_plan = crisis_stability_plan

        step = self.create_step(
            name="Physical Coping Strategy",
            content_type=coping_strategy_content_type,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="copingStrategy",
            function="top_physical_coping_strategy",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        self.manager.handle()

        # should still have only 1 active
        PatientWalkthrough.objects.get(
            patient=self.patient, walkthrough=self.walkthrough, status="active"
        )
        PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
            status="active",
        )
