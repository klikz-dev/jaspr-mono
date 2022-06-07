import Segment from 'lib/segment';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';

// This function only updates email locally in the reducer.
// Actual email is saved through the assesment answer api
export const updateEmail = (dispatch: Dispatch, email: string): void => {
    Segment.track('Email updated');
    dispatch({ type: UserConstants.UPDATE_EMAIL, email });
};
