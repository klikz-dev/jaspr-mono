import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { UserConstants } from 'state/constants';
import { Dispatch, Patient } from 'state/types';

import Segment from 'lib/segment';

export const getMe = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get(`${config.apiRoot}/me`);
        const { analyticsToken, userType, clinic, role } = response.data;
        const json: Patient = response.data;
        dispatch({
            type: UserConstants.SET_ME,
            ...json,
        });

        Segment.identify(analyticsToken, {
            userType,
            clinic,
            role,
        });

        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
