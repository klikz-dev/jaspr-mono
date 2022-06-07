export interface PostRequest {
    email: string;
    fromNative: false;
    longLived: false;
    organizationCode: string;
    password: string;
}

export interface PostResponse {
    expiry: string; // 2022-03-23T20:12:09.643048-05:00,
    token: string;
    session: {
        userType: 'Technician';
        inEr: true;
        fromNative: false;
        longLived: false;
        encounter: null;
    };
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
}

export interface PostResponseError {
    nonFieldErrors?: string[];
    email?: string[];
    password?: string[];
    detail?: string[];
    error: true;
}
