import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { GetResponse } from 'state/types/api/me';

export const getMe = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get<GetResponse>(`${config.apiRoot}/me`);
        const json = response.data;

        // @ts-ignore
        dispatch({
            type: UserConstants.SET_ME,
            ...json,
        });

        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
