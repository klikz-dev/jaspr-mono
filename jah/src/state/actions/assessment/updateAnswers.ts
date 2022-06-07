import { AssessmentConstants } from 'state/constants';
import { AssessmentAnswers, Dispatch } from 'state/types';

export const updateAnswers = (dispatch: Dispatch, answers: AssessmentAnswers): void => {
    return dispatch({
        type: AssessmentConstants.UPDATE_ANSWERS,
        answers,
    });
};
