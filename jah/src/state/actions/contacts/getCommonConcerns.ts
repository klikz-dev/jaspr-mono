import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { ContactsConstants } from 'state/constants';
import { CommonConcern, Dispatch } from 'state/types';

type CommonConcerns = CommonConcern[];

export const getCommonConcerns = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get(`${config.apiRoot}/common-concerns`);
        const json: CommonConcerns = response.data;
        dispatch({
            type: ContactsConstants.SET_COMMON_CONCERNS,
            concerns: json,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
