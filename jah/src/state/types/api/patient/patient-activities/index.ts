interface PatientActivity {
    id: number;
    activity: number;
    rating: null | 1 | 2 | 3 | 4 | 5;
    saveForLater: null | boolean;
    viewed: null | boolean;
}

export type RequestCreatePatientActivity = Pick<PatientActivity, 'activity'> &
    Partial<Omit<PatientActivity, 'id, activity'>>;

export type RequestUpdatePatientVideo = Pick<PatientActivity, 'id'> & Partial<PatientActivity>;

export type ResponseListPatientVideo = PatientActivity[];

export type ResponsePatientVideo = PatientActivity;
