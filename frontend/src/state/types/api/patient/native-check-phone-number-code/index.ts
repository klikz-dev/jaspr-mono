/**
 * JAH Only endpoint
 */
export interface PostRequest {
    email: string;
    mobilePhone: string;
    code: string;
    longLived: true;
}

/**
 * JAH Only endpoint
 */
export interface PostResponse {
    token: string;
    uid: string;
    alreadySetUp: boolean;
    setPasswordToken: string;
}

export interface PostErrorResponse {
    code?: string[];
}
