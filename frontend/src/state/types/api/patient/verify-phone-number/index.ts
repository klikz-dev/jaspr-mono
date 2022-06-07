// Note: Shape should be identical to reset-password/verify-phone-number

export interface PostResponse {
    setPasswordToken: string;
}

export interface PostRequest {
    code: string;
    uid: string;
    token: string;
}

export interface PostErrorResponse {
    nonFieldErrors?: string[];
}
