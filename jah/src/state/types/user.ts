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
}

export interface Patient {
    authenticated: true; //TODO this is a field I add, not returned by the API.  Should be on a union type?
    analyticsToken: string;
    currentSession: number | null;
    token: null | string;
    currentWalkthroughStep: null; // TODO type
    currentWalkthroughStepChanged: string; // timestamp "2020-06-29T14:23:28.273000-05:00"
    dateOfBirth: string | null; // timestamp YYYY-MM-DD
    email: string;
    firstName: string;
    guide: 'Jasper' | 'Jaz' | null;
    hasSecuritySteps: boolean;
    id: number;
    lastName: string;
    mobilePhone: string;
    mrn: string;
    onboarded: boolean;
    ssid: string | null;
    toolsToGoStatus: 'Not Started' | 'Email Sent' | 'Phone Number Verified' | 'Setup Finished';
    tourComplete: boolean;
    userType: 'patient';
    online?: boolean;
}

export type User = Patient | AnonymousUser;
