from django.conf import settings
from django.urls import include, re_path
from rest_framework import routers

from jaspr.apps.api.v1 import views as v1_views
from jaspr.apps.api.v1 import viewsets as v1_viewsets

if settings.DEBUG:
    v1_router = routers.DefaultRouter(trailing_slash=False)
else:
    v1_router = routers.SimpleRouter(trailing_slash=False)

# Pure content endpoints. May require `Patient` but doesn't involve any data tied to
# `Patient`.
v1_router.register("videos", v1_viewsets.JasprMediaViewSet)
v1_router.register("shared-stories", v1_viewsets.SharedStoryViewSet)
v1_router.register("common-concerns", v1_viewsets.CommonConcernViewSet)
v1_router.register("conversation-starters", v1_viewsets.ConversationStarterViewSet)
v1_router.register("coping-strategies", v1_viewsets.CopingStrategyViewSet)

# `Technician` endpoints.
v1_router.register("technician/departments", v1_viewsets.DepartmentViewSet)
v1_router.register("technician/patients", v1_viewsets.TechnicianPatientViewSet)

# `Patient` endpoints and/or endpoints with data tied into `Patient`s in some way that
# they can view and/or manage.
v1_router.register("patient/patient-videos", v1_viewsets.PatientVideoViewSet)
# NOTE: Namespaced this under "patient/" because `ActivityViewSet` also includes
# `PatientActivity` data alongside each `Activity` if present, so this endpoint is
# effectively tied to the `Patient` right now.
v1_router.register("patient/activities", v1_viewsets.ActivityViewSet)
v1_router.register("patient/patient-activities", v1_viewsets.PatientActivityViewSet)

