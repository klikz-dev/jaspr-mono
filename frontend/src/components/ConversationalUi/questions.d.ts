/* export type UIDType =
    | '' // When blank, analytic for question is not recorded
    | 'abuseDescribe'
    | 'additionalStrategies'
    | 'burdenDescribe'
    | 'checkinThankYou'
    | 'collectEmail'
    | 'collectPhone'
    | 'comfortAndSkills'
    | 'considerReducingAccess'
    | 'copingBody'
    | 'copingCourage'
    | 'copingDistract'
    | 'copingHelpOthers'
    | 'copingSenses'
    | 'copingTop'
    | 'crisisDesc'
    | 'currentDescribe'
    | 'desireToHarm'
    | 'drivers'
    | 'explore'
    | 'firearmDescribe'
    | 'getHelp'
    | 'healthDescribe'
    | 'hospitalizedDescribe'
    | 'iCanHelp'
    | 'impulsiveDescribe'
    | 'intentDescribe'
    | 'jahOnboardGlad'
    | 'jahOnboardShowHow'
    | 'jahOnboardSlideShow'
    | 'jahOnboardDisclaimer'
    | 'jahOnboardToughTime'
    | 'jahOnboardWelcome'
    | 'jasprRating'
    | 'jasprRecommend'
    | 'legalDescribe'
    | 'lethalMeansAfraidHospital'
    | 'lethalMeansDontNeed'
    | 'lethalMeansGetRid'
    | 'lethalMeansNotStable'
    | 'lethalMeansTooDepressed'
    | 'lethalMeansTooShameful'
    | 'lethalMeansWantToKeep'
    | 'lossesDescribe'
    | 'makeHomeStart'
    | 'meansCustom'
    | 'meansDescribe'
    | 'meansDescribeReview'
    | 'meansSupport'
    | 'meansWilling'
    | 'nssiDescribe'
    | 'okReady'
    | 'oneThing'
    | 'overallErCare'
    | 'plansDescribe'
    | 'practicedDescribe'
    | 'rankFeelings'
    | 'rankReasonsDie'
    | 'rankReasonsLive'
    | 'rateAgitation'
    | 'rateAgitationText'
    | 'rateDistress'
    | 'rateDistress1'
    | 'rateFrustration'
    | 'rateFrustration1'
    | 'rateHopeless'
    | 'rateHopelessText'
    | 'ratePsych'
    | 'ratePsychText'
    | 'rateSelfHate'
    | 'rateSelfHateText'
    | 'rateStress'
    | 'rateStressText'
    | 'readiness'
    | 'readinessNo'
    | 'readinessYesChanged'
    | 'readinessYesReasons'
    | 'reasonDontWantToTalk'
    | 'reasonDontWantToTalkAll'
    | 'reasonDontWantToTalkAllSkip'
    | 'reasonPeopleWillOverreact'
    | 'reasonPeopleWillOverreactKeepAgainstWill'
    | 'reasonPeopleWillOverreactKeepAgainstWillSkip'
    | 'reasonPeopleWillOverreactTakeAwayMeans'
    | 'reasonPeopleWillOverreactTakeAwayMeansSkip'
    | 'reasonsLiveDie'
    | 'reasonsLiveEdit'
    | 'reasonTooPrivate'
    | 'reasonTooTired'
    | 'relationshipDescribe'
    | 'setSecurityImage'
    | 'setSecurityQuestion'
    | 'shameDescribe'
    | 'sharedStories'
    | 'skipLethalMeans'
    | 'skipReason'
    | 'sleepDescribe'
    | 'ssfaFinish'
    | 'ssfAReview'
    | 'stabilityConfidence'
    | 'stabilityRehearsal'
    | 'start'
    | 'stepsDescribe'
    | 'strategiesGeneral'
    | 'suicidalAboutOthers'
    | 'suicidalAboutYourself'
    | 'suicidalDescribe'
    | 'suicidalFreq'
    | 'suicidalLength'
    | 'suicideRisk'
    | 'supportivePeople'
    | 'survivingMakesSense'
    | 'takeCare'
    | 'talkItThrough'
    | 'thanksPlanToCope'
    | 'thankYouMeans'
    | 'timesTriedDescribe'
    | 'viewCard1'
    | 'viewCard2'
    | 'viewCard3'
    | 'viewCard4'
    | 'walkThrough'
    | 'walkThroughVideo'
    | 'warningActions'
    | 'warningFeelings'
    | 'warningStressors'
    | 'warningThoughts'
    | 'welcome'
    | 'whenThingsGetHard'
    | 'willCheckIn'
    | 'wishDie'
    | 'wishLive'
    | 'worseDescribe'
    | 'wsTop';

export type AnswerKeyType =
    | 'abuseYesNo'
    | 'abuseYesNoDescribe'
    | 'burdenOnOthersYesNo'
    | 'burdenOnOthersYesNoDescribe'
    | 'cannotRidMeansDec'
    | 'causesAgitation'
    | 'copingBody'
    | 'copingCourage'
    | 'copingDistract'
    | 'copingHelpOthers'
    | 'copingSenses'
    | 'copingTop'
    | 'crisisDesc'
    | 'currentYesNo'
    | 'currentYesNoDescribe'
    | 'distress0'
    | 'distress1'
    | 'doNotNeedDec'
    | 'feelDepressedDec'
    | 'firearmsYesNo'
    | 'firearmsYesNoDescribe'
    | 'frustration0'
    | 'frustration1'
    | 'healthYesNo'
    | 'healthYesNoDescribe'
    | 'hospitalizedYesNo'
    | 'hospitalizedYesNoDescribe'
    | 'impulsiveYesNo'
    | 'impulsiveYesNoDescribe'
    | 'intentYesNo'
    | 'intentYesNoDescribe'
    | 'jasprRating'
    | 'jasprRecommend'
    | 'keepInHospitalDec'
    | 'keepMeansDec'
    | 'legalYesNo'
    | 'legalYesNoDescribe'
    | 'lengthSuicidalThought'
    | 'lossesYesNo'
    | 'lossesYesNoDescribe'
    | 'meansSupportWho'
    | 'meansSupportYesNo'
    | 'meansWilling'
    | 'meansYesNo'
    | 'meansYesNoDescribe'
    | 'mostHate'
    | 'mostHopeless'
    | 'mostPainful'
    | 'mostStress'
    | 'notSureTalkDec'
    | 'nssiYesNo'
    | 'nssiYesNoDescribe'
    | 'oneThing'
    | 'overallErCare'
    | 'overreactKeepMeDec'
    | 'overreactSpecific'
    | 'overreactTakeAwayDec'
    | 'planYesNo'
    | 'planYesNoDescribe'
    | 'practicedYesNo'
    | 'practicedYesNoDescribe'
    | 'rankFeelings'
    | 'rateAgitation'
    | 'rateHopeless'
    | 'ratePsych'
    | 'rateSelfHate'
    | 'rateStress'
    | 'readiness'
    | 'readinessNo'
    | 'readinessYesChanged'
    | 'readinessYesReasons'
    | 'reasonNotSureTalk'
    | 'reasonsDie'
    | 'reasonsLive'
    | 'relationshipYesNo'
    | 'relationshipYesNoDescribe'
    | 'shameYesNo'
    | 'shameYesNoDescribe'
    | 'skipLethalMeans'
    | 'skipReason'
    | 'sleepYesNo'
    | 'sleepYesNoDescribe'
    | 'stabilityConfidence'
    | 'stabilityRehearsal'
    | 'stableDec'
    | 'stepsYesNo'
    | 'stepsYesNoDescribe'
    | 'strategiesCustom'
    | 'strategiesGeneral'
    | 'strategiesFirearm'
    | 'strategiesMedicine'
    | 'strategiesOther'
    | 'strategiesPlaces'
    | 'suicidalFreq|suicidalFreqUnits'
    | 'suicidalFreq'
    | 'suicidalFreqUnits'
    | 'suicidalOthers'
    | 'suicidalYesNo'
    | 'suicidalYesNoDescribe'
    | 'suicidalYourself'
    | 'suicideRisk'
    | 'supportivePeople'
    | 'timeHere'
    | 'timesTried'
    | 'timesTriedDescribe'
    | 'tooPrivateDec'
    | 'tooShamefulDec'
    | 'walkThrough'
    | 'walkThroughVideo'
    | 'watchTutorialVideo'
    | 'willCheckIn'
    | 'willingToTalk'
    | 'wishDie'
    | 'wishLive'
    | 'worseYesNo'
    | 'worseYesNoDescribe'
    | 'wsActions'
    | 'wsFeelings'
    | 'wsStressors'
    | 'wsThoughts'
    | 'wsTop';


*/

