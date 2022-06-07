export type GetResponse = {
    id: number;
    patient: number;
    note: string;
    noteType: 'narrative_note' | 'stability_plan';
    department: string;
    clinic: string;
    system: string;
    created: string; // 2022-02-23T15:40:47.722624Z
}[];

export type PostRequest = {
    encounter: number;
} & (
    | { narrativeNote: boolean; stabilityPlan?: boolean }
    | { narrativeNote?: boolean; stabilityPlan: boolean }
);

export interface PostResponse {
    status: 'ok';
}

// TODO Errors are not returning valid JSON
