import { AssessmentConstants } from 'state/constants';
import { AssessmentAnswers, Walkthrough } from 'state/types';
import { Questions, UIDType } from 'components/ConversationalUi/questions';
import {
    ActionSetQuestions,
    ActionSetAssessment,
    ActionUpdateAnswers,
    ActionSetAnswer,
    ActionSetCurrentSectionUid,
    ActionSetWalkthrough,
} from 'state/types/actions';

type AssessmentReducerType =
    | ActionSetQuestions
    | ActionSetAssessment
    | ActionUpdateAnswers
    | ActionSetAnswer
    | ActionSetCurrentSectionUid
    | ActionSetWalkthrough;

export interface AssessmentReducerState {
    currentAssessment: number | null;
    currentSectionUid: UIDType;
    assessmentFinished: boolean;
    assessmentLocked: boolean;
    assessmentLockedAcknowledged: boolean;
    ssid: string | null;
    answers: Partial<AssessmentAnswers>;
    walkthrough: Walkthrough;
    questions: Questions;
}

const initialState: AssessmentReducerState = {
    currentAssessment: null,
    currentSectionUid: 'ratePsych',
    assessmentFinished: false,
    assessmentLocked: false,
    assessmentLockedAcknowledged: true,
    ssid: null,
    answers: {},
    walkthrough: [],
    questions: [],
};

const AssessmentReducer = (
    state: AssessmentReducerState = initialState,
    action: AssessmentReducerType,
): AssessmentReducerState => {
    switch (action.type) {
        case AssessmentConstants.SET_QUESTIONS:
            return {
                ...state,
                questions: action.questions,
            };
        case AssessmentConstants.SET_ASSESSMENT:
            return {
                ...state,
                currentAssessment: action.currentAssessment,
                currentSectionUid: action.currentSectionUid,
                assessmentFinished: action.assessmentFinished,
                assessmentLocked: action.assessmentLocked,
                assessmentLockedAcknowledged: action.assessmentLockedAcknowledged,
                ssid: action.ssid || null,
                answers: action.answers,
            };
        case AssessmentConstants.UPDATE_ANSWERS:
            return {
                ...state,
                answers: { ...state.answers, ...action.answers },
            };
        case AssessmentConstants.SET_ANSWERS:
            return {
                ...state,
                currentSectionUid: action.currentSectionUid || state.currentSectionUid,
                assessmentFinished: action.assessmentFinished,
                answers: { ...state.answers, ...action.answers },
            };
        case AssessmentConstants.SET_CURRENT_SECTION_UID:
            return {
                ...state,
                currentSectionUid: action.currentSectionUid,
            };
        case AssessmentConstants.SET_WALKTHROUGH:
            return { ...state, walkthrough: action.walkthrough };
        default:
            return state;
    }
};

export { AssessmentReducer, initialState };
