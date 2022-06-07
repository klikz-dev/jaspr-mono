import { UserConstants } from 'state/constants';
import { Dispatch, Technician, Patient, AnonymousUser } from 'state/types';

export const updateMe = (
    dispatch: Dispatch,
    userType: 'patient' | 'technician' | '',
    me: Partial<Patient> | Partial<Technician> | Partial<AnonymousUser>,
): void => {
    // @ts-ignore
    dispatch({ type: UserConstants.UPDATE_ME, ...me, userType });
};
