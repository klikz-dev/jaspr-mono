import { PatientSerializer } from '../../sharedSerializers';

// NOTE: This endpoint is used by Epic to initiate OAuth handshake and not for internal API use
export interface PostRequest {
    redirectUri: string;
    code: string;
    tokenUrl: string;
    state: string;
    iss: string;
}

export interface PostResponse {
    token: string;
    technician: {
        id: number;
        location: {
            system: {
                name: string;
                id: number;
            };
        };
        userType: 'technician';
        analyticsToken: string;
        firstName: string;
        lastName: string;
        email: string;
        role: string;
        supportUrl: string;
    };
    patient: PatientSerializer;
}
