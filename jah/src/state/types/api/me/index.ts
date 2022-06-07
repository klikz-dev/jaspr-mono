interface MePatient {
    id: number;
    userType: 'patient';
    currentSectionUid: string;
    assessmentFinished: boolean;
    guide: 'Jasper' | 'Jaz' | '';
    tourComplete: boolean;
    onboarded: boolean;
    hasSecuritySteps: boolean;
    email: string;
    mobilePhone: string;
    toolsToGoStatus: 'Not Started' | 'Email Sent' | 'Phone Number Verified' | 'Setup Finished';
    currentWalkthroughStep: null | string; // Currently unused by frontend
    currentWalkthroughStepChanged: string; //"2020-06-30T16:10:39.240000-05:00" // Currently unused by frontend
    analyticsToken: string;
    mrn: string;
    ssid: string;
    dateOfBirth: null | string; //2004-12-31
    firstName: string;
    lastName: string;
    activities: {
        csa: boolean;
        csp: boolean;
        skills: boolean;
    };
}

export type ResponseMe = MePatient;

export type RequestUpdateMe = Partial<
    Pick<MePatient, 'guide' | 'tourComplete' | 'email' | 'mobilePhone'>
>;
