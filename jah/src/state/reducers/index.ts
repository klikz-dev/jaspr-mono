import Storage from 'lib/storage';
import { AssessmentReducer } from './assessment';
import { SkillsReducer } from './skills';
import { StoriesReducer } from './stories';
import { UserReducer } from './user';
import { ContactsReducer } from './contacts';
import { MediaReducer } from './media';
import { ErrorReducer } from './error';
import { UserConstants } from 'state/constants';
import { Actions } from 'state/types';

import { initialState as initialAssessment } from 'state/reducers/assessment';
import { initialState as initialContacts } from 'state/reducers/contacts';
import { initialState as initialError } from 'state/reducers/error';
import { initialState as initialMedia } from 'state/reducers/media';
import { initialState as initialSkills } from 'state/reducers/skills';
import { initialState as initialStories } from 'state/reducers/stories';
import { initialState as initialUser } from 'state/reducers/user';
import { CrisisStabilityPlanReducer } from './crisisStabilityPlan';
import { DeviceReducer } from './device';

export type CombinedReducer = {
    assessment: typeof AssessmentReducer;
    crisisStabilityPlan: typeof CrisisStabilityPlanReducer;
    device: typeof DeviceReducer;
    skills: typeof SkillsReducer;
    stories: typeof StoriesReducer;
    user: typeof UserReducer;
    contacts: typeof ContactsReducer;
    media: typeof MediaReducer;
    error: typeof ErrorReducer;
};

export interface ActionResetApp {
    type: 'RESET_APP';
    exclude?: [keyof CombinedReducer];
}

export const initialState = {
    assessment: initialAssessment,
    contacts: initialContacts,
    error: initialError,
    media: initialMedia,
    skills: initialSkills,
    stories: initialStories,
    user: initialUser,
};

// @ts-ignore
const combineReducers =
    (slices: CombinedReducer): CombinedReducer =>
    // @ts-ignore
    (state: CombinedReducer, action: Actions | ActionResetApp) => {
        if (!state) {
            return {};
        }
        return Object.keys(slices).reduce((acc, prop) => {
            return {
                ...acc,
                //@ts-ignore //TODO FIXME
                [prop]: slices[prop](acc[prop], action),
            };
        }, state);
    };

const allReducers = combineReducers({
    assessment: AssessmentReducer,
    crisisStabilityPlan: CrisisStabilityPlanReducer,
    device: DeviceReducer,
    skills: SkillsReducer,
    stories: StoriesReducer,
    user: UserReducer,
    contacts: ContactsReducer,
    media: MediaReducer,
    error: ErrorReducer,
});

const rootReducer = (state: CombinedReducer, action: Actions | ActionResetApp) => {
    if (action.type === UserConstants.RESET_APP) {
        const stateReference: CombinedReducer = state;

        Storage.removeSecureItem('token');
        Storage.removeSecureItem('userType');
        Storage.removeStorageItem('credentialsStored');

        if (state) {
            state = {
                // Preserve device specific metadata across app resets
                device: {
                    // @ts-ignore
                    deptId: stateReference['device']['deptId'],
                    // @ts-ignore
                    isTablet: stateReference['device']['isTablet'],
                },
                // Don't clear out static media.
                // It does not serve different content for different users or user types
                media: stateReference.media,
            };
        } else {
            state = undefined;
        }
    }
    // @ts-ignore
    return allReducers(state, action);
};

export default rootReducer;
