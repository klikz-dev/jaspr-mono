import { Questions } from 'components/ConversationalUi/questions';
import { AssessmentScores } from '.';
import { AssessmentAnswers } from './assessment';
import { VideoRatings } from './media';
import { Skills } from './skill';

export interface AnonymousUser {
    authenticated: false;
    userType: '' | null;
    token?: string; // Set when restoring state but user is not yet known
    setPasswordToken?: string;
    setupToken?: string;
    setupUid?: string;
    alreadySetUp?: string;
    email?: string;
    mobilePhone?: string;
    online?: boolean;
}

type ToolsToGoStatus = 'Not Started' | 'Email Sent' | 'Phone Number Verified' | 'Setup Finished';

export interface Patient {
    activities: { csp: boolean; csa: boolean; skills: boolean };
    analyticsToken: string;
    authenticated: true; // TODO this is a field I add, not returned by the API.  Should be on a union type?
    assessmentLockTimer?: number;
    technicianOperated?: boolean;
    consentLanguage?: string;
    currentWalkthroughStep: null | string;
    currentWalkthroughStepChanged: string; // timestamp "2020-06-29T14:23:28.273000-05:00"
    dateOfBirth: string | null; // timestamp YYYY-MM-DD
    email: string;
    firstName: string;
    guide: 'Jasper' | 'Jaz' | '';
    hasSecuritySteps: boolean;
    id: number;
    inEr: boolean;
    lastName: string;
    location?: {
        system: { id: number; name: string };
        clinic: { id: number; name: string };
        department: { id: number; name: string };
    };
    mobilePhone: string;
    mrn: string;
    onboarded: boolean;
    online?: boolean;
    privacyImages?: PrivacyImages;
    securityQuestion?: SecurityQuestion;
    sessionLocked?: boolean;
    ssid: string | null;
    timeSinceCheckin?: number;
    timezone?: string;
    token: null | string;
    toolsToGoStatus: ToolsToGoStatus;
    tourComplete: boolean;
    userType: 'patient';
}

export interface Technician {
    authenticated: true; // TODO this is a field I add, not returned by the API.  Should be on a union type?
    analyticsToken: string;
    department: string;
    token: null | string;
    id: number;
    locations?: Department[];
    location?: {
        system: {
            id: number;
            name: string;
        };
        clinic: { id: number; name: string };
        department: { id: number; name: string };
    };
    role: string; // TODO What roles are available
    userType: 'technician';
    firstName: string;
    lastName: string;
    supportUrl: string;
    email: string;
    online?: boolean;
}

export interface Department {
    id: number;
    name: string;
}

export type Departments = Department[];

export interface PrivacyImage {
    id: number;
    url: string;
}

export type PrivacyImages = PrivacyImage[];

export interface SecurityQuestion {
    id?: number;
    question: string;
}

export type User = (Patient | Technician | AnonymousUser) & { authenticated: boolean };

export interface PatientData {
    answers: {
        answers: AssessmentAnswers;
        metadata: AssessmentScores;
    };
    patientVideos: VideoRatings;
    questions: Questions;
    skills: Skills;
    storiesVideos: [];
}

export interface Preferences {
    timezone: string;
    providerNotes: boolean;
    stabilityPlanLabel: string;
}

export interface PatientPreferences {
    timezone: string;
    consentLanguage: string;
}

export interface Activity {
    created: string;
    order: number;
    status: 'not-started' | 'in-progress' | 'completed' | 'updated';
    statusUpdated: string;
    type:
        | 'outro'
        | 'intro'
        | 'lethal_means'
        | 'comfort_and_skills'
        | 'suicide_assessment'
        | 'stability_plan';
    id: number;
    locked: boolean;
    metadata: {
        currentSectionUid?: string;
        scoringScore?: null | 0 | 1 | 2 | 3 | 4 | 5 | 6;
        scoringCurrentAttempt?: 'Current Attempt' | 'No Current Attempt';
        scoringSuicidePlanAndIntent?:
            | 'Suicide Plan and Intent'
            | 'Suicide Plan or Intent'
            | 'No Suicide Plan or Intent';
        scoringRisk?: 'Low' | 'Moderate' | 'High';
        scoringSuicideIndexScore?: null | -2 | -1 | 0 | 1 | 2;
        scoringSuicideIndexScoreTypology?: 'Wish to Live' | 'Ambivalent' | 'Wish to Die';
    };
    startTime: string;
}
