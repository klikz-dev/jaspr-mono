import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { UserConstants } from 'state/constants';
import { Dispatch, PatientPreferences } from 'state/types';

export const getPreferences = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get<PatientPreferences>(
            `${config.apiRoot}/patient/preferences`,
        );

        dispatch({
            type: UserConstants.SET_PREFERENCES,
            ...response.data,
        });

        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
