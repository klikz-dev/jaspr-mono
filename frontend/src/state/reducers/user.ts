import Storage from 'lib/storage';
import { UserConstants } from 'state/constants';
import {
    AnonymousUser,
    Departments,
    Patient,
    Technician,
    PrivacyImages,
    SecurityQuestion,
} from 'state/types';
import {
    ActionSetToken,
    ActionSetGuide,
    ActionSetMe,
    ActionUpdateMe,
    ActionSetPreferences,
    ActionFetchLocations,
    ActionActivatePatient,
    ActionSetPrivacyImages,
    ActionHeartbeat,
    ActionSetTimeSinceCheckin,
    ActionSetSecurityQuestion,
    ActionLockSession,
    ActionValidateSession,
    ActionSetSecurityImage,
    ActionSaveSecurityQuestion,
    ActionCompleteTour,
    ActionCompleteJahOnboarding,
    ActionToggleOnline,
    ActionUpdateEmail,
    ActionSetupToolsToGo,
    ActionSetAssessmentLockTimer,
} from 'state/types/actions';

type UserReducerType =
    | ActionSetToken
    | ActionSetGuide
    | ActionSetMe
    | ActionUpdateMe
    | ActionSetPreferences
    | ActionFetchLocations
    | ActionActivatePatient
    | ActionSetPrivacyImages
    | ActionHeartbeat
    | ActionSetTimeSinceCheckin
    | ActionSetSecurityQuestion
    | ActionLockSession
    | ActionValidateSession
    | ActionSetSecurityImage
    | ActionSaveSecurityQuestion
    | ActionCompleteTour
    | ActionCompleteJahOnboarding
    | ActionToggleOnline
    | ActionUpdateEmail
    | ActionSetupToolsToGo
    | ActionSetAssessmentLockTimer;

export type UserReducerState = {
    online?: boolean;
} & (
    | (Patient & {
          authenticated: true;
          token: string;
          privacyImages?: PrivacyImages;
          sessionLocked?: boolean;
          resetPassword?: boolean;
          lastHeartbeat?: Date;
          securityQuestion?: SecurityQuestion;
          timeSinceCheckin?: number;
          assessmentLockTimer?: number;
          activities?: { csp: boolean; csa: boolean; skills: boolean };
          technicianOperated?: boolean;
      })
    | ({
          authenticated: true;
          token: string;
          analyticsToken: string;
          lastHeartbeat?: Date;
          locations?: Departments;
      } & Technician)
    | AnonymousUser
    | (AnonymousUser & { token: string; authenticated: true })
);

const initialState: UserReducerState = {
    authenticated: false,
    userType: '',
    online: window.navigator.onLine,
};

