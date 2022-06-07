import { Dispatch as ReactDispatch } from 'react';

import {
    AssessmentConstants,
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
    StaticMedia,
    Skills,
    SkillActivity,
    Stories,
    Patient,
    AnonymousUser,
    Technician,
    Departments,
    VideoRating,
    VideoRatings,
    PrivacyImages,
    SecurityQuestion,
} from 'state/types';

import {
    AssignedActivities,
    AssignedActivity,
    Questions,
    UIDType,
} from 'components/ConversationalUi/questions';
import { Device } from './device';
import { PatientPreferences } from './user';
import { PatientSerializer } from './api/sharedSerializers';

// Reset

export interface ActionResetApp {
    type: 'RESET_APP';
    exclude?: ['user'];
}

// Assessment Actions

export interface ActionSetQuestions {
    type: AssessmentConstants.SET_QUESTIONS;
    questions: Questions;
}

export interface ActionSetActivities {
    type: AssessmentConstants.SET_ACTIVITIES;
    activities: AssignedActivities;
}

export interface ActionUpdateActivities {
    type: AssessmentConstants.UPDATE_ACTIVITIES;
    activity: AssignedActivity;
}

export interface ActionSetAssessment {
    type: AssessmentConstants.SET_ASSESSMENT;
    //assessmentLockedAcknowledged: boolean;
    //assessmentLockedBy?: 'patient' | 'technician' | null;
    //assessmentLocked: boolean;
    currentAssessment: number;
    currentSectionUid: UIDType;
    ssid?: string | null;
    answers: Partial<AssessmentAnswers>;
}

export interface ActionUpdateAnswers {
    type: AssessmentConstants.UPDATE_ANSWERS;
    answers: Partial<AssessmentAnswers>;
}

export interface ActionSetAnswer {
    type: AssessmentConstants.SET_ANSWERS;
    currentSectionUid?: UIDType;
    answers: Partial<AssessmentAnswers>;
}

export interface ActionSetCurrentSectionUid {
    type: AssessmentConstants.SET_CURRENT_SECTION_UID;
    currentSectionUid: UIDType;
}

export interface ActionSetWalkthrough {
    type: AssessmentConstants.SET_WALKTHROUGH;
    walkthrough: Walkthrough;
}

export interface ActionSetAssessmentLockTimer {
    type: UserConstants.SET_ASSSESSMENT_LOCK_TIMER;
    assessmentLockTimer: number;
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

export interface ActionSetGuide {
    type: UserConstants.SET_GUIDE;
    guide: 'Jaz' | 'Jasper';
}

export type ActionSetMe = {
    type: UserConstants.SET_ME;
} & (Patient | Technician | AnonymousUser);

export type ActionUpdateMe = {
    type: UserConstants.UPDATE_ME;
} & (
    | ({ userType: 'patient' } & Partial<Patient>)
    | ({ userType: 'technician' } & Partial<Technician>)
    | ({ userType: '' } & Partial<AnonymousUser>)
);

export type ActionSetPreferences = {
    type: UserConstants.SET_PREFERENCES;
} & PatientPreferences;

export interface ActionFetchLocations {
    // TODO Change Fetch to Set
    type: UserConstants.FETCH_LOCATIONS;
    locations: Departments;
}

export interface ActionActivatePatient {
    type: UserConstants.ACTIVATE_PATIENT;
    patient: PatientSerializer;
    token: string;
    resetPassword?: boolean;
    technicianOperated?: boolean;
}

export interface ActionSetPrivacyImages {
    type: UserConstants.SET_PRIVACY_IMAGES;
    privacyImages: PrivacyImages;
}

export interface ActionHeartbeat {
    type: UserConstants.HEARTBEAT;
}

export interface ActionSetTimeSinceCheckin {
    type: UserConstants.SET_TIME_SINCE_CHECKIN;
    timeSinceCheckin: number;
}

export interface ActionSetSecurityQuestion {
    type: UserConstants.SET_SECURITY_QUESTIONS;
    securityQuestion: SecurityQuestion;
}

export interface ActionLockSession {
    type: UserConstants.LOCK_SESSION;
}

export interface ActionValidateSession {
    type: UserConstants.VALIDATE_SESSION;
}

export interface ActionSetSecurityImage {
    type: UserConstants.SET_SECURITY_IMAGE;
}

export interface ActionSaveSecurityQuestion {
    type: UserConstants.SAVE_SECURITY_QUESTION;
}

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

export interface ActionSetupToolsToGo {
    type: UserConstants.SETUP_TOOLS_TO_GO;
    inEr: boolean;
    mobilePhone: string;
    email: string;
    toolsToGoStatus: 'Not Started' | 'Email Sent' | 'Phone Number Verified' | 'Setup Finished';
}

export type Actions =
    | ActionResetApp
    | ActionSetQuestions
    | ActionSetActivities
    | ActionSetAssessment
    | ActionUpdateAnswers
    | ActionUpdateActivities
    | ActionSetAnswer
    | ActionSetCurrentSectionUid
    | ActionSetWalkthrough
    | ActionSetAssessmentLockTimer
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
    | ActionSetupToolsToGo;

export type Dispatch = ReactDispatch<Actions>;
