interface PatientVideo {
    id: number;
    activity: number;
    video: number;
    progress: number | null;
    rating: null | 1 | 2 | 3 | 4 | 5;
    saveForLater: null | boolean;
    viewed: null | boolean;
}

export type PostRequest = Pick<PatientVideo, 'activity'> &
    Partial<Omit<PatientVideo, 'id, activity'>>;

export type PostResponse = PatientVideo;

export type GetResponse = PatientVideo[];
