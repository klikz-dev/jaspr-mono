export interface GetResponse {
    answers: {
        [key: string]: any;
    };
    metadata: {
        currentSectionUid?: string;
        scoringScore?: 0 | 1 | 2 | 3 | 4 | 5 | 6;
        scoringCurrentAttempt?: 'Current Attempt' | 'No Current Attempt';
        scoringSuicidePlanAndIntent?:
            | 'Suicide Plan and Intent'
            | 'Suicide Plan or Intent'
            | 'No Suicide Plan or Intent';
        scoringRisk?: 'Low' | 'Moderate' | 'High';
        scoringSuicideIndexScore?: null | -2 | -1 | 0 | 1 | 2;
        scoringSuicideIndexScoreTypology?: 'Wish to Live' | 'Ambivalent' | 'Wish to Die';
    };
}

export interface PatchRequest {
    [key: string]: any;
}

export type PatchResponse = GetResponse;

export interface PatchErrorResponse {
    nonFieldErrors?: string[];
}
