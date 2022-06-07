interface PatientActivity {
    id: number;
    activity: number;
    rating: null | 1 | 2 | 3 | 4 | 5;
    saveForLater: null | boolean;
    viewed: null | boolean;
}

export type PostRequest = Pick<PatientActivity, 'activity'> &
    Partial<Omit<PatientActivity, 'id, activity'>>;

export type PostResponse = PatientActivity;

export type GetResponse = PatientActivity[];