app_name = "v1"
urlpatterns = [
    # Shared/base endpoints.
    re_path(r"^me$", v1_views.MeView.as_view()),
    re_path(
        # # !INSPECT_WHEN_UPGRADING_DJANGO!
        # The token is a sha256 hash with every other character extracted so length is 32.  Review if/when default
        # hashing mechanism changes.  Previously it was a sha1 hash with a string length of 20
        r"^reset-password/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})$",
        v1_views.ResetPasswordRedirectView.as_view(),
    ),
    re_path(r"^reset-password$", v1_views.ResetPasswordView.as_view()),
    # `Technician` endpoints.
    re_path(r"^technician/login$", v1_views.TechnicianLoginView.as_view()),
    re_path(
        r"^technician/epic-oauth-login", v1_views.TechnicianEpicOauthLoginView.as_view()
    ),
    re_path(
        r"^technician/epic/oauth",
        v1_views.TechnicianEpicOauthRedirectView.as_view(),
    ),
    re_path(
        r"^technician/epic/sync-narrative-note",
        v1_views.TechnicianEpicNoteToEhrView.as_view(),
    ),
    re_path(r"^technician/logout", v1_views.LogoutView.as_view()),
    re_path(r"^technician/encounter$", v1_views.TechnicianPatientEncounterView.as_view()),
    re_path(r"^technician/encounter/(?P<encounter_id>[0-9]+)/activities$", v1_views.TechnicianAssignedActivityView.as_view()),
    re_path(r"^technician/encounter/(?P<encounter_id>[0-9]+)/activities/(?P<activity_id>[0-9]+)$", v1_views.TechnicianAssignedActivityView.as_view()),
    re_path(r"^technician/encounter/(?P<encounter_id>[0-9]+)/provider-comments$",
        v1_viewsets.TechnicianPatientProviderCommentViewSet.as_view(
            {"get": "list", "post": "create"}
        )
    ),
    re_path(r"^technician/encounter/(?P<encounter_id>[0-9]+)/provider-comments/(?P<provider_comment_id>[0-9]+)$",
        v1_viewsets.TechnicianPatientProviderCommentViewSet.as_view(
            {"put": "update", "patch": "update", "delete": "destroy"}
        )
    ),
    re_path(
        r"^technician/encounter/(?P<encounter_id>[0-9]+)/amendments$",
        v1_viewsets.TechnicianPatientAmendmentViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
    ),
    re_path(
        r"^technician/encounter/(?P<encounter_id>[0-9]+)/amendments/(?P<amendment_id>[0-9]+)$",
        v1_viewsets.TechnicianPatientAmendmentViewSet.as_view(
            {"put": "update", "delete": "destroy"}
        ),
    ),
    re_path(
        r"^technician/preferences$", v1_views.PreferencesView.as_view(),
    ),
    re_path(
        r"^technician/heartbeat$",
        v1_views.TechnicianHeartbeatView.as_view(),
    ),
    re_path(
        r"technician/tablet-pin$",
        v1_views.TechnicianTabletPinView.as_view(),
    ),
    re_path(
        r"^technician/activate-patient$",
        v1_views.TechnicianActivatePatientView.as_view(),
    ),
    re_path(
        # !INSPECT_WHEN_UPGRADING_DJANGO!
        # The token is a sha256 hash with every other character extracted so length is 32.  Review if/when default
        # hashing mechanism changes.  Previously it was a sha1 hash with a string length of 20
        r"^technician/activate/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})$",
        v1_views.TechnicianActivateRedirectView.as_view(),
    ),
    re_path(
        r"^technician/activate$",
        v1_views.TechnicianActivateView.as_view(),
    ),
    re_path(
        r"^technician/set-password$",
        v1_views.TechnicianActivateSetPasswordView.as_view(),
    ),
    re_path(
        r"^technician/patient-data/(?P<department>[0-9]+)/(?P<patient>[1-9]+[0-9]*)$",
        v1_views.TechnicianPatientDataView.as_view(),
    ),
    re_path(
        r"^technician/reset-password/set-password$",
        v1_views.TechnicianResetPasswordSetPasswordView.as_view(),
    ),
    re_path(
        r"^technician/notes-log$",
        v1_views.TechnicianNotesLogView.as_view(),
    ),
    re_path(
        r"^technician/freshdesk$",
        v1_views.FreshdeskSSOView.as_view(),
    ),
    # `Patient` endpoints.
    re_path(r"^patient/login$", v1_views.PatientLoginView.as_view()),
    re_path(r"^patient/preferences$", v1_views.PatientPreferencesView.as_view()),
    re_path(
        r"patient/tablet-pin$",
        v1_views.PatientTabletPinView.as_view(),
    ),
    re_path(r"^patient/logout", v1_views.LogoutView.as_view()),
    re_path(r"^patient/security-questions", v1_views.PatientSecurityQuestion.as_view()),
    re_path(
        r"^patient/privacy-screen-images$",
        v1_views.PatientPrivacyScreenImagesView.as_view(),
    ),
    re_path(
        r"^patient/privacy-screen-image$",
        v1_views.PatientPrivacyScreenImageView.as_view(),
    ),
    re_path(
        r"^patient/validate-session$", v1_views.PatientValidateSessionView.as_view()
    ),
    re_path(r"^patient/heartbeat$", v1_views.PatientHeartbeatView.as_view()),
    re_path(r"^patient/session-lock$", v1_views.PatientSessionLockView.as_view()),
    re_path(r"^patient/action$", v1_views.PatientActionView.as_view()),
    re_path(
        # !INSPECT_WHEN_UPGRADING_DJANGO!
        # The token is a sha256 hash with every other character extracted so length is 32.  Review if/when default
        # hashing mechanism changes.  Previously it was a sha1 hash with a string length of 20
        r"^patient/at-home-setup/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})$",
        v1_views.PatientToolsToGoVerificationRedirectView.as_view(),
    ),
    re_path(
        r"^patient/at-home-setup$",
        v1_views.PatientToolsToGoVerificationSetupView.as_view(),
    ),
    re_path(
        r"^patient/verify-phone-number$",
        v1_views.PatientVerifyPhoneNumberView.as_view(),
    ),
    re_path(
        r"^patient/reset-password/verify-phone-number$",
        v1_views.PatientResetPasswordVerifyPhoneNumberView.as_view(),
    ),
    re_path(
        r"^patient/native-verify-phone-number$",
        v1_views.PatientNativeVerifyPhoneNumberView.as_view(),
    ),
    re_path(
        r"^patient/check-phone-number-code$",
        v1_views.PatientCheckPhoneNumberCodeView.as_view(),
    ),
    re_path(
        r"^patient/reset-password/check-phone-number-code$",
        v1_views.PatientResetPasswordCheckPhoneNumberCodeView.as_view(),
    ),
    re_path(
        r"^patient/native-check-phone-number-code$",
        v1_views.PatientNativeCheckPhoneNumberCodeView.as_view(),
    ),
    re_path(
        r"^patient/set-password$",
        v1_views.PatientSetPasswordView.as_view(),
    ),
    re_path(
        r"^patient/reset-password/set-password$",
        v1_views.PatientResetPasswordSetPasswordView.as_view(),
    ),
    re_path(
        r"^patient/change-password$",
        v1_views.PatientChangePasswordView.as_view(),
    ),
    # Deprecated URL.  Remove Q4 2021
    re_path(r"^patient/assessments$", v1_views.JahCrisisStabilityPlanView.as_view()),

    re_path(r"^patient/interview-activity/(?P<activity_id>[0-9]+)$", v1_views.PatientAssignedActivityView.as_view()),
    re_path(r"^patient/crisis-stability-plan$", v1_views.JahCrisisStabilityPlanView.as_view()),
    re_path(r"^patient/accept-privacy-policy$", v1_views.PatientPrivacyPolicyAcceptanceView.as_view()),
    re_path(r"^patient/walkthrough$", v1_views.PatientWalkthroughView.as_view()),
    re_path(r"^patient/interview$", v1_views.PatientInterviewView.as_view()),
    re_path(r"^patient/answers$", v1_views.PatientInterviewAnswersView.as_view()),
    re_path(r"^static-media$", v1_views.StaticMediaView.as_view()),
    re_path(r"", include(v1_router.urls)),
]
