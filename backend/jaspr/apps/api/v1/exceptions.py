from jaspr.apps.kiosk.models import Patient


class AlreadyExistsError(Exception):
    pass


class PatientAlreadyExistsError(AlreadyExistsError):
    def __init__(self, patient: Patient):
        assert isinstance(patient, Patient)
        self.content_type = Patient
        self.object_id = patient.pk

        super().__init__("The information entered matches an existing patient record.")
