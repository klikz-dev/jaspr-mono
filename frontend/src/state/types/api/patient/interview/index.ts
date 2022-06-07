import { Question } from 'components/ConversationalUi/questions';
import { AssessmentScores } from 'state/types';

export type GetResponse = {
    id: number;
    created: string; // 2022-02-26T17:04:05.993896Z
    startTime: null | string;
    status: 'not-started' | 'in-progress' | 'completed' | 'updated';
    statusUpdated: null | string;
    type:
        | 'intro'
        | 'stability_plan'
        | 'lethal_means'
        | 'suicide_assessment'
        | 'outro'
        | 'comfort_and_skills';
    locked: boolean;
    metadata: AssessmentScores | {};
    progressBarLabel: null | string;
    questions: Question[];
}[];
