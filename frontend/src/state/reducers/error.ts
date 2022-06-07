import { ErrorConstants } from 'state/constants';

import { ActionSetError } from 'state/types/actions';

type ErrorReducerType = ActionSetError;

export interface ErrorReducerState {
    showError: boolean;
}

const initialState: ErrorReducerState = { showError: false };

const ErrorReducer = (
    state: ErrorReducerState = initialState,
    action: ErrorReducerType,
): ErrorReducerState => {
    switch (action.type) {
        case ErrorConstants.SET_ERROR:
            return { ...state, showError: action.showError };
        default:
            return state;
    }
};

export { ErrorReducer, initialState };
