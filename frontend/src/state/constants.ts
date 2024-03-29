// User
export enum UserConstants {
    RESET_APP = 'RESET_APP',
    LOGIN_ERROR = 'LOGIN_ERROR',
    TOGGLE_ONLINE = 'TOGGLE_ONLINE',
    UPDATE_EMAIL = 'UPDATE_EMAIL',
    SELECT_GUIDE = 'SELECT_GUIDE',
    SET_ME = 'SET_ME',
    UPDATE_ME = 'UPDATE_ME',
    SET_PREFERENCES = 'SET_PREFERENCES',
    SET_GUIDE = 'SET_GUIDE',
    SET_PRIVACY_IMAGES = 'SET_PRIVACY_IMAGES',
    HEARTBEAT = 'HEARTBEAT',
    SET_SECURITY_QUESTIONS = 'SET_SECURITY_QUESTIONS',
    LOCK_SESSION = 'LOCK_SESSION',
    VALIDATE_SESSION = 'VALIDATE_SESSION',
    SET_SECURITY_IMAGE = 'SET_SECURITY_IMAGE',
    SAVE_SECURITY_QUESTION = 'SAVE_SECURITY_QUESTION',
    SET_TOKEN = 'SET_TOKEN',
    COMPLETE_TOUR = 'COMPLETE_TOUR',
    SETUP_TOOLS_TO_GO = 'SETUP_TOOLS_TO_GO',
    SET_TIME_SINCE_CHECKIN = 'SET_TIME_SINCE_CHECKIN',
    FETCH_LOCATIONS = 'FETCH_LOCATIONS',
    ACTIVATE_PATIENT = 'ACTIVATE_PATIENT',
    COMPLETE_JAH_ONBOARDING = 'COMPLETE_JAH_ONBOARDING',
    SET_ASSSESSMENT_LOCK_TIMER = 'SET_ASSSESSMENT_LOCK_TIMER',
}

// Assessment
export enum AssessmentConstants {
    SET_ASSESSMENT = 'SET_ASSESSMENT',
    SET_ANSWERS = 'SET_ANSWERS',
    UPDATE_ANSWERS = 'UPDATE_ANSWERS',
    SET_CURRENT_SECTION_UID = 'SET_CURRENT_SECTION_UID',
    SET_WALKTHROUGH = 'SET_WALKTHROUGH',
    SET_QUESTIONS = 'SET_QUESTIONS',
    SET_ACTIVITIES = 'SET_ACTIVITIES',
    UPDATE_ACTIVITIES = 'UPDATE_ACTIVITIES',
    SET_ASSSESSMENT_LOCK_TIMER = 'SET_ASSSESSMENT_LOCK_TIMER',
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
    MediaConstants;

export type ActionType =
    | 'RESET_APP'
    | 'LOGIN_ERROR'
    | 'SELECT_GUIDE'
    | 'SET_ME'
    | 'UPDATE_ME'
    | 'SET_PREFERENCES'
    | 'TOGGLE_ONLINE'
    | 'SET_GUIDE'
    | 'SET_PRIVACY_IMAGES'
    | 'HEARTBEAT'
    | 'SET_SECURITY_QUESTIONS'
    | 'LOCK_SESSION'
    | 'VALIDATE_SESSION'
    | 'SET_SECURITY_IMAGE'
    | 'SAVE_SECURITY_QUESTION'
    | 'SET_TOKEN'
    | 'COMPLETE_TOUR'
    | 'FETCH_LOCATIONS'
    | 'ACTIVATE_PATIENT'
    | 'SET_DEVICE'
    | 'SET_ASSESSMENT'
    | 'SET_ANSWERS'
    | 'SET_SKILLS'
    | 'SAVE_FOR_LATER'
    | 'SET_VIDEOS'
    | 'FETCH_PATIENT_VIDEOS'
    | 'SAVE_PATIENT_VIDEO'
    | 'SET_TIME_SINCE_CHECKIN'
    | 'UPDATE_EMAIL'
    | 'COMPLETE_JAH_ONBOARDING'
    | 'SET_WALKTHROUGH'
    | 'SET_QUESTIONS'
    | 'SET_ACTIVITIES'
    | 'UPDATE_ACTIVITIES'
    | 'SET_STORIES'
    | 'SET_STORIES_FETCHING'
    | 'SET_ERROR';
