interface PatientVideo {
    id: number;
    video: number;
    rating: null | 1 | 2 | 3 | 4 | 5;
    saveForLater: null | boolean;
    viewed: null | boolean;
    progress: number; //0-100
}

export type RequestCreatePatientVideo = Pick<PatientVideo, 'video'> &
    Partial<Omit<PatientVideo, 'id, video'>>;

export type RequestUpdatePatientVideo = Pick<PatientVideo, 'id'> & Partial<PatientVideo>;

export type ResponseListPatientVideo = PatientVideo[];

export type ResponsePatientVideo = PatientVideo;
