from django.db import connection
from django.test.utils import CaptureQueriesContext
from jaspr.apps.api.v1.serializers import (
    ReadOnlyPersonSerializer,
    ReadOnlySharedStorySerializer,
    ReadOnlyTopicSerializer,
    ReadOnlyVideoSerializer,
)
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


class TestSharedStoryAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="shared-stories",
            version_prefix="v1",
            factory_name="create_shared_story",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Patient"]


class TestSharedStoryAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/shared-stories"
        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)
        self.set_patient_creds(self.patient, encounter=self.encounter)

    def test_list(self):
        person_one = self.create_person(name="Person One", order=2)
        person_two = self.create_person(name="Person Two", order=1)
        person_three = self.create_person(name="Person Three", order=3)
        topic_one = self.create_topic(name="Topic One", order=2)
        topic_two = self.create_topic(name="Topic Two", order=1)
        topic_three = self.create_topic(name="Topic Three", order=3)
        topic_four = self.create_topic(name="Topic Four", order=4)
        video_one = self.create_media(name="Video One")
        video_two = self.create_media(name="Video Two", tags="PLE")
        video_three = self.create_media(name="Video Three")
        video_four = self.create_media(name="Video Four", tags="PLE,laser,beam")
        video_five = self.create_media(name="Video Five", tags="PLE,lazer,beam")
        video_six = self.create_media(name="Video Six")
        video_seven = self.create_media(name="Video Seven", tags="PLE")
        story_one = self.create_shared_story(
            person=person_one, topic=topic_one, video=video_one, order=3
        )
        story_two = self.create_shared_story(
            person=person_one, topic=topic_two, video=video_two, order=1
        )
        story_three = self.create_shared_story(
            person=person_two, topic=topic_one, video=video_three, order=2
        )
        story_four = self.create_shared_story(
            person=person_two, topic=topic_two, video=video_four, order=4
        )
        story_five = self.create_shared_story(
            person=person_one, topic=topic_three, video=video_five, order=5
        )
        # Should not show up because it is archived.
        story_six = self.create_shared_story(
            status="archived",
            person=person_two,
            topic=topic_three,
            video=video_six,
            order=0,
        )
        story_seven = self.create_shared_story(
            person=person_three, topic=topic_four, video=video_seven, order=6
        )

        with CaptureQueriesContext(connection) as capture_queries_context:
            response = self.client.get(self.uri)
        num_queries = len(capture_queries_context.captured_queries)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
        # Just check three of the responses (for fields + ordering).
        first = response.data[0]
        third = response.data[2]
        fifth = response.data[4]

        self.assertEqual(first["id"], story_two.pk)
        self.assertEqual(first["order"], 1)
        self.assertEqual(
            list(first["person"].keys()), ReadOnlyPersonSerializer.Meta.read_only_fields
        )
        self.assertEqual(
            list(first["topic"].keys()), ReadOnlyTopicSerializer.Meta.read_only_fields
        )
        self.assertEqual(
            list(first["video"].keys()), ReadOnlyVideoSerializer.Meta.read_only_fields
        )
        self.assertEqual(first["person"]["name"], "Person One")
        self.assertEqual(first["topic"]["name"], "Topic Two")
        self.assertEqual(first["video"]["name"], "Video Two")
        self.assertEqual(first["video"]["tags"], ["PLE"])

        self.assertEqual(third["id"], story_one.pk)
        self.assertEqual(third["order"], 3)
        self.assertEqual(
            list(third["person"].keys()),
            ReadOnlyPersonSerializer.Meta.read_only_fields,
        )
        self.assertEqual(
            list(third["topic"].keys()), ReadOnlyTopicSerializer.Meta.read_only_fields
        )
        self.assertEqual(
            list(third["video"].keys()), ReadOnlyVideoSerializer.Meta.read_only_fields
        )
        self.assertEqual(third["person"]["name"], "Person One")
        self.assertEqual(third["topic"]["name"], "Topic One")
        self.assertEqual(third["video"]["name"], "Video One")
        self.assertEqual(third["video"]["tags"], [])

        self.assertEqual(fifth["id"], story_five.pk)
        self.assertEqual(fifth["order"], 5)
        self.assertEqual(
            list(fifth["person"].keys()), ReadOnlyPersonSerializer.Meta.read_only_fields
        )
        self.assertEqual(
            list(fifth["topic"].keys()), ReadOnlyTopicSerializer.Meta.read_only_fields
        )
        self.assertEqual(
            list(fifth["video"].keys()), ReadOnlyVideoSerializer.Meta.read_only_fields
        )
        self.assertEqual(fifth["person"]["name"], "Person One")
        self.assertEqual(fifth["topic"]["name"], "Topic Three")
        self.assertEqual(fifth["video"]["name"], "Video Five")
        self.assertEqual(fifth["video"]["tags"], ["PLE", "beam", "lazer"])

        # Sanity check and `select_related` (maybe also `prefetch_related` in the
        # future if necessary) check: Make sure we grabbed all the shared stories and
        # related data efficiently. NOTE: At the time of writing the actual number of
        # queries, including middleware (authentication, etc.) is `8`, so if we add
        # another request somewhere we'll have to update this test or give it more
        # cushion.
        self.assertLessEqual(num_queries, 8)

    def test_retrieve(self):
        story_one = self.create_shared_story(status="active", order=3, topic__order=3)
        # Should not be retrievable because it's archived.
        story_two = self.create_shared_story(status="archived", order=1, topic__order=1)

        response = self.client.get(f"{self.uri}/{story_one.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], story_one.pk)
        self.assertEqual(response.data["order"], 3)

        field_names = list(response.data["person"].keys())
        self.assertEqual(
            field_names, ReadOnlyPersonSerializer.Meta.read_only_fields,
        )
        self.assertEqual(len(field_names), 7)

        field_names = list(response.data["topic"].keys())
        self.assertEqual(
            field_names, ReadOnlyTopicSerializer.Meta.read_only_fields,
        )
        self.assertEqual(len(field_names), 4)

        self.assertEqual(
            list(response.data["video"].keys()),
            ReadOnlyVideoSerializer.Meta.read_only_fields,
        )

        response = self.client.get(f"{self.uri}/{story_two.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
