import responses
from rest_framework import status
from jaspr.apps.clinics.models import GlobalPreferences
from jaspr.apps.kiosk.narrative_note import NarrativeNote
from jaspr.apps.kiosk.models import NoteTemplate
from jaspr.apps.test_infrastructure.testcases import JasprTestCase, JasprApiTestCase
from jaspr.apps.epic.models import NotesLog, EpicSettings, EpicDepartmentSettings, PatientEhrIdentifier
from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.kiosk.activities.activity_utils import ActivityType



class TestYesNoIfy(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        self.answers = self.encounter.get_answers()

    def test_yesnoify_displays_none_as_no_entry_symbol(self):
        """ Is QUOTED_NO_ENTRY_SYMBOL shown for None by yesnoify """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {"suicidal_yes_no": None}
        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        self.assertEqual(
            NarrativeNote.QUOTED_NO_ENTRY_SYMBOL, note.yesnoify("suicidal_yes_no")
        )

    def test_yesnoify_displays_true_yes(self):
        """ Is True displayed as "YES"? """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {"suicidal_yes_no": True}
        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        NarrativeNote.YES, note.yesnoify("suicidal_yes_no")

    def test_yesnoify_displays_false_no(self):
        """ Is True displayed as "NO"? """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {"suicidal_yes_no": False}
        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        NarrativeNote.NO, note.yesnoify("suicidal_yes_no")


class TestElevatedCoreSuicideItems(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])

    def test_elevated_core_suicide_item_no_entries(self):
        """ Are core suicide items None when all contributing fields are also None? """
        note = NarrativeNote(self.encounter)
        self.assertEqual(note.elevated_core_suicide_items(), None)

    def test_elevated_core_suicide_item_with_one_elevated(self):
        """ Can we see the core suicide items when there are no entries? """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "rate_psych": 5,
            "most_painful": "grief",
        }

        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        self.assertEqual(
            [
                (
                    "psychological pain",
                    5,
                    "grief",
                ),
            ],
            note.elevated_core_suicide_items(),
        )

    def test_elevated_core_suicide_item_ordered_correctly(self):
        """ Are elevated core suicide items ordered correctly? """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "rank_feelings": "2,1,3,4,5",
            "rate_psych": 4,
            "most_painful": "sorrow",
            "rate_stress": 5,
            "rate_agitation": 3,
        }

        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        self.assertEqual(
            [
                ("stress", 5, note.QUOTED_NO_ENTRY_SYMBOL),
                ("psychological pain", 4, "sorrow"),
            ],
            note.elevated_core_suicide_items(),
        )


class TestCoreSuicideItemsText(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])

    def test_core_suicide_items_text_no_entries(self):
        """ Are core suicide items QUOTED_NO_ENTRY_SYMBOL when there are no entries? """
        note = NarrativeNote(self.encounter)
        self.assertEqual(note.QUOTED_NO_ENTRY_SYMBOL, note.core_suicide_items_text())

    def test_core_suicide_items_text_(self):
        """ Are core suicide items an "not elevated" when there are no entries that are elevated? """

        self.encounter.save_answers({
            "rate_psych": 1,
        })
        note = NarrativeNote(self.encounter)
        self.assertEqual("not elevated", note.core_suicide_items_text())

    def test_core_suicide_items_text_with_one_elevated(self):
        """ Can we see the core suicide items when there are no entries? """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "rate_psych": 5,
        }
        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        self.assertEqual(
            "mixed with psychological pain elevated",
            note.core_suicide_items_text(),
        )

    def test_core_suicide_items_text_with_two_elevated(self):
        """ When two items are elevated do results have an `and`? """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "rate_psych": 5,
            "rate_stress": 4,
            "rate_agitation": 3,  # should be ignored
        }
        suicide_assessment.save()

        note = NarrativeNote(self.encounter)
        self.assertEqual(
            "mixed with psychological pain and stress elevated",
            note.core_suicide_items_text(),
        )

    def test_core_suicide_items_text_with_three_elevated(self):
        """ When two items are elevated do results have an `and`? """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "rate_psych": 5,
            "rate_stress": 4,
            "rate_agitation": 4,
        }
        suicide_assessment.save()

        note = NarrativeNote(self.encounter)
        self.assertEqual(
            "mixed with psychological pain, stress and agitation elevated",
            note.core_suicide_items_text(),
        )

    def test_core_suicide_items_text_all_elevated(self):
        """ When two items are elevated do results have an `and`? """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "rate_psych": 5,
            "rate_stress": 5,
            "rate_agitation": 5,
            "rate_hopeless": 5,
            "rate_self_hate": 5,
        }
        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        self.assertEqual("elevated", note.core_suicide_items_text())


