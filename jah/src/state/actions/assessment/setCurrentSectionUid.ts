import { UIDType } from 'components/shared/conversational-ui/questions';
import { Dispatch } from 'state/types';
import { AssessmentConstants } from 'state/constants';

export const setCurrentSectionUid = (dispatch: Dispatch, currentSectionUid: UIDType) => {
    return dispatch({
        type: AssessmentConstants.SET_CURRENT_SECTION_UID,
        currentSectionUid,
    });
};
