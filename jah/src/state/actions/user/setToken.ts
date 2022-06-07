import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';

export const setToken = (dispatch: Dispatch, token: string) => {
    return dispatch({
        type: UserConstants.SET_TOKEN,
        token: token,
    });
};
