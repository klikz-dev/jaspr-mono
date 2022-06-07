import { UserConstants } from 'state/constants';
import { Dispatch, Technician, Patient, AnonymousUser } from 'state/types';

export const setMe = (dispatch: Dispatch, me: Patient | Technician | AnonymousUser): void => {
    dispatch({ type: UserConstants.SET_ME, ...me });
};
