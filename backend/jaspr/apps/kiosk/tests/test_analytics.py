import operator
import random
import sys
import pytz
from datetime import datetime, timedelta, date

from django.utils import timezone

from jaspr.apps.kiosk.models import Encounter
from jaspr.apps.kiosk.analytics import AnalyticsExporter
from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.test_infrastructure.testcases import JasprTestCase
from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from jaspr.apps.kiosk.activities.question_json import extract_answer_keys_from_json


class TestAnalyticsData(JasprTestCase):
    def setUp(self):
        self.system = self.create_healthcare_system()
        self.clinic = self.create_clinic(system=self.system)
        self.first_department = self.create_department(
            name="First Dept",
            clinic=self.clinic,
        )
        self.second_department = self.create_department(
            name="Second Dept",
            clinic=self.clinic,
        )

        self.first_technician = self.create_technician(
            system=self.system, department=self.first_department
        )
        self.second_technician = self.create_technician(
            system=self.system, department=self.second_department
        )
        self.first_patient = self.create_patient()
        self.second_patient = self.create_patient()
        self.third_patient = self.create_patient()
        self.first_patient_encounter = self.create_patient_encounter(
            patient=self.first_patient, department=self.first_department
        )
        self.first_patient_encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        self.second_patient_encounter = self.create_patient_encounter(
            patient=self.second_patient, department=self.first_department
        )
        self.second_patient_encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        self.third_patient_encounter = self.create_patient_encounter(
            patient=self.third_patient, department=self.second_department
        )
        self.third_patient_encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        self.exporter = AnalyticsExporter(self.system, date(2020, 1, 1), date(2100, 1, 1), include_mrn=True,
                                     include_analytics_token=True)

    @property
    def now(self):
        return timezone.now()

    @property
    def incrementing_times(self):
        next_time = self.now
        while True:
            yield next_time
            next_time = timedelta(
                days=random.choice(range(0, 4)), seconds=random.choice(range(0, 60))
            )

    @property
    def next_incremented_time(self):
        return next(self.incrementing_times)

    def format_value_if_timestamp(self, value):
        if isinstance(value, datetime):
            tz = pytz.timezone("America/Los_Angeles")
            # Allow the timestamp to be generated properly locally for testing purposes
            # if the local machine is a windows machine.
            day_format = "%#d" if sys.platform == "win32" else "%d"
            return value.astimezone(tz).strftime("%B {0}, %Y %I:%M:%S %p %Z".format(day_format))
        return value

    def datetime_handling_retriever(self, *attrs):
        assert (
            len(attrs) >= 2
        ), "We only support >= 2 arguments (for `*attrs`) at this point."
        retriever = operator.attrgetter(*attrs)

        def f(a):
            return [*map(self.format_value_if_timestamp, retriever(a))]

        return f

    def action_retriever(self):
        def f(a):
            action_name = a.action
            if (
                action_name in (ActionNames.ARRIVE, ActionNames.SUBMIT)
                and a.section_uid
            ):
                action_name = f"{action_name} {a.section_uid}"
            elif (
                action_name
                in (
                    ActionNames.WATCH,
                    ActionNames.JAH_WALKTHROUGH_ARRIVE,
                    ActionNames.JAH_WALKTHROUGH_CLICKED_MORE_INFO,
                    ActionNames.JAH_USER_COPY,
                    ActionNames.JAH_OPEN_CONCERN,
                )
                and a.extra
            ):
                action_name = f"{action_name} {a.extra}"
            return [
                a.patient.analytics_token,
                a.patient.mrn,
                a.in_er,
                action_name,
                a.screen,
                self.format_value_if_timestamp(a.timestamp),
                self.format_value_if_timestamp(a.client_timestamp),
            ]

        return f

    def test_clinic_and_department_count(self):
        """
        Can we query for the clinic created at Setup?
        """
        clinics = list(self.system.get_clinics())
        departments = self.system.get_departments()
        self.assertEqual(len(clinics), 1, "Incorrect number of clinics. Expected 1.")
        self.assertEqual(
            len(departments), 2, "Incorrect number of departments. Expected 2."
        )

    def test_only_retrieves_from_current_clinic(self):
        """
        Does an export file retrieve data only from the current clinic?

        NOTE: Since logic is shared using cached `departments`, we
        are only going to test one example.
        """
        first_action = self.create_action(patient=self.first_patient, encounter=self.first_patient_encounter)
        second_action = self.create_action(patient=self.first_patient, encounter=self.first_patient_encounter)
        third_action = self.create_action(patient=self.second_patient, encounter=self.second_patient_encounter)

        system, clinic, department = self.create_full_healthcare_system(
            name="Another System"
        )
        other_patient = self.create_patient()
        other_encounter = self.create_patient_encounter(
            patient=other_patient, department=department
        )
        other_action = self.create_action(
            patient=other_patient, encounter=other_encounter
        )

        data = [*self.exporter.action_log_iterator]
        self.assertEqual(len(data), 4)
        self.assertFalse(any(map(lambda row: row[0] == other_patient.id, data[1:])))

    def test_visit_log_iterator(self):
        first_record = self.create_activate_record(
            technician=self.first_technician,
            patient=self.first_patient,
            encounter=self.first_patient_encounter,
            timestamp=self.next_incremented_time,
        )
        second_record = self.create_activate_record(
            technician=self.first_technician,
            patient=self.second_patient,
            encounter=self.second_patient_encounter,
            timestamp=self.next_incremented_time,
        )
        third_record = self.create_activate_record(
            technician=self.second_technician,
            patient=self.first_patient,
            encounter=self.first_patient_encounter,
            timestamp=self.next_incremented_time,
        )

        data = [*self.exporter.visit_log_iterator]

        self.assertEqual(len(data), 4)
        retriever = self.datetime_handling_retriever(
            "patient.analytics_token",
            "patient.mrn",
            "technician_id",
            "timestamp",
            "encounter.department.name",
        )
        self.assertEqual(
            data[0],
            [
                "Analytics Token",
                "MRN",
                "Technician ID",
                "Visit Timestamp",
                "Clinic Department",
            ],
        )
        self.assertEqual(data[1], retriever(first_record))
        self.assertEqual(data[2], retriever(second_record))
        self.assertEqual(data[3], retriever(third_record))

    def test_action_log_iterator(self):
        first_action = self.create_action(
            patient=self.first_patient,
            encounter=self.first_patient_encounter,
            in_er=True,
            timestamp=self.next_incremented_time,
        )
        second_action = self.create_action(
            action=ActionNames.SUBMIT,
            section_uid=[*self.first_patient_encounter.sections_dictionary][0],
            patient=self.first_patient,
            encounter=self.first_patient_encounter,
            in_er=False,
            timestamp=self.next_incremented_time,
        )
        third_action = self.create_action(
            action=ActionNames.ARRIVE,
            section_uid=[*self.second_patient_encounter.sections_dictionary][-1],
            patient=self.second_patient,
            encounter=self.second_patient_encounter,
            in_er=True,
            timestamp=self.next_incremented_time,
        )

        fourth_action = self.create_action(
            action=ActionNames.SKIP_WTE,
            patient=self.first_patient,
            encounter=self.first_patient_encounter,
            in_er=True,
            timestamp=self.next_incremented_time,
        )

        data = [*self.exporter.action_log_iterator]
        self.assertEqual(len(data[0]), 7)

        retriever = self.action_retriever()
        self.assertEqual(
            data[0],
            [
                "Analytics Token",
                "MRN",
                "In ER",
                "Action",
                "Screen",
                "Timestamp",
                "Client Timestamp",
            ],
        )

        self.assertEqual(data[1], retriever(first_action))
        self.assertEqual(data[2], retriever(second_action))
        self.assertEqual(data[3], retriever(third_action))
        self.assertEqual(data[4], retriever(fourth_action))

    #def test_cams_iterator(self):
    #    # NOTE: If we add more assessments per patient, etc. don't
    #    # forget about the automatic Assessment creation upon
    #    # Patient creation.
    #    first_encounter = self.first_patient.current_encounter
    #    first_encounter.save_answers({
    #        "rate_psych": 3,
    #        "length_suicidal_thought": "5"
    #    })

    #    second_encounter = self.second_patient.current_encounter
    #    second_encounter.save_answers({
    #        "current_yes_no": False,
    #        "plan_yes_no": False,
    #        "plan_yes_no": 1,
    #        "means_yes_no": False,
    #        "crisis_desc": "Some description"
    #    })

    #    data = [*self.exporter.assessment_iterator]
    #    self.assertEqual(len(data), 4)
    #    self.maxDiff = None
    #    field_names = extract_answer_keys_from_json(first_encounter.get_questions()) + first_encounter.get_metadata().keys
    #    print(field_names)
    #    retriever = self.datetime_handling_retriever(
    #         "patient.analytics_token", "patient.mrn", "department.name", "start_time", *field_names
    #    )
    #    self.assertEqual(data[0], ["Analytics Token", "MRN", "Department", "Encounter Start Time", *field_names])
    #    assert (
    #        self.first_patient.id < self.second_patient.id
    #    ), "If this ever fails, we should rewrite the test and not rely on this assumption."

    #    sorted_rows = sorted(data[1:], key=lambda row: row[0])
    #    self.assertEqual(sorted_rows[0], tuple(retriever(first_encounter)))
    #    self.assertEqual(sorted_rows[1], tuple(retriever(second_encounter)))

    def test_skills_iterator(self):
        first_patient_activity = self.create_patient_activity(
            patient=self.first_patient,
            save_for_later=False,
        )
        second_patient_activity = self.create_patient_activity(
            patient=self.second_patient,
            viewed=timezone.now(),
            save_for_later=True,
            rating=3,
        )
        third_patient_activity = self.create_patient_activity(
            patient=self.second_patient,
        )

        data = [*self.exporter.skills_iterator]
        self.assertEqual(len(data[0]), 7)
        retriever = self.datetime_handling_retriever(
            "patient.analytics_token",
            "patient.mrn",
            "activity.name",
            "modified",
            "save_for_later",
            "rating",
            "viewed",
        )
        self.assertEqual(
            data[0],
            [
                "Analytics Token",
                "MRN",
                "Activity Title",
                "Modified",
                "Saved",
                "Rating",
                "Viewed",
            ],
        )
        expected_set = set(map(tuple, data[1:]))
        given_set = set(
            map(
                tuple,
                map(
                    retriever,
                    (
                        first_patient_activity,
                        second_patient_activity,
                        third_patient_activity,
                    ),
                ),
            )
        )
        assert expected_set == given_set

    def test_videos_iterator(self):
        first_patient_video = self.create_patient_video(
            patient=self.first_patient, save_for_later=False
        )
        second_patient_video = self.create_patient_video(
            patient=self.second_patient,
            viewed=timezone.now(),
            save_for_later=True,
            rating=3,
        )
        third_patient_video = self.create_patient_video(patient=self.second_patient)

        data = [*self.exporter.videos_iterator]
        self.assertEqual(len(data), 4)
        retriever = self.datetime_handling_retriever(
            "patient.analytics_token",
            "patient.mrn",
            "video.name",
            "modified",
            "save_for_later",
            "rating",
            "viewed",
        )
        self.assertEqual(
            data[0],
            [
                "Analytics Token",
                "MRN",
                "Video Title",
                "Modified",
                "Saved",
                "Rating",
                "Viewed",
            ],
        )
        expected_set = set(map(tuple, data[1:]))
        given_set = set(
            map(
                tuple,
                map(
                    retriever,
                    (
                        first_patient_video,
                        second_patient_video,
                        third_patient_video,
                    ),
                ),
            )
        )
        assert expected_set == given_set
