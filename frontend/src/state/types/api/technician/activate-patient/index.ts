import { PatientSerializer } from '../../sharedSerializers';

export interface PostRequest {
    department: number;
    patient: number;
}

export interface PostResponse {
    expiry: string; // 2022-03-23T20:12:09.643048-05:00,
    token: string;
    session: {
        userType: 'Patient';
        inEr: true;
        fromNative: false;
        longLived: false;
        encounter: number;
    };
    patient: PatientSerializer;
}

export interface PostErrorResponse {
    nonFieldErrors?: string[];
    department?: string[];
    patient?: string;
}
