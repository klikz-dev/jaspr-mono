import { UserConstants } from 'state/constants';
import { Dispatch, Patient, AnonymousUser } from 'state/types';

export const updateMe = (
    dispatch: Dispatch,
    userType: 'patient' | '',
    me: Partial<Patient> | Partial<AnonymousUser>,
): void => {
    // @ts-ignore
    dispatch({ type: UserConstants.UPDATE_ME, ...me, userType });
};