import { actionNames } from 'state/actions/analytics';
import { StaticMedia, StaticMediaVideo } from 'state/types';

export type UIDType = string;
export type AnswerKeyType = string;

export interface ActivateAccountType {
    type: 'activate-account';
}
export interface ActivationCodetype {
    type: 'activation-code';
}
export interface ButtonType {
    type: 'buttons';
    validation?: boolean;
    orientation?: 'vertical' | 'horizontal';
    answerKey?: AnswerKeyType;
    buttons: {
        label: string;
        action?: string;
        path?: string;
        params?: string;
        analyticsAction?: keyof typeof actionNames;
        goto?: string[];
    }[];
}
export interface ChoiceType {
    type: 'choice';
    subtitle?: string;
    options: { label: string; value: boolean | string }[];
    multiple?: boolean;
    vertical?: boolean;
}
export interface ComfortSkillsType {
    type: 'comfort-skills';
}
export interface CopingStrategyType {
    type: 'coping-strategy';
    allowCustom: boolean;
    choices: string[];
    answerKey: AnswerKeyType;
}
export interface CounterType {
    type: 'counter';
    options: { label: string; value: string }[];
    answerKey: AnswerKeyType; // This one is special
    answerKeyUnit: string;
    answerKeyCount: AnswerKeyType;
}
export interface HomeButtonType {
    type: 'homeButton';
}
export interface InfoButtonType {
    type: 'info-modal';
    title: string;
    content: {
        header: string;
        body: string;
    }[];
}
export interface ListType {
    type: 'list';
    rows: number;
    question: string;
    answerKey: AnswerKeyType;
    maxLength: number;
}
export interface ListRankType {
    type: 'list-rank';
    maxLabel: string;
    minLabel: string;
    answerKey: AnswerKeyType;
}
export interface MeansCustomType {
    type: 'means-custom';
    answerKey: AnswerKeyType;
    reviewKeys: { label: string; answerKey: AnswerKeyType }[];
}
export interface RankType {
    type: 'rank';
    answerKey: AnswerKeyType;
    options: {
        title: string;
        question: string;
        subtitle?: string;
        answerKey: string; // This one is special
    }[];
}
export interface RankTopType {
    type: 'rank-top';
    lists: AnswerKeyType[];
    answerKey: AnswerKeyType;
    labels?: string[];
    dropTitle: string;
    targetCount: number;
}
export interface RequestPermissiontype {
    type: 'request-permission';
    permission: 'local authentication';
}
export interface ScaleButtonType {
    type: 'scalebuttons';
    min: number;
    max: number;
    minLabel: string;
    maxLabel: string;
    answerKey: AnswerKeyType;
}
export interface SecurityImageType {
    type: 'security-image';
}
export interface SecurityQuestionType {
    type: 'security-question';
}
export interface SetPasswordType {
    type: 'set-password';
}

