import { ProviderComment } from '../';

export interface PatchRequest {
    answerKey: string;
    comment: string;
}

export type PatchResponse = ProviderComment;