class TestCoreSuicideItemsAsTable(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])

    def test_table_produces_list_of_tuples_when_data_present(self):
        """ Is a list of 6 rows produced by core_suicide_items_as_table? """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "rate_psych": 5,
        }
        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        self.assertEqual(6, len(note.core_suicide_items_as_table()))

    def test_table_produces_list_of_tuples_when_no_data_present(self):
        """ Is a list of 6 rows produced by core_suicide_items_as_table even when no data is present? """
        note = NarrativeNote(self.encounter)
        self.assertEqual(6, len(note.core_suicide_items_as_table()))


class TestSsiAssessmentNotStarted(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )


    def ssi_assessment_started_returns_false_if_not_started(self):
        """ SSI Is not started if none of the SSI answers have been answered """
        note = NarrativeNote(self.encounter)
        self.assertEqual(False, note.ssi_assessment_started())


class TestSsiAssessmentStartedBooleanAnswer(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )

    def ssi_assessment_started_returns_false_if_not_started(self):
        """ SSI Is started if one of the boolean questions in SSI has been answered """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "hospitalized_yes_no": False,
        }
        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        self.assertEqual(True, note.ssi_assessment_started())


class TestSsiAssessmentStartedIntegerAnswer(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )

    def ssi_assessment_started_returns_false_if_not_started(self):
        """ SSI Is started if one of the integer questions in SSI has been answered """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "wish_die": 0,
        }
        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        self.assertEqual(True, note.ssi_assessment_started())


class TestSsiAssessmentStartedStringAnswer(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )

    def ssi_assessment_started_returns_false_if_not_started(self):
        """ SSI Is started if one of the integer questions in SSI has been answered """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "hospitalized_yes_no_describe": "Has a value",
        }
        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        self.assertEqual(True, note.ssi_assessment_started())


class TestSsiAssessmentStartedArrayAnswer(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )

    def ssi_assessment_started_returns_false_if_not_started(self):
        """ SSI Is started if one of the array questions in SSI has been answered """

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.answers = {
            "strategies_custom": ["Has a value"],
        }
        suicide_assessment.save()
        note = NarrativeNote(self.encounter)
        self.assertEqual(True, note.ssi_assessment_started())


class TestItemHighlighting(JasprTestCase):
    fixtures = [
        "jaspr/apps/bootstrap/fixtures/jaspr_media.json",
        "jaspr/apps/bootstrap/fixtures/jaspr_content.json"
    ]
    def setUp(self):
        super().setUp()

        stability_plan_template = NoteTemplate.objects.get(name="Default Stability Plan")
        narrative_note_template = NoteTemplate.objects.get(name="Default Narrative Note")
        GlobalPreferences.objects.update_or_create(
            pk="global_preferences",
            stability_plan_template=stability_plan_template,
            narrative_note_template=narrative_note_template,
            timezone="America/New_York",
            provider_notes=False,
            consent_language = ""
        )

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])

    def test_highlight_top_item(self):
        '''
        Items in top list should be marked with asterisks, custom items should be in qutoes.  Custom items in the top
        list should not be marked twice.
        '''

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)

        stability_plan.coping_senses = ["Be in nature","Enjoy a hot drink","Light a candle","Custom sense 1", "Custom sense 2"]
        stability_plan.coping_top = ["Enjoy a hot drink", "Custom sense 1"]
        stability_plan.save()
        note = NarrativeNote(self.encounter)

        comma_value = note.separate_with_commas('coping_senses', top_key='coping_top')
        newline_value = note.separate_with_newlines('coping_senses', top_key='coping_top')
        self.assertEqual(
            comma_value,
            "Be in nature, *Enjoy a hot drink*, Light a candle, \"Custom sense 1\", \"Custom sense 2\""
        )
        self.assertEqual(
            newline_value,
            '+ Be in nature\n+ *Enjoy a hot drink*\n+ Light a candle\n+ \"Custom sense 1\"\n+ \"Custom sense 2\"'
        )

    def test_items_should_not_error_when_output_when_top_is_none(self):

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)

        stability_plan.coping_senses = ["Be in nature","Enjoy a hot drink","Light a candle","Custom sense 1", "Custom sense 2"]
        stability_plan.coping_top = None
        stability_plan.save()
        note = NarrativeNote(self.encounter)

        comma_value = note.separate_with_commas('coping_senses', top_key='coping_top')
        newline_value = note.separate_with_newlines('coping_senses', top_key='coping_top')
        self.assertEqual(
            comma_value,
            "Be in nature, Enjoy a hot drink, Light a candle, \"Custom sense 1\", \"Custom sense 2\""
        )
        self.assertEqual(
            newline_value,
            '+ Be in nature\n+ Enjoy a hot drink\n+ Light a candle\n+ \"Custom sense 1\"\n+ \"Custom sense 2\"'
        )

    def test_values_separated_with_newlines(self):

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)

        stability_plan.reasons_live = ["Live", "Laugh", "Love"]
        stability_plan.save()
        note = NarrativeNote(self.encounter)
        numberline = note.separate_with_numberlines("reasons_live", no_entry=note.NO_ENTRY_SYMBOL)
        self.assertEqual(numberline, "1. Live\n2. Laugh\n3. Love")




