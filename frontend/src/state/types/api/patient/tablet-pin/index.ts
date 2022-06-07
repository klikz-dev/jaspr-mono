import { PatientSerializer } from '../../sharedSerializers';

export type PostRequest = {
    pinCode: string;
} & ({ departmentCode: string } | { systemCode: string });

export interface PostResponse {
    expiry: string; // 2022-03-23T20:12:09.643048-05:00,
    token: string;
    session: {
        userType: 'patient';
        inEr: true;
        fromNative: false;
        longLived: false;
        encounter: number;
    };
    technicianOperated: boolean;
    patient: PatientSerializer;
}

export interface PostErrorResponse {
    detail?: string;
    nonFieldErrors?: string[];
}
