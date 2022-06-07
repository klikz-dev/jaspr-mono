import axios, { AxiosResponse } from 'axios';
import config from '../../../config';
import { DeviceConstants, UserConstants } from 'state/constants';
import Storage from 'lib/storage';
import Sentry from 'lib/sentry';
import { Dispatch } from 'state/types';
import { PostResponse, PostResponseError } from 'state/types/api/technician/login';

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

export const loginAction = async (
    dispatch: Dispatch,
    username: string,
    password: string,
    slug?: string,
): Promise<AxiosResponse<PostResponse | PostResponseError>> => {
    try {
        const params: Params = {
            email: username,
            password,
            fromNative: false,
            longLived: false, // Currently, all native devices are JAH so get a long lived token. That may not be true in the future
        };
        if (slug) {
            params.organizationCode = slug;
        }
        let response;

        response = await axios.post<PostResponse>(`${config.apiRoot}/technician/login`, params);

        const json = response?.data;

        Storage.setSecureItem('token', json.token);

        axios.defaults.headers.common['Authorization'] = `Token ${json.token}`;

        dispatch({
            type: DeviceConstants.SET_DEVICE,
            inPatientContext: false,
            isEhrEmbedded: false,
            patientContextId: null,
        });
        dispatch({
            type: UserConstants.SET_TOKEN,
            token: json.token,
        });

        // @ts-ignore
        dispatch({
            type: UserConstants.SET_ME,
            ...json.technician,
        });

        return response;
    } catch (err) {
        const { response } = err;
        Sentry.captureException(err);
        return { ...response, error: true };
    }
};
