import { Activity } from '../';

export interface PatchRequest {
    locked: boolean;
}

export type PatchResponse = Activity;
