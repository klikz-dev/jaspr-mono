/**
 * JAH Only endpoint
 */
export interface PostRequest {
    email: string;
    fromNative: true;
    longLived: true;
    password: string;
}

/**
 * JAH Only endpoint
 */
export interface PostResponse {
    expiry: string; // 2022-03-23T20:12:09.643048-05:00,
    token: string;
    session: {
        userType: 'patient';
        inEr: false;
        fromNative: true;
        longLived: true;
        encounter: null;
    };
    patient: {
        activities: {
            csa: boolean;
            csp: boolean;
            skills: boolean;
        };
        analyticsToken: string;
        currentWalkthroughStep: null | string;
        currentWalkthroughStepChanged: string; //"2020-06-30T16:10:39.240000-05:00",
        dateOfBirth: null | string; // 2004-12-31
        email: string;
        firstName: string;
        guide: 'Jasper' | 'Jaz' | '';
        hasSecuritySteps: boolean;
        id: number;
        inEr: boolean;
        lastName: string;
        location: {
            system: {
                id: number;
                name: string;
            };
            clinic: {
                id: number;
                name: string;
            };
            department: {
                id: number;
                name: string;
            };
        };
        mobilePhone: string;
        mrn: string;
        onboarded: boolean;
        ssid: string | null;
        toolsToGoStatus: 'Not Started' | 'Email Sent' | 'Phone Number Verified' | 'Setup Finished';
        tourComplete: boolean;
        userType: 'patient';
    };
}
