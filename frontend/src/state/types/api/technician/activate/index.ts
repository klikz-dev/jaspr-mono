export interface PostRequest {
    email: string;
    activationCode: string;
    token: string;
    uid: string;
}

export interface PostResponse {
    setPasswordToken: string;
}

export interface PostErrorResponse {
    nonFieldErrors?: string[];
}
