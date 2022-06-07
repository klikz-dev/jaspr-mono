interface PatientVideo {
    id: number;
    activity: number;
    video: number;
    progress: number | null;
    rating: null | 1 | 2 | 3 | 4 | 5;
    saveForLater: null | boolean;
    viewed: null | boolean;
}

export type PatchRequest = Pick<PatientVideo, 'id'> & Partial<PatientVideo>;

export type PatchResponse = PatientVideo;

export type GetResponse = PatientVideo;