class TestAutomaticNoteTriggers(JasprApiTestCase):
    fixtures = [
        "jaspr/apps/bootstrap/fixtures/jaspr_content.json",
    ]

    def setUp(self):
        super().setUp()

        self.department = self.create_department(
            name="Epic Dept 1"
        )
        epic_settings = EpicSettings.objects.create(name="Epic System", provider="Epic",
                                                         iss_url="https://fakeprovider.com")
        EpicDepartmentSettings.objects.create(
            epic_settings=epic_settings,
            department=self.department,
            location_code="valid_location",
        )

        self.technician = self.create_technician(system=self.department.clinic.system)
        self.create_department_technician(technician=self.technician, department=self.department)

        stability_plan_template = NoteTemplate.objects.get(name="Default Stability Plan")
        narrative_note_template = NoteTemplate.objects.get(name="Default Narrative Note")

        self.patient = self.create_patient()
        self.create_patient_department_sharing(patient=self.patient, department=self.department)
        self.encounter = self.create_patient_encounter(patient=self.patient, department=self.department)

        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        PatientEhrIdentifier.objects.create(
            patient=self.patient,
            fhir_id="fhir123",
            epic_settings=epic_settings,
        )
        self.encounter.fhir_id = "fhirenc123"
        self.encounter.save()
        technician = self.create_technician(system=self.department.clinic.system)
        self.create_department_technician(technician=technician, department=self.department)

        GlobalPreferences.objects.update_or_create(
            pk="global_preferences",
            stability_plan_template=stability_plan_template,
            narrative_note_template=narrative_note_template,
            timezone="America/New_York",
            provider_notes=False,
            consent_language = ""
        )

    @responses.activate
    def test_arrive_section_end(self):
        responses.add(responses.GET, 'https://fakeprovider.com/metadata',
                      json=self.epic_iss_metadata, status=status.HTTP_200_OK)
        responses.add(responses.POST, self.epic_token_url,
                      json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
        responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
                      json={}, headers={"location": "sample/docfhir"}, status=status.HTTP_201_CREATED)

        self.set_patient_creds(self.patient, encounter=self.encounter)
        self.client.post(
            "/v1/patient/action",
            data={"action": ActionNames.ARRIVE, "section_uid": "start"},
        )
        self.assertEqual(NotesLog.objects.count(), 0, "Sending non trigger analytics does not create note")
        self.client.post(
            "/v1/patient/action",
            data={"action": ActionNames.ARRIVE, "section_uid": "talk_it_through"},
        )
        self.client.post(
            "/v1/patient/action",
            data={"action": ActionNames.ARRIVE, "section_uid": "thanks_plan_to_cope"},
        )
        self.assertEqual(NotesLog.objects.filter(
            trigger="SSI Finish",
            sent_to_ehr=True,
        ).count(), 1)

        self.assertEqual(NotesLog.objects.filter(
            trigger="CSP Finish",
            sent_to_ehr=True,
        ).count(), 1)

    # @responses.activate
    # def test_technician_locks_assessment(self):
    #     responses.add(responses.GET, 'https://fakeprovider.com/metadata',
    #                   json=self.epic_iss_metadata, status=status.HTTP_200_OK)
    #     responses.add(responses.POST, self.epic_token_url,
    #                   json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
    #     responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
    #                   json={}, headers={"location": "sample/docfhir"}, status=status.HTTP_201_CREATED)
    #
    #     self.set_technician_creds(self.technician)
    #     self.client.patch(
    #         f"/v1/technician/encounter/{self.encounter.pk}",
    #         data={"assessment_lock": True},
    #     )
    #
    #     self.assertEqual(NotesLog.objects.filter(
    #         trigger="Assessment Locked",
    #         sent_to_ehr=True,
    #     ).count(), 2)

    # @responses.activate
    # def test_patient_locks_assessment(self):
    #     responses.add(responses.GET, 'https://fakeprovider.com/metadata',
    #                   json=self.epic_iss_metadata, status=status.HTTP_200_OK)
    #     responses.add(responses.POST, self.epic_token_url,
    #                   json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
    #     responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
    #                   json={}, headers={"location": "sample/docfhir"}, status=status.HTTP_201_CREATED)
    #
    #     self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
    #
    #     self.client.patch(
    #         "/v1/me",
    #         data={"assessment_locked": True},
    #     )
    #
    #     self.assertEqual(NotesLog.objects.filter(
    #         trigger="Assessment Locked",
    #         sent_to_ehr=True,
    #     ).count(), 2)

    @responses.activate
    def test_patient_saves_takeaway_kit(self):
        responses.add(responses.GET, 'https://fakeprovider.com/metadata',
                      json=self.epic_iss_metadata, status=status.HTTP_200_OK)
        responses.add(responses.POST, self.epic_token_url,
                      json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
        responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
                      json={}, headers={"location": "sample/docfhir"}, status=status.HTTP_201_CREATED)

        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
        self.client.patch(
            "/v1/patient/answers?takeaway=true",
            data={"most_hate": "The thing"},
        )
        self.assertEqual(NotesLog.objects.filter(
            trigger="Takeaway Edit",
            sent_to_ehr=True,
        ).count(), 2)

    @responses.activate
    def test_patient_does_not_finish_timeout(self):
        responses.add(responses.GET, 'https://fakeprovider.com/metadata',
                      json=self.epic_iss_metadata, status=status.HTTP_200_OK)
        responses.add(responses.POST, self.epic_token_url,
                      json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
        responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
                      json={}, headers={"location": "sample/docfhir"}, status=status.HTTP_201_CREATED)

        # TODO

    # @responses.activate
    # def test_duplicate_notes_note_saved(self):
    #     responses.add(responses.GET, 'https://fakeprovider.com/metadata',
    #                   json=self.epic_iss_metadata, status=status.HTTP_200_OK)
    #     responses.add(responses.POST, self.epic_token_url,
    #                   json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
    #     responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
    #                   json={}, headers={"location": "sample/docfhir"}, status=status.HTTP_201_CREATED)
    #
    #     self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)
    #     self.client.patch(
    #         "/v1/patient/answers?takeaway=true",
    #         data={"most_hate": "The thing"},
    #     )
    #     self.client.patch(
    #         "/v1/patient/answers?takeaway=true",
    #         data={"most_hate": "The thing"},
    #     )
    #     self.assertEqual(NotesLog.objects.filter(
    #         patient_session=self.patient_session,
    #         trigger="Takeaway Edit",
    #         sent_to_ehr=True,
    #     ).count(), 2)
    #
    #     self.client.patch(
    #         "/v1/patient/answers?takeaway=true",
    #         data={"suicide_risk": 5},
    #     )
    #     self.assertEqual(NotesLog.objects.filter(
    #         patient_session=self.patient_session,
    #         trigger="Takeaway Edit",
    #         sent_to_ehr=True,
    #     ).count(), 3)