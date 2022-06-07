// User
export enum UserConstants {
    RESET_APP = 'RESET_APP',
    LOGIN_ERROR = 'LOGIN_ERROR',
    TOGGLE_ONLINE = 'TOGGLE_ONLINE',
    UPDATE_EMAIL = 'UPDATE_EMAIL',
    SELECT_GUIDE = 'SELECT_GUIDE',
    SET_ME = 'SET_ME',
    UPDATE_ME = 'UPDATE_ME',
    SET_TOKEN = 'SET_TOKEN',
    COMPLETE_TOUR = 'COMPLETE_TOUR',
    COMPLETE_JAH_ONBOARDING = 'COMPLETE_JAH_ONBOARDING',
}

// Assessment
export enum AssessmentConstants {
    SET_ASSESSMENT = 'SET_ASSESSMENT',
    SET_ANSWERS = 'SET_ANSWERS',
    UPDATE_ANSWERS = 'UPDATE_ANSWERS',
    SET_CURRENT_SECTION_UID = 'SET_CURRENT_SECTION_UID',
    SET_WALKTHROUGH = 'SET_WALKTHROUGH',
}

// Device
export enum DeviceConstants {
    SET_DEVICE = 'SET_DEVICE',
}

// Skills
export enum SkillsConstants {
    SET_SKILLS = 'SET_SKILLS',
    SAVE_SKILL_FOR_LATER = 'SAVE_SKILL_FOR_LATER',
    RATE_SKILL = 'RATE_SKILL',
}

// Shared Stories
export enum StoriesConstants {
    SET_STORIES = 'SET_STORIES',
    SET_STORIES_FETCHING = 'SET_STORIES_FETCHING',
    SET_VIDEOS = 'SET_VIDEOS',
    FETCH_PATIENT_VIDEOS = 'FETCH_PATIENT_VIDEOS',
    SAVE_PATIENT_VIDEO = 'SAVE_PATIENT_VIDEO',
}

// Contacts
export enum ContactsConstants {
    SET_CONVERSATION_STARTERS = 'SET_CONVERSATION_STARTERS',
    SET_COMMON_CONCERNS = 'SET_COMMON_CONCERNS',
}

// CrisisStabilityPlan
export enum CrisisStabilityPlanConstants {
    SET_CRISIS_STABILITY_PLAN = 'SET_CRISIS_STABILITY_PLAN',
}

// Media
export enum MediaConstants {
    SET_MEDIA = 'SET_MEDIA',
    SET_FULLSCREEN = 'SET_FULLSCREEN',
    SET_CAPTIONS_ENABLED = 'SET_CAPTIONS_ENABLED',
}

// Errors
export enum ErrorConstants {
    SET_ERROR = 'SET_ERROR',
}

export type DispatchTypes = UserConstants &
    AssessmentConstants &
    DeviceConstants &
    ErrorConstants &
    SkillsConstants &
    ContactsConstants &
    MediaConstants;

export type ActionType =
    | 'RESET_APP'
    | 'LOGIN_ERROR'
    | 'SELECT_GUIDE'
    | 'SET_ME'
    | 'UPDATE_ME'
    | 'TOGGLE_ONLINE'
    | 'SET_TOKEN'
    | 'COMPLETE_TOUR'
    | 'SET_DEVICE'
    | 'SET_SKILLS'
    | 'SAVE_FOR_LATER'
    | 'SET_VIDEOS'
    | 'FETCH_PATIENT_VIDEOS'
    | 'SAVE_PATIENT_VIDEO'
    | 'UPDATE_EMAIL'
    | 'SET_CONVERSATION_STARTERS'
    | 'SET_COMMON_CONCERNS'
    | 'COMPLETE_JAH_ONBOARDING'
    | 'SET_WALKTHROUGH'
    | 'SET_QUESTIONS'
    | 'SET_STORIES'
    | 'SET_STORIES_FETCHING'
    | 'SET_ERROR';
