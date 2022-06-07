import { AssessmentScores } from 'state/types';

export interface Activity {
    id: number;
    created: string; // 2022-02-23T01:28:48.648851Z
    startTime: null | string; // 2022-02-23T01:28:48.648851Z;
    status: 'not-started' | 'in-progress' | 'completed' | 'updated';
    statusUpdated: null | string; // 2022-02-23T01:28:48.648851Z;
    locked: boolean;
    type:
        | 'stability_plan'
        | 'intro'
        | 'comfort_and_skills'
        | 'lethal_means'
        | 'suicide_assessment'
        | 'outro';
    metadata: AssessmentScores | {};
    order: number;
}

export type GetResponse = Activity[];

export interface PostRequest {
    csp: boolean;
    csa: boolean;
    skills: boolean;
}

export type PostResponse = Activity[];
