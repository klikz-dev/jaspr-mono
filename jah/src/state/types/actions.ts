import { Dispatch as ReactDispatch } from 'react';

import {
    AssessmentConstants,
    ContactsConstants,
    CrisisStabilityPlanConstants,
    DeviceConstants,
    ErrorConstants,
    MediaConstants,
    SkillsConstants,
    StoriesConstants,
    UserConstants,
} from 'state/constants';

import {
    AssessmentAnswers,
    Walkthrough,
    ConversationStarter,
    CommonConcern,
    StaticMedia,
    Skills,
    SkillActivity,
    Stories,
    Patient,
    AnonymousUser,
    VideoRating,
    VideoRatings,
} from 'state/types';

import { UIDType } from 'components/ConversationalUi/questions';
import { Device } from './device';
import { CrisisStabilityPlan } from './crisisStabilityPlan';

// Reset

export interface ActionResetApp {
    type: 'RESET_APP';
    exclude?: ['user'];
}

// Assessment Actions

export interface ActionSetAssessment {
    type: AssessmentConstants.SET_ASSESSMENT;
    assessmentLockedAcknowledged: boolean;
    assessmentLocked: boolean;
    currentAssessment: number;
    currentSectionUid: UIDType;
    assessmentFinished: boolean;
    ssid?: string | null;
    answers: Partial<AssessmentAnswers>;
}

export interface ActionSetCrisisStabilityPlan {
    type: CrisisStabilityPlanConstants.SET_CRISIS_STABILITY_PLAN;
    crisisStabilityPlan: Partial<CrisisStabilityPlan>;
}

export interface ActionUpdateAnswers {
    type: AssessmentConstants.UPDATE_ANSWERS;
    answers: Partial<AssessmentAnswers>;
}

export interface ActionSetAnswer {
    type: AssessmentConstants.SET_ANSWERS;
    currentSectionUid?: UIDType;
    assessmentFinished: boolean;
    answers: Partial<AssessmentAnswers>;
}

export interface ActionSetWalkthrough {
    type: AssessmentConstants.SET_WALKTHROUGH;
    walkthrough: Walkthrough;
}

// Contact Actions

export interface ActionSetConversationStarters {
    type: ContactsConstants.SET_CONVERSATION_STARTERS;
    starters: ConversationStarter[];
}

export interface ActionSetCommonConerns {
    type: ContactsConstants.SET_COMMON_CONCERNS;
    concerns: CommonConcern[];
}

// Device Actions

export type ActionSetDevice = {
    type: DeviceConstants.SET_DEVICE;
} & Device;

// Error Actions

export interface ActionSetError {
    type: ErrorConstants.SET_ERROR;
    showError: boolean;
}

// Media Actions

export interface ActionSetFullscreen {
    type: MediaConstants.SET_FULLSCREEN;
    isFullScreen: boolean;
}

export interface ActionSetCaptionsEnabled {
    type: MediaConstants.SET_CAPTIONS_ENABLED;
    captionsEnabled: boolean;
}

export interface ActionSetMedia {
    type: MediaConstants.SET_MEDIA;
    media: StaticMedia;
}

// Skill  Actions

export interface ActionSetSkills {
    type: SkillsConstants.SET_SKILLS;
    skills: Skills;
}

export interface ActionSaveSkillForLater {
    type: SkillsConstants.SAVE_SKILL_FOR_LATER;
    skillActivity: SkillActivity;
}

export interface ActionRateSkills {
    type: SkillsConstants.RATE_SKILL;
    skillActivity: SkillActivity;
}

// Story Actions

export interface ActionSetStories {
    type: StoriesConstants.SET_STORIES;
    stories: Stories;
}

export interface ActionSetStoriesFetching {
    type: StoriesConstants.SET_STORIES_FETCHING;
}

export interface ActionFetchPatientVideos {
    type: StoriesConstants.FETCH_PATIENT_VIDEOS;
    videoRatings: VideoRatings;
}

export interface ActionSavePatientVideo {
    type: StoriesConstants.SAVE_PATIENT_VIDEO;
    videoRating: VideoRating;
}

// User Actions

export interface ActionSetToken {
    type: UserConstants.SET_TOKEN;
    token: string;
}

export type ActionSetMe = {
    type: UserConstants.SET_ME;
    //authenticated: true;
} & (Patient | AnonymousUser | null);

export type ActionUpdateMe = {
    type: UserConstants.UPDATE_ME;
} & { userType: 'patient' | '' } & (Partial<Patient> | Partial<AnonymousUser>);

export interface ActionCompleteTour {
    type: UserConstants.COMPLETE_TOUR;
}

export interface ActionCompleteJahOnboarding {
    type: UserConstants.COMPLETE_JAH_ONBOARDING;
}

export interface ActionToggleOnline {
    type: UserConstants.TOGGLE_ONLINE;
    online: boolean;
}

export interface ActionUpdateEmail {
    type: UserConstants.UPDATE_EMAIL;
    email: string;
}

export type Actions =
    | ActionResetApp
    | ActionSetAssessment
    | ActionSetCrisisStabilityPlan
    | ActionUpdateAnswers
    | ActionSetAnswer
    | ActionSetWalkthrough
    | ActionSetConversationStarters
    | ActionSetCommonConerns
    | ActionSetDevice
    | ActionSetError
    | ActionSetFullscreen
    | ActionSetCaptionsEnabled
    | ActionSetMedia
    | ActionSetSkills
    | ActionSaveSkillForLater
    | ActionRateSkills
    | ActionSetStories
    | ActionSetStoriesFetching
    | ActionFetchPatientVideos
    | ActionSavePatientVideo
    | ActionSetToken
    | ActionSetMe
    | ActionUpdateMe
    | ActionCompleteTour
    | ActionCompleteJahOnboarding
    | ActionToggleOnline
    | ActionUpdateEmail;

export type Dispatch = ReactDispatch<Actions>;
