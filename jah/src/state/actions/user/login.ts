import axios, { AxiosResponse } from 'axios';
import config from 'config';
import { DeviceConstants, UserConstants } from 'state/constants';
import Storage from 'lib/storage';
import * as Sentry from 'sentry-expo';
import { Dispatch, Patient } from 'state/types';

export const validateLogin = (username: string, password: string) => {
    if (username.length < 1) {
        return 'Please enter your email';
    } else if (password.length < 1) {
        return 'Please enter your password';
    }
    return false;
};

interface Params {
    email: string;
    password: string;
    fromNative: boolean;
    longLived: boolean;
    organizationCode?: string;
}

interface ErrorResponse {
    nonFieldErrors?: Array<string>;
    email?: Array<string>;
    password?: Array<string>;
    detail?: Array<string>;
    error: true;
}

interface SuccessResponse {
    token: string;
    patient: Patient;
}

export const loginAction = async (
    dispatch: Dispatch,
    username: string,
    password: string,
): Promise<AxiosResponse<SuccessResponse | ErrorResponse>> => {
    try {
        const params: Params = {
            email: username,
            password,
            fromNative: true,
            longLived: true, // Currently, all native devices are JAH so get a long lived token. That may not be true in the future
        };

        const response = await axios.post(`${config.apiRoot}/patient/login`, params);

        const json: {
            token: string;
            patient: Patient;
        } = response?.data;

        Storage.setSecureItem('token', json.token);

        axios.defaults.headers.common['Authorization'] = `Token ${json.token}`;
        const meDispatch = json.patient;
        Storage.setSecureItem('userType', 'patient');

        dispatch({
            type: DeviceConstants.SET_DEVICE,
            inPatientContext: false,
            isEhrEmbedded: false,
        });
        dispatch({
            type: UserConstants.SET_TOKEN,
            token: json.token,
        });
        dispatch({
            type: UserConstants.SET_ME,
            ...meDispatch,
        });

        return response;
    } catch (err) {
        const { response } = err;
        Sentry.Native.captureException(err);
        return { ...response, error: true };
    }
};
