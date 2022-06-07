import Storage from 'lib/storage';
import { UserConstants } from 'state/constants';
import { AnonymousUser, Patient } from 'state/types';
import {
    ActionSetToken,
    ActionSetMe,
    ActionUpdateMe,
    ActionCompleteTour,
    ActionCompleteJahOnboarding,
    ActionToggleOnline,
    ActionUpdateEmail,
} from 'state/types/actions';

type UserReducerType =
    | ActionSetToken
    | ActionSetMe
    | ActionUpdateMe
    | ActionCompleteTour
    | ActionCompleteJahOnboarding
    | ActionToggleOnline
    | ActionUpdateEmail;

export type UserReducerState = {
    online?: boolean;
} & (
    | (Patient & {
          authenticated: true;
          token: string;
          analyticsToken: string;
          resetPassword?: boolean;
      })
    | AnonymousUser
    | (AnonymousUser & { token: string; authenticated: true })
);

const initialState: UserReducerState = {
    authenticated: false,
    userType: '',
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
                    firstName: action.firstName,
                    guide: action.guide,
                    hasSecuritySteps: action.hasSecuritySteps,
                    lastName: action.lastName,
                    mobilePhone: action.mobilePhone,
                    mrn: action.mrn,
                    onboarded: action.onboarded,
                    ssid: action.ssid,
                    toolsToGoStatus: action.toolsToGoStatus,
                    tourComplete: action.tourComplete,
                    userType: 'patient',
                } as Patient; // TODO Should not need the "as Patient"
            } else {
                return {
                    ...state,
                    setupToken: action.setupToken,
                    setupUid: action.setupUid,
                    alreadySetUp: action.alreadySetUp,
                    setPasswordToken: action.setPasswordToken,
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
                    authenticated: action.authenticated,
                    analyticsToken: action.analyticsToken,
                    token: action.token,
                    currentWalkthroughStep:
                        action.currentWalkthroughStep || state.currentWalkthroughStep,
                    currentWalkthroughStepChanged:
                        action.currentWalkthroughStepChanged || state.currentWalkthroughStepChanged,
                    dateOfBirth: action.dateOfBirth || state.dateOfBirth,
                    email: action.email || state.email,
                    firstName: action.firstName || state.firstName,
                    guide: action.guide || state.guide,
                    hasSecuritySteps: action.hasSecuritySteps || state.hasSecuritySteps,
                    lastName: action.lastName || state.lastName,
                    mobilePhone: action.mobilePhone || state.mobilePhone,
                    mrn: action.mrn || state.mrn,
                    onboarded: action.onboarded || state.onboarded,
                    ssid: action.ssid || state.ssid,
                    toolsToGoStatus: action.toolsToGoStatus || state.toolsToGoStatus,
                    tourComplete: action.tourComplete || state.tourComplete,
                    userType: 'patient',
                };
            } else if (state.userType === '' && action.userType === '') {
                return {
                    ...state,
                    email: action.email || state.email,
                    mobilePhone: action.mobilePhone || state.mobilePhone,
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
        default:
            return state;
    }
};

export { UserReducer, initialState };
