import axios from 'axios';
import Sentry from 'lib/sentry';
import Segment from 'lib/segment';
import config from '../../config';
import { PostResponse } from 'state/types/api/patient/action';

interface BodyType {
    clientTimestamp: string;
    action: string;
    screen?: string;
    extra?: string;
    sectionUid?: string;
}

interface ExtraActionData {
    screen?: string;
    extra?: string;
    sectionUid?: string;
}

class InOrderAction {
    clientTimestamp: Date;
    name: string;
    screen?: string;
    extra?: string;
    sectionUid?: string;
    manager: ActionManager;
    posted: boolean;
    nextAction: InOrderAction | null;

    // Prepare the `InOrderAction` for being sent to the server.
    constructor(
        name: string,
        manager: ActionManager,
        screen?: string,
        extra?: string,
        sectionUid?: string,
    ) {
        this.clientTimestamp = new Date();
        this.name = name;
        this.screen = screen;
        this.extra = extra;
        this.sectionUid = sectionUid;
        this.posted = false;
        this.manager = manager;
        this.nextAction = null;
    }

    // Send the `InOrderAction` to the server.
    async send(): Promise<void> {
        const body: BodyType = {
            clientTimestamp: this.clientTimestamp.toISOString(),
            action: this.name,
        };
        if (this.screen) {
            body.screen = this.screen.substring(0, 63);
        }
        if (this.extra) {
            body.extra = this.extra.substring(0, 127);
        }
        if (this.sectionUid) {
            body.sectionUid = this.sectionUid;
        }
        try {
            Segment.track(this.name, body);
            await axios.post<PostResponse>(`${config.apiRoot}/patient/action`, body);
        } catch (err) {
            console.error(err);
            Sentry.captureException(err);
        } finally {
            this.posted = true;
            if (this.nextAction) {
                this.nextAction.send();
            } else {
                // If there is no `nextAction`, we must be the latest,
                // and since we're done we can set `latest` on our
                // `ActionManager` to `null`.
                this.manager.latest = null;
            }
        }
    }
}

class ActionManager {
    latest: InOrderAction | null;
    constructor() {
        this.latest = null;
    }

    async add(actionName: string, screen?: string, extra?: string, sectionUid?: string) {
        const action = new InOrderAction(actionName, this, screen, extra, sectionUid);
        if (this.latest === null || this.latest === undefined) {
            this.latest = action;
            this.latest.send();
        } else {
            // This part of the code relies on `InOrderAction.send()` correctly
            // setting `this.latest` to `null` if there is no following action
            // (which that part of the code currently does). If this ever gets changed,
            // be careful to check that part of the code too.
            this.latest.nextAction = action;
            this.latest = action;
        }
    }
}

const actionManager = new ActionManager();

const addAction = async (actionName: string, actionData: ExtraActionData = {}) => {
    const { screen, extra, sectionUid } = actionData;
    await actionManager.add(actionName, screen, extra, sectionUid);
};

const actionNames = {
    ARRIVE: 'Arrive', // (Arrive[section_uid])
    CARE_PLANNING_REPORT_CLOSED: 'CarePlanningReportClosed',
    CARE_PLANNING_REPORT_OPEN: 'CarePlanningReportOpen',
    EXPLORE: 'Explore',
    GUIDE: 'Guide',
    HAMBURGER_CAMS: 'HamburgerCAMS',
    HAMBURGER_CS: 'HamburgerCS',
    HAMBURGER_HOME: 'HamburgerHome',
    HAMBURGER_MY_ACCOUNT: 'HamburgerMyAccount',
    HAMBURGER_SS: 'HamburgerSS',
    HAMBURGER_TK: 'HamburgerTK',
    HAMBURGER_STABILITY_PLAN: 'HamburgerStabilityPlan',
    HAMBURGER_CONTACTS: 'HamburgerContacts',
    HAMBURGER_WALKTHROUGH: 'HamburgerWalkthrough',
    INTERVIEW_SUMMARY_CLOSED: 'InterviewSummaryClosed',
    INTERVIEW_SUMMARY_OPEN: 'InterviewSummaryOpen',
    LOCKOUT: 'Lockout',
    LOG_OUT_BY_USER: 'LogOutByUser',
    LOG_OUT_TIMEOUT: 'LogOutTimeout',
    MENU_CAMS: 'MenuCAMS',
    MENU_CS: 'MenuCS',
    MENU_HOME: 'MenuHome',
    MENU_SS: 'MenuSS',
    MENU_TK: 'MenuTK',
    SESSION_START: 'SessionStart',
    SKIP_WTE: 'SkipWTE',
    STABILITY_PLAN_CLOSED: 'StabilityPlanClosed',
    STABILITY_PLAN_OPEN: 'StabilityPlanOpen',
    SUBMIT: 'Submit', // (Submit[section_uid])
    SUMMARIES_CLOSED: 'SummariesClosed',
    SUMMARIES_OPEN: 'SummariesOpen',
    WATCH: 'Watch', // (Watch[extra=name_of_video])
    /* --- JAH Walkthrough --- */
    JAH_WALKTHROUGH_START: 'JAHWalkthroughStart',
    JAH_WALKTHROUGH_ARRIVE: 'JAHWalkthroughArrive', // (JAHWalkthroughArrive[extra=name])
    JAH_WALKTHROUGH_CLICKED_MORE_INFO: 'JAHWalkthroughClickedMoreInfo', // (JAHWalkthroughClickedMoreInfo[extra=name])
    JAH_WALKTHROUGH_ARRIVE_RECAP: 'JAHWalkthroughArriveRecap',
    JAH_WALKTHROUGH_END: 'JAHWalkthroughEnd',
    /* --- JAH Contacts --- */
    JAH_ARRIVE_CONTACTS: 'JAHArriveContacts',
    JAH_ARRIVE_PEOPLE: 'JAHArrivePeople',
    JAH_ARRIVE_CONTACT_EDIT: 'JAHArriveContactEdit',
    JAH_CONTACT_EDITED: 'JAHContactEdited',
    JAH_CONTACT_MODIFIED: 'JAHContactModified',
    JAH_CONTACT_DELETED: 'JAHContactDeleted',
    JAH_ARRIVE_SUPPORTIVE_PERSON: 'JAHArriveSupportivePerson',
    JAH_ARRIVE_CRISIS_LINE: 'JAHArriveCrisisLine',
    JAH_ARRIVE_PEOPLE_MORE: 'JAHArrivePeopleMore',
    JAH_ARRIVE_CONVO_STARTERS: 'JAHArriveConvoStarters',
    JAH_USER_COPY: 'JAHUserCopy', // JAHUserCopy[extra=order_number]
    JAH_ARRIVE_COMMON_CONCERNS: 'JAHArriveCommonConcerns',
    JAH_OPEN_CONCERN: 'JAHOpenConcern', // JAHOpenConcern[extra=order_number]
    JAH_ARRIVE_SS_SUPPORTIVE_PEOPLE: 'JAHArriveSSSupportivePeople',
    JAH_ARRIVE_SS_HOTLINES: 'JAHArriveSSHotlines',
    JAH_CALL_HOTLINE: 'JAHCallHotline',
    JAH_TEXT_HOTLINE: 'JAHTextHotline',
    JAH_CALL_SUPPORTIVE_PERSON: 'JAHCallSupportivePerson',
    JAH_TEXT_SUPPORTIVE_PERSON: 'JAHTextSupportivePerson',
};

export { actionManager, addAction, actionNames };
