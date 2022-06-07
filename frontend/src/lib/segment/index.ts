import { actionNames } from 'state/actions/analytics';

export const track = (event: string, properties?: any) => {
    if (properties) {
        window.analytics.track(event, properties);
    } else {
        window.analytics.track(event);
    }
};

export const page = (name: string, properties?: Object) => {
    if (properties) {
        window.analytics.page(name, properties);
    } else {
        window.analytics.page(name);
    }
};

export const identify = (userId: number | string, properties?: Object) => {
    if (properties) {
        window.analytics.identify(userId, properties);
    } else {
        window.analytics.identify(userId);
    }
};

export const reset = () => {
    window.analytics.reset();
};

export const AnalyticNames = {
    APP_LOADED: 'APP_LOADED',
    ASSESSMENT_QUESTION_ANSWERED: 'ASSESSMENT_QUESTION_ANSWERED',
    JAH_SIGNUP_CONSENT: 'JAH_SIGNUP_CONSENT',
    LOG_OUT_BY_USER: 'LogOutByUser',
    OPEN_HAMBURGER_MENU: 'Open hamburger menu',
    VIDEO_PLAYER_CLOSED: 'Video player closed',
    VIDEO_BUFFER_STARTED: 'Video Playback Buffer Started',
    VIDEO_BUFFER_COMPLETED: 'Video Playback Buffer Completed',
    VIDEO_PLAYBACK_STARTED: 'Video playback Started',
    VIDEO_PLAYBACK_PAUSED: 'Video Playback Paused',
    VIDEO_PLAYBACK_COMPLETED: 'Video Playback Completed',
    VIDEO_PLAYBACK_INTERRUPTED: 'Video Playback Interrupted',
    SET_DEVICE: 'set device',
    LOG_OUT_TIMEOUT: 'LogOutTimeout',
    APP_UPDATE_AVAILABLE: 'App update available',
    DEBUG: 'Debug',
    STABILITY_PLAN_EDITED_TAKEAWAY: 'stability plan edited from takeaway kit',
    SESSION_LOCKED: 'Session Locked',
    SESSION_TIMEOUT: 'Session Timeout',
    TECHNICIAN_ACTIVATED: 'technician activated',
    TECHNICIAN_SET_PASSWORD: 'technician set password',
    TECHNICIAN_FAILED_TO_ACTIVATE: 'technician failed to activate',
    TECHNICIAN_AUTHENTICATED_WITH_EPIC: 'technician authenticated with epic',
    TECHNICIAN_TRIED_TO_LEAVE_DIRTY_COMMENT: 'technician tried to leave dirty comment',
    NOTE_COPIED_TO_CLIPBOARD: 'Note copied to clipboard',
    NOTE_SENT_TO_EHR: 'technician sent note to EHR',
    NOTE_MODIFIED_COMMENT_ON_NOTE: 'Note modified comment on note',
    NOTE_ADDED_COMMENT_TO_NOTE: 'Note added comment to note',
    TECHNICIAN_SCROLLED_TO_NOTE_COMMENTS: 'technician scrolled to note comments',
    TECHNICIAN_CHANGED_ACTIVATION_METHOD: 'technician changed activation method to pin method',
    TECHNICIAN_UPDATED_PATIENT_JAH_CREDENTIALS: 'technician updated patients JAH credentials',
    TECHNICIAN_CANCELED_EDITING_PATIENT: 'technician canceled editing patient',
    TECHNICIAN_EDITED_PATIENT: 'patient-edited',
    TECHNICIAN_PRINTED_REPORT: 'technician printed report',
    TECHNICIAN_CREATED_NEW_ENCOUNTER: 'technician created new encounter',
    LOCK_ASSESSMENT: 'LOCK_ASSESSMENT',
    LOCK_ACTIVITY: 'LOCK_ACTIVITY',
    TECHNICIAN_REASSIGNED_ASSESSMENT: 'technician reassigned assessment',
    SUMMARIES_PREVIEWED: 'Summaries previewed',
    PRINT_SUMMARIES: 'print-summaries',
    TECHNICIAN_CREATED_PROVIDER_COMMENT: 'technician created provider comment',
    TECHNICIAN_SET_PATIENT_PATH: 'technician set patient path',
    TECHNICIAN_UPDATED_PATIENT_PATH: 'technician updated patient path',
    CREATE_PATIENT: 'Create Patient',
    TECHNICIAN_TRIED_TO_CREATE_DUPLICATE_PATIENT: 'technician tried to create duplicate patient',
    TECHNICIAN_OPENED_DUPLICATE_PATIENT: 'technician opened duplicate patient',
    PATIENT_CONSENTED_DURING_ONBOARDING: 'patient consented during onboarding',
    ACTIVATE_NEW_PATIENT: 'activate-new-patient',
    REACTIVATE_EXISTING_PATIENT: 'reactivate-existing-patient',
    PATIENT_ACTIVATED_BY_PIN: 'patient activated by pin',
    LOGOUT: 'logout',
    GUIDE_SELECTED: 'Guide selected',
    JAH_SETUP_STARTED: 'JAH Setup Started',
    CONNECTION_LOST: 'connection-lost',
    CONNECTION_RESTORED: 'connection-restored',
    SECURITY_IMAGE_SET: 'security image set',
    SECURITY_QUESTION_SET: 'security question set',
    TOUR_COMPLETED: 'Tour completed',
    EMAIL_UPDATED: 'Email updated',
    SESSION_RESUMED: 'Session Resumed',
    ...actionNames,
};

const Segment = {
    track,
    page,
    identify,
    reset,
};

export default Segment;
