// NOTE.  This should be identical in shape to the set-password endpoint

import { PatientSerializer } from 'state/types/api/sharedSerializers';

/**
 * JAH Only endpoint
 */
export interface PostRequest {
    password: string;
    token: string;
    uid: string;
    setPasswordToken: string;
    authToken: true;
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
    patient: PatientSerializer;
}

export interface PostErrorResponse {
    nonFieldErrors?: string[];
    password?: string[];
    token?: string[];
    detail?: string[];
}
