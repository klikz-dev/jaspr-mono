class ActionNames:
    ARRIVE = "Arrive"  # (Arrive[section_uid])
    CARE_PLANNING_REPORT_CLOSED = "CarePlanningReportClosed"
    CARE_PLANNING_REPORT_OPEN = "CarePlanningReportOpen"
    EXPLORE = "Explore"
    GUIDE = "Guide"
    GUIDE_JASPER = "GuideJasper"
    GUIDE_JAZ = "GuideJaz"
    HAMBURGER_CAMS = "HamburgerCAMS"
    HAMBURGER_CS = "HamburgerCS"
    HAMBURGER_HOME = "HamburgerHome"
    HAMBURGER_MY_ACCOUNT = "HamburgerMyAccount"
    HAMBURGER_SS = "HamburgerSS"
    HAMBURGER_TK = "HamburgerTK"
    HAMBURGER_STABILITY_PLAN = "HamburgerStabilityPlan"
    HAMBURGER_CONTACTS = "HamburgerContacts"
    HAMBURGER_WALKTHROUGH = "HamburgerWalkthrough"
    HAMBURGER_SUPPORT = "HamburgerSupport"
    INTERVIEW_SUMMARY_CLOSED = "InterviewSummaryClosed"
    INTERVIEW_SUMMARY_OPEN = "InterviewSummaryOpen"
    LOCKOUT = "Lockout"
    LOG_OUT_BY_USER = "LogOutByUser"
    LOG_OUT_TIMEOUT = "LogOutTimeout"
    MENU_CAMS = "MenuCAMS"
    MENU_CS = "MenuCS"
    MENU_HOME = "MenuHome"
    MENU_SS = "MenuSS"
    MENU_TK = "MenuTK"
    SESSION_START = "SessionStart"
    SKIP_WTE = "SkipWTE"
    STABILITY_PLAN_CLOSED = "StabilityPlanClosed"
    STABILITY_PLAN_OPEN = "StabilityPlanOpen"
    SUBMIT = "Submit"  # (Submit[section_uid])
    SUMMARIES_CLOSED = "SummariesClosed"
    SUMMARIES_OPEN = "SummariesOpen"
    WATCH = "Watch"  # (Watch[extra=name_of_video])
    # --- JAH Walkthrough --- #
    JAH_WALKTHROUGH_START = "JAHWalkthroughStart"
    JAH_WALKTHROUGH_ARRIVE = (
        "JAHWalkthroughArrive"  # (JAHWalkthroughArrive[extra=name])
    )
    JAH_WALKTHROUGH_CLICKED_MORE_INFO = (
        "JAHWalkthroughClickedMoreInfo"  # (JAHWalkthroughClickedMoreInfo[extra=name])
    )
    JAH_WALKTHROUGH_ARRIVE_RECAP = "JAHWalkthroughArriveRecap"
    JAH_WALKTHROUGH_END = "JAHWalkthroughEnd"
    # --- JAH Contacts --- #
    JAH_ARRIVE_CONTACTS = "JAHArriveContacts"
    JAH_ARRIVE_PEOPLE = "JAHArrivePeople"
    JAH_ARRIVE_SUPPORTIVE_PERSON = "JAHArriveSupportivePerson"
    JAH_ARRIVE_CONTACT_EDIT = "JAHArriveContactEdit"
    JAH_CONTACT_EDITED = "JAHContactEdited"
    JAH_CONTACT_MODIFIED = "JAHContactModified"
    JAH_CONTACT_DELETED = "JAHContactDeleted"
    JAH_ARRIVE_CRISIS_LINE = "JAHArriveCrisisLine"
    JAH_ARRIVE_PEOPLE_MORE = "JAHArrivePeopleMore"
    JAH_ARRIVE_CONVO_STARTERS = "JAHArriveConvoStarters"
    JAH_USER_COPY = "JAHUserCopy"  # JAHUserCopy[extra=order_number]
    JAH_ARRIVE_COMMON_CONCERNS = "JAHArriveCommonConcerns"
    JAH_OPEN_CONCERN = "JAHOpenConcern"  # JAHOpenConcern[extra=order_number]
    JAH_ARRIVE_SS_SUPPORTIVE_PEOPLE = "JAHArriveSSSupportivePeople"
    JAH_ARRIVE_SS_HOTLINES = "JAHArriveSSHotlines"
    JAH_CALL_HOTLINE = "JAHCallHotline"
    JAH_TEXT_HOTLINE = "JAHTextHotline"
    JAH_CALL_SUPPORTIVE_PERSON = "JAHCallSupportivePerson"  # JAHCallSupportivePerson[extra=name_of_supportive_person]
    JAH_TEXT_SUPPORTIVE_PERSON = "JAHTextSupportivePerson"  # JAHTextSupportivePerson[extra=name_of_supportive_person]


COPING_STRATEGY_CATEGORY_SLUG_MAP = {
    "coping_body": "physical",
    "coping_distract": "distract",
    "coping_help_others": "help",
    "coping_courage": "courage",
    "coping_senses": "senses",
}
