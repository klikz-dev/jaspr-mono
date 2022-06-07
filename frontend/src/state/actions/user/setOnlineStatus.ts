import Segment, { AnalyticNames } from 'lib/segment';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';

export const toggleOnline = (dispatch: Dispatch, online: boolean, secondsOffline: number = 0) => {
    if (online) {
        Segment.track(AnalyticNames.CONNECTION_RESTORED, { secondsOffline });
    } else {
        Segment.track(AnalyticNames.CONNECTION_LOST);
    }

    dispatch({ type: UserConstants.TOGGLE_ONLINE, online });
};
