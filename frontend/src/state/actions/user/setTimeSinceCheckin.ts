import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';

export const saveTimeSinceCheckin = (
    dispatch: Dispatch,
    timeSinceCheckin: number, // Minutes
) => {
    dispatch({ type: UserConstants.SET_TIME_SINCE_CHECKIN, timeSinceCheckin });
};
