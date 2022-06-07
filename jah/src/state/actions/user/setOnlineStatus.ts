import Segment from 'lib/segment';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';

export const toggleOnline = (dispatch: Dispatch, online: boolean) => {
    if (online) {
        Segment.track('connection-restored'); // TODO Track how long connection was lost
    }

    dispatch({ type: UserConstants.TOGGLE_ONLINE, online });
};
