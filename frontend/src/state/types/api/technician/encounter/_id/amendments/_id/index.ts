import { Amendment } from '../';

export type GetResponse = Amendment;

export interface PutRequest {
    noteType: 'narrative-note' | 'stability-plan';
    comment: string;
}

export type PutResponse = Amendment;
