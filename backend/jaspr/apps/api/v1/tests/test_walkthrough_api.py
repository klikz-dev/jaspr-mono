from django.contrib.contenttypes.models import ContentType
from rest_framework import status

from jaspr.apps.api.v1.serializers import (
    MediaSerializer,
    ReadOnlyPersonSerializer,
    ReadOnlyTopicSerializer,
)
from jaspr.apps.jah.models import JAHAccount, CrisisStabilityPlan
from jaspr.apps.stability_plan.models import (
    PatientWalkthrough,
    PatientWalkthroughStep,
)
from jaspr.apps.stability_plan.walkthrough_manager import WalkthroughManager
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestPatientWalkthroughAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="patient/walkthrough",
            version_prefix="v1",
            factory_name="create_walkthrough",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Patient"]

        self.detail_uri = self.base_uri


class TestPatientWalkthroughAPIWithoutFirstCallingWalkthroughManager(JasprApiTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/walkthrough"

        self.department = self.create_department()

        self.patient = self.create_patient(
            ssid="test-patient-1"
        )
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.jah_account = JAHAccount.objects.create(patient=self.patient)
        self.jah_csp = CrisisStabilityPlan.objects.create(jah_account=self.jah_account)
        self.set_patient_creds(self.patient)
        self.walkthrough = self.create_walkthrough(name="Default")
        self.physical_coping_strategy_category = self.create_coping_strategy_category(
            name="Physical", slug="physical"
        )
        self.paced_breathing_activity = self.create_activity(
            name="Paced Breathing",
            target_url="/breathe",
        )

    def test_favorite_shared_stories_without_favorited_video(self):
        """
        Can a step to display a shared story be created,
        without first calling manager or having a favorited video?
        """

        ple_video1 = self.create_media(
            file_type="video", name="Someone sharing", description="Description text1"
        )

        shared_story = self.create_shared_story(
            video=ple_video1, order=1, topic__order=1
        )

        shared_story_content_type = ContentType.objects.get(
            model="sharedstory", app_label="kiosk"
        )

        step = self.create_step(
            name="Favorite Shared Story",
            content_type=shared_story_content_type,
            object_id=shared_story.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="sharedStory",
            function="favorite_shared_story",
        )

        # join the step to the walkthroughs
        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            "video",
        )
        self.assertEqual(obj_data["value"]["name"], ple_video1.name)


class TestPatientWalkthroughAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/patient/walkthrough"

        self.department = self.create_department()

        self.patient = self.create_patient(
            ssid="test-patient-1"
        )
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )

        self.jah_account = JAHAccount.objects.create(patient=self.patient)
        self.jah_csp = CrisisStabilityPlan.objects.create(jah_account=self.jah_account)
        self.set_patient_creds(self.patient, from_native=True)
        self.walkthrough = self.create_walkthrough(name="Default")

        self.physical_coping_strategy_category = self.create_coping_strategy_category(
            name="Physical", slug="physical"
        )
        self.paced_breathing_activity = self.create_activity(
            name="Paced Breathing",
            target_url="/breathe",
        )
        self.manager = WalkthroughManager(
            patient=self.patient, walkthrough=self.walkthrough
        )

    def test_list(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_ple_video(self):
        """ can the PLE video (an example of video with description) be seen in steps?"""

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

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(
            obj_data["value"]["id"], patient_walkthrough_step.step.object_id
        )

    def test_comfort_skills_puppies(self):
        """ Can the Comfort & Skill Video: Puppies (an example of video without description) be seen in walkthrough?"""
        puppy_video = self.create_media(
            file_type="video",
            name="Puppies without description",
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

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(
            obj_data["value"]["id"], patient_walkthrough_step.step.object_id
        )
        self.assertEqual(obj_data["value"]["name"], puppy_video.name)

    def test_paced_breathing(self):
        """ Can Paced Breathing step be added as a patient walkthrough step? """

        step = self.create_step(
            name="Paced Breathing",
            content_type=None,
            object_id=None,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="breathe",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(obj_data["value"], None)

    def test_guide_message(self):
        """ Can Guide Message step be added as a patient walkthrough step? """

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

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(obj_data["value"]["message"], guide_message.message)

    def test_physical_coping_strategy(self):
        """ Can a physical coping strategy step be cnnnected rendered as a patient step on the walkthrough"""

        go_for_a_walk = self.create_coping_strategy(
            name="Admin Name: Perambulate",  # not sure if there is a reason to have this field at this time...
            title="Go for a walk.",
            # image
            category__name="physical",
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
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(obj_data["value"]["title"], go_for_a_walk.title)
        self.assertEqual(obj_data["value"]["image"], go_for_a_walk.image.url)

    def test_favorite_comfort_skills_video(self):
        """ Can the Favorite Comfort & Skill Video: Puppies (an example of video without description) be seen in walkthrough?"""

        # currently just testing if a video can be shown...

        puppy_video = self.create_media(
            file_type="video",
            name="Puppies without description",
            description="",
        )

        media_content_type = ContentType.objects.get(
            model="media", app_label="awsmedia"
        )

        step = self.create_step(
            name="Coping Skills",
            content_type=media_content_type,
            object_id=puppy_video.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="video",
            # TODO seems like it is missing a function
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(
            obj_data["value"]["id"], patient_walkthrough_step.step.object_id
        )
        self.assertEqual(obj_data["value"]["name"], puppy_video.name)

    def test_reasons_for_living(self):
        """ Can Reasons For Living step be added as a patient walkthrough step? """

        step = self.create_step(
            name="Reasons for Living",
            content_type=None,
            object_id=None,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="reasonsForLiving",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        crisis_stability_plan = self.jah_csp
        crisis_stability_plan.reasons_live = ["thing1", "thing2", "thing3"]
        crisis_stability_plan.save()

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(obj_data["value"], ["thing1", "thing2", "thing3"])

    def test_lethal_means(self):
        """ Can My Steps to Make Home Safer step be added as a patient walkthrough step? """

        step = self.create_step(
            name="My Steps to Make Home Safer",
            content_type=None,
            object_id=None,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="lethalMeans",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(obj_data["value"], None)

    def test_personalized_lethal_means(self):
        """ Can Making Home Safer step be added as a patient walkthrough step? """

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

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(obj_data["value"]["name"], make_home_safer_video.name)

    def test_national_hotline(self):
        """ Can a step to display a national hotline be one of the patient steps? """

        national_hotline = self.create_helpline(
            name="National Hotline", phone="206 555 1212", text="206 777 1212"
        )

        helpline_content_type = ContentType.objects.get(
            model="helpline", app_label="kiosk"
        )

        step = self.create_step(
            name="National Hotline",
            content_type=helpline_content_type,
            object_id=national_hotline.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="nationalHotline",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)

        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(obj_data["value"]["name"], national_hotline.name)
        self.assertEqual(obj_data["value"]["phone"], national_hotline.phone)
        self.assertEqual(obj_data["value"]["text"], national_hotline.text)

    def test_recap(self):
        """ Can Recap step be added as a patient walkthrough step? """

        step = self.create_step(
            name="Recap",
            content_type=None,
            object_id=None,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="recap",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )
        self.assertEqual(obj_data["value"], None)

    def test_shared_stories(self):
        """ Can a step to display a shared stories be one of the patient steps? """

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

        response = self.client.get(self.uri)

        patient_walkthrough_step = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 1)
        obj_data = response.data[0]
        self.assertEqual(len(obj_data), 3)
        self.assertTrue("step_name" in obj_data)
        self.assertTrue("frontend_render_type" in obj_data)
        self.assertTrue("value" in obj_data)
        self.assertEqual(obj_data["step_name"], patient_walkthrough_step.step.name)
        self.assertEqual(
            obj_data["frontend_render_type"],
            patient_walkthrough_step.frontend_render_type,
        )

        person_data = ReadOnlyPersonSerializer(shared_story.person).data
        topic_data = ReadOnlyTopicSerializer(shared_story.topic).data
        video_data = MediaSerializer(shared_story.video).data

        # note <= is a subset operator
        self.assertTrue(obj_data["value"]["person"].items() <= person_data.items())
        self.assertTrue(obj_data["value"]["topic"].items() <= topic_data.items())
        self.assertTrue(obj_data["value"]["video"].items() <= video_data.items())

        person_data = ReadOnlyPersonSerializer(shared_story.person).data
        topic_data = ReadOnlyTopicSerializer(shared_story.topic).data
        video_data = MediaSerializer(shared_story.video).data

        # note <= is a subset operator
        self.assertTrue(obj_data["value"]["person"].items() <= person_data.items())
        self.assertTrue(obj_data["value"]["topic"].items() <= topic_data.items())
        self.assertTrue(obj_data["value"]["video"].items() <= video_data.items())

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
        self.manager.crisis_stability_plan = crisis_stability_plan

        step = self.create_step(
            name="Supportive People",
            content_type=None,
            object_id=None,
            skip_if_blank=True,
            frontend_render_type="supportivePeople",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step)

        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 3)

        for index, supportive_person_step in enumerate(response.data):
            with self.subTest(supportive_person_step=supportive_person_step):
                self.assertEqual(len(supportive_person_step), 3)
                self.assertTrue("step_name" in supportive_person_step)
                self.assertTrue("frontend_render_type" in supportive_person_step)
                self.assertTrue("value" in supportive_person_step)

                self.assertEqual(
                    supportive_person_step["step_name"],
                    step.name,
                )

                self.assertEqual(
                    supportive_person_step["frontend_render_type"],
                    step.frontend_render_type,
                )
                self.assertEqual(
                    supportive_person_step["value"], supportive_people[index]
                )

    def test_calling_url_with_an_existing_active_patient_walkthrough_doesnt_change_existing_patient_walkthrough(
        self,
    ):
        """ Do we find just 1 Patient Walkthrough if we call walkthough endpoint twice? """

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

        self.client.get(self.uri)
        patient_walk1 = PatientWalkthrough.objects.get(
            patient=self.patient, walkthrough=self.walkthrough
        )
        pws1 = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.client.get(self.uri)
        patient_walk2 = PatientWalkthrough.objects.get(
            patient=self.patient, walkthrough=self.walkthrough
        )
        pws2 = PatientWalkthroughStep.objects.get(
            patient_walkthrough__patient=self.patient,
            patient_walkthrough__walkthrough=self.walkthrough,
            step=step,
        )

        self.assertEqual(patient_walk1, patient_walk2)
        self.assertEqual(pws1, pws2)

    def test_default_user_for_simple_history_is_patient_user(self):
        """ Is the user associated with patient, the user who is recorded on simplehistory? """

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
        pws_history = patient_walkthrough_step.history.first()
        self.assertEqual(pws_history.history_user, self.patient.user)

        patient_walkthrough_history = (
            patient_walkthrough_step.patient_walkthrough.history.first()
        )
        self.assertEqual(patient_walkthrough_history.history_user, self.patient.user)

        # now test the update
        self.manager.handle()
        pws_history = patient_walkthrough_step.history.first()
        self.assertEqual(pws_history.history_user, self.patient.user)

        patient_walkthrough_history = (
            patient_walkthrough_step.patient_walkthrough.history.first()
        )
        self.assertEqual(patient_walkthrough_history.history_user, self.patient.user)

    def test_ordering_of_patient_walkthrough_steps_unaffected_by_name_or_chronology(
        self,
    ):
        """ Are PatientWalkthroughSteps ordered by their related WalkthroughStep? """

        # making sure that name and order of creation doesn't affect order.
        middle_step = self.create_step(
            name="X. Breathe 2",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="breathe",
        )

        last_step = self.create_step(
            name="Y. Breathe 3",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="breathe",
        )

        first_step = self.create_step(
            name="Z. Breathe 1",
            content_type=None,
            object_id=None,
            skip_if_blank=False,
            frontend_render_type="breathe",
        )

        self.create_walkthrough_step(
            walkthrough=self.walkthrough, step=last_step, order=10
        )
        self.create_walkthrough_step(
            walkthrough=self.walkthrough, step=middle_step, order=5
        )
        self.create_walkthrough_step(
            walkthrough=self.walkthrough, step=first_step, order=1
        )

        response = self.client.get(self.uri)
        self.assertEqual(response.data[0]["step_name"], first_step.name)
        self.assertEqual(response.data[1]["step_name"], middle_step.name)
        self.assertEqual(response.data[2]["step_name"], last_step.name)

    def test_ordering_of_patient_walkthrough_steps_unaffected_by_type_of_step(self):
        """ Are PatientWalkthroughSteps ordered by their related WalkthroughStep despite step type? """

        go_for_a_walk = self.create_coping_strategy(
            name="Admin Name: Perambulate",  # not sure if there is a reason to have this field at this time...
            title="Go for a walk.",
            # image
            category__name="physical",
        )

        coping_strategy_content_type = ContentType.objects.get(
            model="copingstrategy", app_label="kiosk"
        )

        step2 = self.create_step(
            name="Physical Coping Strategy",
            content_type=coping_strategy_content_type,
            object_id=go_for_a_walk.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="copingStrategy",
        )

        guide_message = self.create_guide_message(
            name="test guide message", message="text to display."
        )

        guide_content_type = ContentType.objects.get(
            model="guidemessage", app_label="kiosk"
        )

        step1 = self.create_step(
            name="Message from your Virtual Guide",
            content_type=guide_content_type,
            object_id=guide_message.pk,
            skip_if_blank=False,  # just here for documentation
            frontend_render_type="guide",
        )

        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step1, order=10)
        self.create_walkthrough_step(walkthrough=self.walkthrough, step=step2, order=20)

        response = self.client.get(self.uri)
        self.assertEqual(response.data[0]["step_name"], step1.name)
        self.assertEqual(response.data[1]["step_name"], step2.name)
