import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';

export const startAssessmentLockCounter = async (
    dispatch: Dispatch,
    count: number,
): Promise<void> => {
    dispatch({ type: UserConstants.SET_ASSSESSMENT_LOCK_TIMER, assessmentLockTimer: count });
};
