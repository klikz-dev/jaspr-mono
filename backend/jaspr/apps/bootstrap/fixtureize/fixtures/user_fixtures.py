from jaspr.apps.accounts.models import User
from jaspr.apps.clinics.models import (
    Clinic,
    Department,
    DepartmentTechnician,
    HealthcareSystem,
    Preferences,
    GlobalPreferences,
)
from jaspr.apps.epic.models import EpicSettings, EpicDepartmentSettings, PatientEhrIdentifier
from jaspr.apps.kiosk.models import (
    Action,
    ActivateRecord,
    AssignedActivity,
    Amendment,
    ComfortAndSkills,
    CrisisStabilityPlan,
    CustomOnboardingQuestions,
    Encounter,
    LethalMeans,
    Patient,
    PatientActivity,
    PatientCopingStrategy,
    PatientDepartmentSharing,
    PatientMeasurements,
    PatientVideo,
    Technician,
    Srat,
    Outro,
)
from jaspr.apps.jah.models import (
    JAHAccount,
    CrisisStabilityPlan as JAHCrisisStabilityPlan,
    PatientCopingStrategy as JAHPatientCopingStrategy
)
from jaspr.apps.stability_plan.models import PatientWalkthrough, PatientWalkthroughStep

from ..base import AppFixture, ModelFixture
from ..tags import Tags


class UserFixture(ModelFixture):
    model = User
    tags = {Tags.USER}

class GlobalPreferencesFixture(ModelFixture):
    model = GlobalPreferences
    tags = {Tags.USER}


class PreferencesFixture(ModelFixture):
    model = Preferences
    tags = {Tags.USER}


class HealthcareSystemFixture(ModelFixture):
    model = HealthcareSystem
    tags = {Tags.USER}


class ClinicFixture(ModelFixture):
    model = Clinic
    tags = {Tags.USER}


class DepartmentFixture(ModelFixture):
    model = Department
    tags = {Tags.USER}


class DepartmentTechnicianFixture(ModelFixture):
    model = DepartmentTechnician
    tags = {Tags.USER}


class EpicSettingsFixture(ModelFixture):
    model = EpicSettings
    tags = {Tags.USER}

class EpicDepartmentSettingsFixture(ModelFixture):
    model = EpicDepartmentSettings
    tags = {Tags.USER}

class PatientEhrIdentifierFixture(ModelFixture):
    model = PatientEhrIdentifier
    tags = {Tags.USER}

class ActionFixture(ModelFixture):
    model = Action
    tags = {Tags.USER}


class ActivateRecordFixture(ModelFixture):
    model = ActivateRecord
    tags = {Tags.USER}


class AmendmentFixture(ModelFixture):
    model = Amendment
    tags = {Tags.USER}


class CrisisStabilityPlanFixture(ModelFixture):
    model = CrisisStabilityPlan
    tags = {Tags.USER}


class JAHCrisisStabilityPlanFixture(ModelFixture):
    model = JAHCrisisStabilityPlan
    tags = {Tags.USER}


class EncounterFixture(ModelFixture):
    model = Encounter
    tags = {Tags.USER}

class AssignedActivityFixture(ModelFixture):
    model = AssignedActivity
    tags = {Tags.USER}

class ComfortAndSkillsFixture(ModelFixture):
    model = ComfortAndSkills
    tags = {Tags.USER}

class LethalMeansFixture(ModelFixture):
    model = LethalMeans
    tags = {Tags.USER}


class CustomOnboardingQuestions(ModelFixture): # Intro questions
    model = CustomOnboardingQuestions
    tags = {Tags.USER}


class PatientFixture(ModelFixture):
    model = Patient
    tags = {Tags.USER}


class PatientActivityFixture(ModelFixture):
    model = PatientActivity
    tags = {Tags.USER}


class PatientCopingStrategyFixture(ModelFixture):
    model = PatientCopingStrategy
    tags = {Tags.USER}


class JAHPatientCopingStrategyFixture(ModelFixture):
    model = JAHPatientCopingStrategy
    tags = {Tags.USER}


class PatientDepartmentSharingFixture(ModelFixture):
    model = PatientDepartmentSharing
    tags = {Tags.USER}


class PatientMeasurementsFixture(ModelFixture):
    model = PatientMeasurements
    tags = {Tags.USER}



class PatientVideoFixture(ModelFixture):
    model = PatientVideo
    tags = {Tags.USER}


class TechnicianFixture(ModelFixture):
    model = Technician
    tags = {Tags.USER}


class PatientWalkthroughFixture(ModelFixture):
    model = PatientWalkthrough
    tags = {Tags.USER}


class PatientWalkthroughStepFixture(ModelFixture):
    model = PatientWalkthroughStep
    tags = {Tags.USER}


class SratFixture(ModelFixture):
    model = Srat
    tags = {Tags.USER}


class OutroFixture(ModelFixture):
    model = Outro
    tags = {Tags.USER}


class JAHAccountFixture(ModelFixture):
    model = JAHAccount
    tags = {Tags.USER}


class OTPStaticFixture(AppFixture):
    app_label = "otp_static"
    tags = {Tags.USER, Tags.THIRD_PARTY}
