/**
 * JAH Only endpoint
 * Allows user to change their password
 */
export interface PostResponse {}

/**
 * JAH Only endpoint
 * Allows user to change their password
 */
export interface PostRequest {
    currentPassword: string;
    password: string;
}
