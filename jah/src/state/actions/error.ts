import { ErrorConstants } from 'state/constants';
import { Dispatch } from 'state/types';

export const displayError = (dispatch: Dispatch): void => {
    return dispatch({ type: ErrorConstants.SET_ERROR, showError: true });
};

export const dismissError = (dispatch: Dispatch): void => {
    return dispatch({ type: ErrorConstants.SET_ERROR, showError: false });
};
