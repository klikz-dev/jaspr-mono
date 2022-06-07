// NOTE.  This should be identical in shape to the reset-password/set-password endpoint

export interface PostRequest {
    password: string;
    token: string;
    uid: string;
    setPasswordToken: string;
    authToken: true;
}

export interface PostResponse {
    expiry: string; // 2022-03-23T20:12:09.643048-05:00,
    token: string;
    session: {
        userType: 'patient';
        inEr: true;
        fromNative: false;
        longLived: false;
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
        email: string;
        guide: 'Jasper' | 'Jaz' | '';
        hasSecuritySteps: boolean;
        id: number;
        inEr: boolean;
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
        onboarded: boolean;
        toolsToGoStatus: 'Not Started' | 'Email Sent' | 'Phone Number Verified' | 'Setup Finished';
        tourComplete: boolean;
        userType: 'patient';
    } & (
        | {
              ssid: string;
              firstName: '';
              lastName: '';
              dateOfBirth: null;
              mrn: '';
          }
        | {
              ssid: '';
              firstName: string;
              lastName: string;
              dateOfBirth: string | null; // 1985-10-11
              mrn: string;
          }
    );
}

export interface PostErrorResponse {
    nonFieldErrors?: string[];
    password?: string[];
    token?: string[];
    detail?: string[];
}
