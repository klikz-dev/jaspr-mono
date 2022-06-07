from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestSections(JasprTestCase):
    def test_get_section_uid_for_answer_key(self):
        system, clinic, department = self.create_full_healthcare_system()

        patient = self.create_patient()

        encounter = self.create_patient_encounter(
            patient=patient, department=department
        )
        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])

        answer_key_to_correct_section_uid = {
            "time_here": "welcome",
            "distress0": "rate_distress",
            "frustration0": "rate_frustration",
            "rate_psych": "rate_psych",
            "most_painful": "rate_psych_text",
            "rate_stress": "rate_stress",
            "most_stress": "rate_stress_text",
            "suicidal_others": "suicidal_about_others",
            "reasons_live": "reasons_live_die",
            "reasons_die": "reasons_live_die",
            "wish_live": "wish_live",
            "wish_die": "wish_die",
            "one_thing": "one_thing",
            "suicidal_yes_no": "suicidal_describe",
            "suicidal_yes_no_describe": "suicidal_describe",
            # Test if we handled questions split by pipes correctly (at the time of
            # writing).
            "suicidal_freq": "suicidal_freq",
            "suicidal_freq_units": "suicidal_freq",
            "length_suicidal_thought": "suicidal_length",
            "plan_yes_no": "plans_describe",
            "plan_yes_no_describe": "plans_describe",
            "shame_yes_no": "shame_describe",
            "shame_yes_no_describe": "shame_describe",
            "skip_lethal_means": "skip_lethal_means",
            "skip_reason": "skip_reason",
            "too_private_dec": "reason_too_private",
            "overreact_specific": "reason_people_will_overreact",
            "overreact_take_away_dec": "reason_people_will_overreact_take_away_means",
            "overreact_keep_me_dec": "reason_people_will_overreact_keep_against_will",
            "reason_not_sure_talk": "reason_dont_want_to_talk",
            "not_sure_talk_dec": "reason_dont_want_to_talk_all",
            "too_shameful_dec": "lethal_means_too_shameful",
            "do_not_need_dec": "lethal_means_dont_need",
            "cannot_rid_means_dec": "lethal_means_get_rid",
            "stable_dec": "lethal_means_not_stable",
            "keep_means_dec": "lethal_means_want_to_keep",
            "keep_in_hospital_dec": "lethal_means_afraid_hospital",
            "feel_depressed_dec": "lethal_means_too_depressed",
            # note: that these fields show up twice,
            # by convention we take the first appearance.
            "means_yes_no": "means_describe",
            "means_yes_no_describe": "means_describe",
            # /note: end
            "strategies_general": "strategies_general",
            "strategies_firearm": "additional_strategies",
            "strategies_medicine": "additional_strategies",
            "strategies_places": "additional_strategies",
            "strategies_other": "additional_strategies",
            "strategies_custom": "means_custom",
            "means_support_yes_no": "means_support",
            "means_support_who": "means_support",
            "means_willing": "means_willing",
            "crisis_desc": "crisis_desc",
            "coping_body": "coping_body",
            "coping_senses": "coping_senses",
            "supportive_people": "supportive_people",
            "coping_top": "coping_top",
            "ws_stressors": "warning_stressors",
            "ws_actions": "warning_actions",
            "ws_top": "ws_top",
            "stability_rehearsal": "stability_rehearsal",
            "stability_confidence": "stability_confidence",
            "readiness": "readiness",
            "readiness_no": "readiness_no",
            "readiness_yes_reasons": "readiness_yes_reasons",
            "readiness_yes_changed": "readiness_yes_changed",
            "walk_through": "walk_through",
            "something_that_is_definitely_not_present": None,
        }

        for answer_key, correct_uid in answer_key_to_correct_section_uid.items():
            with self.subTest(answer_key=answer_key):
                section_uid = encounter.get_section_uid_for_answer_key(answer_key)
                self.assertEqual(section_uid, correct_uid)