const UserReducer = (
    state: UserReducerState = initialState,
    action: UserReducerType,
): UserReducerState => {
    switch (action.type) {
        case UserConstants.SET_TOKEN:
            if (action.token) {
                Storage.setSecureItem('token', action.token);
                // @ts-ignore TODO FIXME
                return {
                    ...state,
                    token: action.token,
                    authenticated: true,
                };
            }
            return initialState;

        case UserConstants.SET_GUIDE:
            if (state.authenticated && state.userType === 'patient') {
                return { ...state, guide: action.guide };
            }
            return state;
        case UserConstants.SET_ME:
            if (state.authenticated && action.userType === 'patient') {
                return {
                    ...state,
                    id: action.id,
                    authenticated: true,
                    analyticsToken: action.analyticsToken,
                    token: state.token,
                    currentWalkthroughStep: action.currentWalkthroughStep,
                    currentWalkthroughStepChanged: action.currentWalkthroughStepChanged,
                    dateOfBirth: action.dateOfBirth,
                    email: action.email,
                    location: action.location,
                    firstName: action.firstName,
                    guide: action.guide || 'Jaz',
                    hasSecuritySteps: action.hasSecuritySteps,
                    inEr: action.inEr,
                    lastName: action.lastName,
                    mobilePhone: action.mobilePhone,
                    mrn: action.mrn,
                    onboarded: action.onboarded,
                    ssid: action.ssid,
                    toolsToGoStatus: action.toolsToGoStatus,
                    tourComplete: action.technicianOperated || action.tourComplete,
                    userType: 'patient',
                    activities: action.activities,
                    technicianOperated: action.technicianOperated || false,
                };
            } else if (state.authenticated && action.userType === 'technician') {
                return {
                    authenticated: true,
                    analyticsToken: action.analyticsToken,
                    department: action.department,
                    token: state.token,
                    id: action.id,
                    role: action.role,
                    userType: action.userType,
                    firstName: action.firstName,
                    lastName: action.lastName,
                    email: action.email,
                    location: action.location,
                    online: window.navigator.onLine,
                    supportUrl: action.supportUrl,
                };
            }

            return initialState;
        case UserConstants.UPDATE_ME:
            if (
                state.authenticated &&
                state.userType === 'patient' &&
                action.userType === 'patient'
            ) {
                return {
                    ...state,
                    id: action.id,
                    authenticated: action.authenticated || state.authenticated,
                    analyticsToken: action.analyticsToken || state.analyticsToken,
                    token: action.token || state.token,
                    currentWalkthroughStep:
                        action.currentWalkthroughStep || state.currentWalkthroughStep,
                    currentWalkthroughStepChanged:
                        action.currentWalkthroughStepChanged || state.currentWalkthroughStepChanged,
                    dateOfBirth: action.dateOfBirth || state.dateOfBirth,
                    email: action.email || state.email,
                    location: action.location || state.location,
                    firstName: action.firstName || state.firstName,
                    guide: action.guide || state.guide || 'Jaz',
                    hasSecuritySteps: action.hasSecuritySteps || state.hasSecuritySteps,
                    inEr: action.inEr || state.inEr,
                    lastName: action.lastName || state.lastName,
                    mobilePhone: action.mobilePhone || state.mobilePhone,
                    mrn: action.mrn || state.mrn,
                    onboarded: action.onboarded || state.onboarded,
                    ssid: action.ssid || state.ssid,
                    toolsToGoStatus: action.toolsToGoStatus || state.toolsToGoStatus,
                    tourComplete:
                        action.technicianOperated ||
                        state.technicianOperated ||
                        action.tourComplete ||
                        state.tourComplete,
                    userType: 'patient',
                    activities: action.activities || state.activities,
                    technicianOperated: action.technicianOperated || state.technicianOperated,
                };
            } else if (
                state.authenticated &&
                state.userType === 'technician' &&
                action.userType === 'technician'
            ) {
                return {
                    ...state,
                    authenticated: state.authenticated,
                    analyticsToken: state.analyticsToken,
                    department: action.department || state.department,
                    token: state.token,
                    id: state.id,
                    role: action.role || state.role,
                    supportUrl: action.supportUrl || state.supportUrl,
                    userType: 'technician',
                };
            } else if (state.userType === '' && action.userType === '') {
                return {
                    ...state,
                    email: action.email || state.email,
                    mobilePhone: action.mobilePhone || state.mobilePhone,
                };
            }
            return state;
        case UserConstants.SET_PREFERENCES:
            if (state.authenticated && state.userType === 'patient') {
                return {
                    ...state,
                    consentLanguage: action.consentLanguage,
                    timezone: action.timezone,
                };
            }
            return state;
        case UserConstants.FETCH_LOCATIONS:
            if (state.userType === 'technician') {
                return { ...state, locations: action.locations };
            }
            return state;
        case UserConstants.ACTIVATE_PATIENT:
            Storage.setSecureItem('token', action.token);

            return {
                ...action.patient,
                tourComplete: action.technicianOperated ? true : action.patient.tourComplete,
                technicianOperated: action.technicianOperated,
                authenticated: true,
                token: action.token,
            };

        case UserConstants.SET_PRIVACY_IMAGES:
            if (state.userType === 'patient') {
                return { ...state, privacyImages: [...action.privacyImages] };
            }
            return state;
        case UserConstants.HEARTBEAT:
            if (state.authenticated) {
                return { ...state, lastHeartbeat: new Date() };
            }
            return state;
        case UserConstants.SET_TIME_SINCE_CHECKIN:
            if (state.authenticated && state.userType === 'patient') {
                return { ...state, timeSinceCheckin: action.timeSinceCheckin };
            }
            return state;
        case UserConstants.SET_SECURITY_QUESTIONS:
            // TODO This may not need to be in the reducers, limit to the view
            if (state.userType === 'patient') {
                return { ...state, securityQuestion: action.securityQuestion };
            }
            return state;
        case UserConstants.LOCK_SESSION:
            if (state.userType === 'patient') {
                return {
                    ...state, // TODO do we need to remove any of this data?
                    sessionLocked: true,
                };
            }
            return state;
        case UserConstants.VALIDATE_SESSION:
            if (state.userType === 'patient') {
                return { ...state, sessionLocked: false };
            }
            return state;
        case UserConstants.SET_SECURITY_IMAGE:
            // TODO This reducer/action is useless.  Move to view inline?
            return { ...state };
        case UserConstants.SAVE_SECURITY_QUESTION:
            if (state.userType === 'patient') {
                return {
                    ...state,
                    resetPassword: false,
                    hasSecuritySteps:
                        state.privacyImages && state.privacyImages.length > 0 ? true : false,
                };
            }
            return state;
        case UserConstants.COMPLETE_TOUR:
            if (state.userType === 'patient') {
                return { ...state, tourComplete: true };
            }
            return state;
        case UserConstants.COMPLETE_JAH_ONBOARDING:
            if (state.userType === 'patient') {
                return { ...state, onboarded: true };
            }
            return state;
        case UserConstants.TOGGLE_ONLINE:
            return { ...state, online: action.online };
        case UserConstants.UPDATE_EMAIL:
            if (state.userType === 'patient') {
                return { ...state, email: action.email };
            }
            return state;
        case UserConstants.SETUP_TOOLS_TO_GO:
            if (state.userType === 'patient') {
                return {
                    ...state,
                    inEr: action.inEr,
                    mobilePhone: action.mobilePhone,
                    email: action.email,
                    toolsToGoStatus: action.toolsToGoStatus,
                };
            }
            return state;
        case UserConstants.SET_ASSSESSMENT_LOCK_TIMER:
            if (state.userType === 'patient') {
                return { ...state, assessmentLockTimer: action.assessmentLockTimer };
            }
            return state;
        default:
            return state;
    }
};

export { UserReducer, initialState };