export interface PrivacyPolicyQuestionType {
    type: 'privacy-policy';
}

export interface GiveConsentQuestionType {
    type: 'give-consent';
    options: { label: string; value: boolean | string; sublable: string }[];
}

export interface AssessmentLockQuestionType {
    type: 'assessment-lock';
}
export interface SharedStoriesType {
    type: 'shared-stories';
}
export interface SliderType {
    type: 'slider';
    max: number;
    min: number;
    step?: number;
    maxLabel: string; // New line (\n) characters are expected and OK
    minLabel: string; // New line (\n) characters are expected and OK
    answerKey: AnswerKeyType;
}
export interface SlideshowType {
    type: 'slideshow';
    slides: {
        text: string;
        imageUrl: string; // This is currently ignored and needs to be updated when we remove embedded assets
    }[];
}
export interface SortEditType {
    type: 'sort-edit';
    answerKey: AnswerKeyType;
}
export interface StabilityCardType {
    type: 'stability-card';
    empty?: boolean;
}
export interface SupportivePeopleType {
    type: 'supportive-people';
    answerKey: AnswerKeyType;
}
export interface TabChoiceType {
    type: 'tab-choice';
    groups: {
        label: string;
        options: {
            label: string;
            value: string;
        }[];
        answerKey: AnswerKeyType;
    }[];
}
export interface TextType {
    type: 'text';
    label: string;
    answerKey: AnswerKeyType;
    maxLength?: number;
}
export interface UserEmailType {
    type: 'user-email';
}
export interface UserPhonetype {
    type: 'user-phone';
}

