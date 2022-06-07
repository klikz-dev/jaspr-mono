from jaspr.apps.api.v1.serializers import (
    ReadOnlyActivitySerializer,
    ReadOnlyPatientActivitySerializer,
)
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestActivityAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="patient/activities",
            version_prefix="v1",
            factory_name="create_activity",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Patient"]


class TestActivityAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/patient/activities"
        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)
        self.set_patient_creds(self.patient, encounter=self.encounter)

    def test_list(self):
        first_activity = self.create_activity()
        second_activity = self.create_activity()
        third_activity = self.create_activity()
        fourth_activity = self.create_activity()
        l = locals()
        id_to_activity = {l[k].id: l[k] for k in l if k.endswith("_activity")}
        self.assertEqual(
            len(id_to_activity),
            4,
            "Test assertion: Should have four activites exactly in this dictionary.",
        )

        first_patient_activity = self.create_patient_activity(
            patient=self.patient, activity=first_activity
        )
        # There won't be a second patient activity in this test, so there
        # should be a `None` returned for that one once we get there.
        third_patient_activity = self.create_patient_activity(
            patient=self.patient, activity=third_activity
        )
        id_to_patient_activity = {
            first_patient_activity.id: first_patient_activity,
            third_patient_activity.id: third_patient_activity,
        }

        # Will have a different `patient`.
        first_other_patient_activity = self.create_patient_activity(
            activity=first_activity
        )
        fourth_other_patient_activity = self.create_patient_activity(
            patient=first_other_patient_activity.patient, activity=fourth_activity,
        )

        response = self.client.get(self.uri)
        id_set = set(map(lambda item: item["id"], response.data))
        patient_activity_id_list = list(
            map(lambda item: item["patient_activity"], response.data)
        )
        expected_field_names = set(
            ReadOnlyActivitySerializer.Meta.fields + ["patient_activity"]
        )

        self.assertEqual(
            id_set,
            {
                first_activity.id,
                second_activity.id,
                third_activity.id,
                fourth_activity.id,
            },
        )
        self.assertEqual(1, patient_activity_id_list.count(first_patient_activity.id))
        self.assertEqual(1, patient_activity_id_list.count(third_patient_activity.id))
        self.assertEqual(2, patient_activity_id_list.count(None))
        for item in response.data:
            activity = id_to_activity[item["id"]]
            # Check one attribute here just to make sure it's the correct name corresponding
            # to that activity.
            self.assertEqual(item["name"], activity.name)
            if item["patient_activity"] is None:
                self.assertEqual(set(item.keys()), expected_field_names)
                # Check one attribute here just to make sure it's correctly
                # not in the data (I.E. not being flattened since
                # `patient_activity` is `None`).
                self.assertNotIn("rating", response.data)
            else:
                self.assertEqual(
                    set(item.keys()),
                    expected_field_names.union(
                        ReadOnlyPatientActivitySerializer.Meta.fields
                    ),
                )
                patient_activity = id_to_patient_activity[item["patient_activity"]]
                self.assertEqual(activity.id, patient_activity.activity_id)
                # Check one attribute here just to make sure it's the correct rating
                # corresponding to that patient activity.
                self.assertEqual(item["rating"], patient_activity.rating)

    def test_retrieve(self):
        activity = self.create_activity()
        second_activity = self.create_activity()
        patient_activity = self.create_patient_activity(
            patient=self.patient, activity=activity
        )

        response = self.client.get(f"{self.uri}/{activity.id}")
        self.assertEqual(response.data["id"], activity.id)
        self.assertEqual(response.data["name"], activity.name)
        self.assertEqual(response.data["patient_activity"], patient_activity.id)
        self.assertEqual(response.data["rating"], patient_activity.rating)

        response = self.client.get(f"{self.uri}/{second_activity.id}")
        self.assertEqual(response.data["id"], second_activity.id)
        self.assertEqual(response.data["name"], second_activity.name)
        self.assertEqual(response.data["patient_activity"], None)
        self.assertNotIn("rating", response.data)
