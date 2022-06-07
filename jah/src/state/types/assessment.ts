import { Questions, UIDType } from 'components/ConversationalUi/questions';

export type AssessmentAnswers = Partial<{
    abuseYesNo: boolean | null;
    abuseYesNoDescribe: boolean | null;
    burdenOnOthersYesNo: boolean | null;
    burdenOnOthersYesNoDescribe: null;
    cannotRidMeansDec: "Yes, I'll think with you" | 'Skip for now';
    causesAgitation: string | null;
    checkInTime0: string | null;
    checkInTime1: string | null;
    checkInTime2: string | null;
    copingBody: Array<string> | null;
    copingCourage: Array<string> | null;
    copingDistract: Array<string> | null;
    copingHelpOthers: Array<string> | null;
    copingSenses: Array<string> | null;
    copingTop: Array<string> | null;
    created: string;
    crisisDesc: string | null;
    currentYesNo: boolean | null;
    currentYesNoDescribe: string | null;
    distress0: null | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
    distress1: null | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
    distress2: null | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
    doNotNeedDec: "Yes, I'll think with you" | 'Skip for now';
    feelDepressedDec: "Yes, I'll think with you" | 'Skip for now';
    firearmsYesNo: boolean | null;
    firearmsYesNoDescribe: string | null;
    frustration0: null | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
    frustration1: null | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
    frustration2: null | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
    healthYesNo: boolean | null;
    healthYesNoDescribe: string | null;
    hospitalizedYesNo: boolean | null;
    hospitalizedYesNoDescribe: string | null;
    impulsiveYesNo: boolean | null;
    impulsiveYesNoDescribe: string | null;
    intentYesNo: boolean | null;
    intentYesNoDescribe: string | null;
    jasprRating: number | null;
    jasprRecommend: boolean | null;
    keepInHospitalDec: "Yes, I'll think with you" | 'Skip for now';
    keepMeansDec: "Yes, I'll think with you" | 'Skip for now';
    legalYesNo: boolean | null;
    legalYesNoDescribe: string | null;
    lengthSuicidalThought: 'seconds' | 'minutes' | 'hours';
    lossesYesNo: boolean | null;
    lossesYesNoDescribe: string | null;
    meansSupportWho: string | null;
    meansSupportYesNo: boolean | null;
    meansWilling: string | null;
    meansYesNo: boolean | null;
    meansYesNoDescribe: string | null;
    modified: string;
    mostHate: string | null;
    mostHopeless: string | null;
    mostPainful: string | null;
    mostStress: string | null;
    notSureTalkDec: "Yes, I'll think with you" | 'Skip for now';
    nssiYesNo: boolean | null;
    nssiYesNoDescribe: string | null;
    oneThing: string | null;
    overallErCare: null; // No longer used
    overreactKeepMeDec: "Yes, I'll think with you" | 'Skip for now';
    overreactSpecific: 'Take away means' | 'Keep me in hospital against my will';
    overreactTakeAwayDec: "Yes, I'll think with you" | 'Skip for now';
    planYesNo: boolean | null;
    planYesNoDescribe: string | null;
    practicedYesNo: boolean | null;
    practicedYesNoDescribe: string | null;
    rankFeelings: string; // '1,2,3,4,5'
    rateAgitation: null | 1 | 2 | 3 | 4 | 5;
    rateHopeless: null | 1 | 2 | 3 | 4 | 5;
    ratePsych: null | 1 | 2 | 3 | 4 | 5;
    rateSelfHate: null | 1 | 2 | 3 | 4 | 5;
    rateStress: null | 1 | 2 | 3 | 4 | 5;
    readiness: 'Not at all ready' | 'Somewhat ready' | 'Very ready';
    readinessChanged: null; // No longer used
    readinessDescribe: string | null; // No longer used
    readinessNo: string | null;
    readinessYesChanged: string | null;
    readinessYesReasons: (
        | 'I need to take care of my obligations'
        | 'I feel better and calmer'
        | 'I feel ready to cope'
        | 'My urge has gone down'
        | 'This was a misunderstanding'
        | "I'm frustrated"
        | 'People who support me understand how serious I am'
        | 'My circumstances have changed'
    )[];
    reasonNotSureTalk: (
        | "I'll be forced to do something I don't want to do"
        | "I'm undecided if I want to kill myself"
        | "I want to kill myself and don't want to be blocked"
        | "I don't want my answers about this recorded"
        | "I'm mixed about reducing access"
        | 'Having access is comforting - I have a way out'
    )[];
    reasonsDie: Array<string> | null;
    reasonsLive: Array<string> | null;
    relationshipYesNo: boolean | null;
    relationshipYesNoDescribe: string | null;
    scoringCurrentAttempt: 'Current Attempt' | 'No Current Attempt' | null;
    scoringRisk: null | 0 | 1 | 2 | 3 | 4 | 5;
    scoringScore: null | 0 | 1 | 2 | 3 | 4 | 5;
    scoringSuicideIndexScore: null | -2 | -1 | 0 | 1 | 2;
    scoringSuicideIndexScoreTypology: null; // Not used
    scoringSuicidePlanAndIntent:
        | 'Suicide Plan and intent | Suicide Plan or Intent'
        | 'No Suicide Plan or Intent'
        | null;
    shameYesNo: boolean | null;
    shameYesNoDescribe: string | null;
    skipLethalMeans: "Yes, I'll think with you" | 'Skip for now' | null;
    skipReason:
        | 'Too tired'
        | 'Too private'
        | "I'm worried people will overreact"
        | "I'm not sure I want to talk about it"
        | "It's too shameful"
        | "I don't need to do this"
        | 'Cannot get rid of means'
        | 'Not sure I want to be stable'
        | 'I want to keep my means'
        | "I'm afraid this will keep me in the hospital"
        | 'I feel too depressed or overwhelmed'
        | null;
    sleepYesNo: boolean | null;
    sleepYesNoDescribe: string | null;
    stabilityConfidence: number | null;
    stabilityRehearsal: string | null;
    stableDec: "Yes, I'll think with you" | 'Skip for now' | null;
    stepsYesNo: boolean | null;
    stepsYesNoDescribe: string | null;
    strategiesCustom: Array<string>;
    strategiesFirearm: Array<string>;
    strategiesGeneral: Array<string>;
    strategiesMedicine: Array<string>;
    strategiesOther: Array<string>;
    strategiesPlaces: Array<string>;
    suicidalFreq: number;
    suicidalFreqUnits: 'day' | 'week' | 'month';
    suicidalOthers: null; // TODO
    suicidalYesNo: boolean | null;
    suicidalYesNoDescribe: string | null;
    suicidalYourself: null; // TODO
    suicideRisk: null; // TODO
    supportivePeople: Array<{
        name: string | null;
        phone: string | null;
    }>;
    timeHere:
        | 'Just got here'
        | 'At least a few hours, less than 24 hours'
        | 'More than 24 hours'
        | null;
    timesTried: 'once' | 'many';
    timesTriedDescribe: string | null;
    tooPrivateDec: "Yes, I'll think with you" | 'Skip for now' | null;
    tooShamefulDec: "Yes, I'll think with you" | 'Skip for now';
    walkThrough: 'Got it' | 'Sounds good' | null;
    willCheckIn: 'Got it' | 'Okay, talk to you later' | null;
    willingToTalk: "Yes, I'm good with that" | 'No, just provider' | null;
    wishDie: null | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;
    wishLive: null | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;
    worseYesNo: boolean | null;
    worseYesNoDescribe: string | null;
    wsActions: Array<
        | 'Problems sleeping'
        | 'Avoiding people'
        | 'Pacing'
        | 'Harming myself'
        | 'Practicing/rehearsing suicide attempt'
        | 'Crying'
        | 'Yelling/screaming'
        | 'Getting ready for suicide attempt'
    > | null;
    wsFeelings: Array<
        | 'Feeling on edge'
        | 'Restless'
        | 'Shaking/trembling'
        | 'Nausea'
        | 'Panicky'
        | 'Physical pain'
        | 'Guilt'
        | 'Anger'
        | 'Worry'
        | 'Shame'
        | 'Sadness'
    > | null;
    wsStressors: Array<'Conflict in relationship' | 'Conflict with family or friend'> | null;
    wsThoughts: Array<'This will never end' | "I can't take it anymore"> | null;
    wsTop: Array<string> | null;
    [answerKey: string]: any;
}>;

export interface Assessment {
    //id: number;
    //currentAssessment: number | null;
    answers: Partial<AssessmentAnswers>;
    currentSectionUid: UIDType;
    assessmentFinished: boolean;
    ssid: string | null;
    questions?: Questions;
    walkthrough: any; // TODO Type walkthrough.  Maybe move to it's own reducer?
}
