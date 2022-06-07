interface PatientActivity {
    id: number;
    activity: number;
    rating: null | 1 | 2 | 3 | 4 | 5;
    saveForLater: null | boolean;
    viewed: null | boolean;
}

export type PatchRequest = Pick<PatientActivity, 'id'> & Partial<PatientActivity>;

export type PatchResponse = PatientActivity;

export type GetResponse = PatientActivity;
