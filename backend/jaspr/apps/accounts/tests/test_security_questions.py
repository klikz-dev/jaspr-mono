from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestSecurityQuestionOperation(JasprTestCase):
    def setUp(self):

        self.user = self.create_user()
        self.patient = self.create_patient()
        self.patient.save()

        super(TestSecurityQuestionOperation, self).setUp()

    # Post/Get
    def test_create_security_questions(self):
        """Can a user create security questions?"""
        secq = "Who is your least favorite presidential candidate?"
        seca = "Daffy Duck"
        encounter = self.create_patient_encounter(
            patient=self.patient, encrypted_question=secq, encrypted_answer=seca
        )
        encounter.save()

        self.assertEqual(encounter.encrypted_question, secq)
        self.assertEqual(encounter.encrypted_answer, seca)
