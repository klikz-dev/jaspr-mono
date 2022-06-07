import { UserConstants } from 'state/constants';
import { Dispatch, Patient, AnonymousUser } from 'state/types';

export const setMe = (dispatch: Dispatch, me: Patient | AnonymousUser): void => {
    dispatch({ type: UserConstants.SET_ME, ...me });
};
