export interface Amendment {
    id: number;
    comment: string;
    created: string; // "2020-06-22T15:09:21.048000-05:00"
    modified: string; // "2020-06-22T15:11:23.034000-05:00",
    noteType: 'narrative-note' | 'stability-plan';
    technician: {
        id: number;
        email: string;
        canEdit: boolean;
    };
}

export type GetResponse = Amendment[];

export type PutResponse = Amendment;

export interface PostRequest {
    noteType: 'narrative-note' | 'stability-plan';
    comment: string;
}

export type PostResponse = Amendment;

export type DeleteResponse = {};
