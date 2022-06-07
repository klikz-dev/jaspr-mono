import { AssessmentConstants } from 'state/constants';
import { AssessmentAnswers, Walkthrough } from 'state/types';
import {
    AssignedActivities,
    AssignedActivity,
    Questions,
    UIDType,
} from 'components/ConversationalUi/questions';
import {
    ActionSetQuestions,
    ActionSetAssessment,
    ActionSetActivities,
    ActionUpdateAnswers,
    ActionSetAnswer,
    ActionUpdateActivities,
    ActionSetCurrentSectionUid,
    ActionSetWalkthrough,
} from 'state/types/actions';

type AssessmentReducerType =
    | ActionSetQuestions
    | ActionSetAssessment
    | ActionSetActivities
    | ActionUpdateActivities
    | ActionUpdateAnswers
    | ActionSetAnswer
    | ActionSetCurrentSectionUid
    | ActionSetWalkthrough;

export interface AssessmentReducerState {
    currentAssessment: number | null;
    currentSectionUid: UIDType;
    assessmentLocked: boolean;
    //assessmentLockedBy: 'patient' | 'technician' | null;
    //assessmentLockedAcknowledged: boolean;
    ssid: string | null;
    answers: Partial<AssessmentAnswers>;
    walkthrough: Walkthrough;
    questions: Questions;
    activities: AssignedActivities;
}

const initialState: AssessmentReducerState = {
    currentAssessment: null,
    currentSectionUid: 'ratePsych',
    assessmentLocked: false,
    //assessmentLockedBy: null,
    //assessmentLockedAcknowledged: true,
    activities: [],
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
        case AssessmentConstants.SET_ACTIVITIES:
            return {
                ...state,
                activities: action.activities,
                assessmentLocked: action.activities
                    .filter((activity) =>
                        ['stability_plan', 'suicide_assessment', 'outro'].includes(activity.type),
                    )
                    .every((activity: AssignedActivity) => activity.locked),
            };
        case AssessmentConstants.UPDATE_ACTIVITIES:
            return {
                ...state,
                // Note, map function is duplicated below for assessmentLocked property
                activities: state.activities.map((activity: AssignedActivity) => {
                    if (activity.id === action.activity.id) {
                        return action.activity;
                    }
                    return activity;
                }),
                assessmentLocked: state.activities
                    .map((activity: AssignedActivity) => {
                        if (activity.id === action.activity.id) {
                            return action.activity;
                        }
                        return activity;
                    })
                    .filter((activity) =>
                        ['stability_plan', 'suicide_assessment', 'outro'].includes(activity.type),
                    )
                    .every((activity: AssignedActivity) => activity.locked),
            };
        case AssessmentConstants.SET_ASSESSMENT:
            return {
                ...state,
                currentAssessment: action.currentAssessment,
                currentSectionUid: action.currentSectionUid,
                assessmentLocked: state.assessmentLocked,
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
                currentSectionUid:
                    action.currentSectionUid !== undefined
                        ? action.currentSectionUid
                        : state.currentSectionUid,
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