export type KeysWithValsOfType<T, V> = keyof { [P in keyof T as T[P] extends V ? P : never]: P };

export type VideoType = {
    // Static Media
    guide?: 'Jasper' | 'Jaz';
    type: 'video';
    name: string;
    mediaKey: KeysWithValsOfType<StaticMedia, StaticMediaVideo>;
    answerKey: AnswerKeyType;
    skippable?: boolean;
};

export interface ProgressBarType {
    type: 'progress-bar';
    label: string;
}

export interface SectionChangeType {
    type: 'section-change';
}

export type ActionType =
    | ActivateAccountType
    | ActivationCodetype
    | ButtonType
    | ChoiceType
    | ComfortSkillsType
    | CopingStrategyType
    | CounterType
    | HomeButtonType
    | InfoButtonType
    | ListType
    | ListRankType
    | MeansCustomType
    | RankType
    | RankTopType
    | RequestPermissiontype
    | ScaleButtonType
    | SecurityImageType
    | SecurityQuestionType
    | PrivacyPolicyQuestionType
    | GiveConsentQuestionType
    | AssessmentLockQuestionType
    | SetPasswordType
    | SharedStoriesType
    | SliderType
    | SlideshowType
    | SortEditType
    | StabilityCardType
    | SupportivePeopleType
    | TabChoiceType
    | TextType
    | UserEmailType
    | UserPhonetype
    | VideoType
    | ProgressBarType
    | SectionChangeType;

export interface Question {
    uid: string;
    guide: string[];
    actions: ActionType[];
    providerOrder?: number;
    providerLabel?: string;
    showIf?: [AnswerKeyType, string]; // This can be removed when the backend only delivers fields that should be shown
    hideIf?: [AnswerKeyType, string]; // This can be removed when the backend only delivers fields that should be shown
}

export type Questions = Question[];

export interface AssignedActivity {
    id: number;
    order?: number;
    created: string;
    startTime: string;
    status: string;
    statusUpdated: string;
    locked: boolean;
    progressBarLabel: null | string;
    type:
        | 'intro'
        | 'stability_plan'
        | 'lethal_means'
        | 'suicide_assessment'
        | 'outro'
        | 'comfort_and_skills';
    questions?: Questions;
    metadata: {
        currentSectionUid?: string;
        scoringScore?: null | 0 | 1 | 2 | 3 | 4 | 5 | 6;
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

export type AssignedActivities = AssignedActivity[];
