import { actionNames } from 'state/actions/analytics';

export interface PostRequest {
    action: typeof actionNames;
    screen?: string;
    extra?: string;
    section_uid?: string;
    client_timestamp: string; //"2021-12-07T12:05:23.1234Z"
}

export interface PostResponse {}
