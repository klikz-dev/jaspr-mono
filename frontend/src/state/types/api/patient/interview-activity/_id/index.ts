export interface PatchRequest {
    locked: boolean;
}

export interface PatchResponse {
    id: number;
    created: string; // "2022-01-13T16:19:43.190184Z"
    startTime: string; // "2022-01-13T16:19:43.190184Z"
    activityStatus: 'not-started' | 'in-progress' | 'completed' | 'updated';
    activityStatusUpdated: string; // "2022-01-13T16:19:43.190184Z"
    locked: boolean;
    activityType:
        | 'intro'
        | 'stability_plan'
        | 'lethal_means'
        | 'suicide_assessment'
        | 'outro'
        | 'comfort_and_skills';
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
