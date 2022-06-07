import { createContext } from 'react';

import { initialState as initialAssessment } from 'state/reducers/assessment';
import { initialState as initialContacts } from 'state/reducers/contacts';
import { initialState as initialCrisisStabilityPlan } from 'state/reducers/crisisStabilityPlan';
import { initialState as initialDevice } from 'state/reducers/device';
import { initialState as initialError } from 'state/reducers/error';
import { initialState as initialMedia } from 'state/reducers/media';
import { initialState as initialSkills } from 'state/reducers/skills';
import { initialState as initialStories, StoriesReducerState } from 'state/reducers/stories';
import { initialState as initialUser } from 'state/reducers/user';

import type {
    Assessment,
    Contacts,
    CrisisStabilityPlan,
    Device,
    Error,
    Media,
    Skills,
    User,
} from 'state/types';

import { Dispatch } from 'state/types';

const initialState = {
    assessment: initialAssessment,
    contacts: initialContacts,
    crisisStabilityPlan: initialCrisisStabilityPlan,
    device: initialDevice,
    error: initialError,
    media: initialMedia,
    skills: initialSkills,
    stories: initialStories,
    user: initialUser,
};

interface IContext {
    assessment: Assessment;
    contacts: Contacts;
    crisisStabilityPlan: CrisisStabilityPlan;
    device: Device;
    error: Error;
    media: Media;
    skills: Skills;
    stories: StoriesReducerState;
    user: User;
}

export default createContext<[IContext, Dispatch]>([initialState, undefined!]);
