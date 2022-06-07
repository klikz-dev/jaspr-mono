import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { GetResponse } from 'state/types/api/patient/security-questions';

export const getSecurityQuestion = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get<GetResponse>(
            `${config.apiRoot}/patient/security-questions`,
        );
        const securityQuestion = response.data;
        dispatch({
            type: UserConstants.SET_SECURITY_QUESTIONS,
            securityQuestion,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
