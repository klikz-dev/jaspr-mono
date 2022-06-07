export interface ProviderComment {
    id: number;
    answerKey: string;
    comment: string;
    created: string; // "2020-06-22T15:09:21.048000-05:00"
    modified: string; // "2020-06-22T15:11:23.034000-05:00",
    technician: {
        id: number;
        firstName: string;
        lastName: string;
        email: string;
        canEdit: boolean;
    };
}

export type GetResponse = {
    [key: string]: ProviderComment[];
};

export interface PostRequest {
    answerKey: string;
    comment: string;
}

export type PostResponse = ProviderComment;
