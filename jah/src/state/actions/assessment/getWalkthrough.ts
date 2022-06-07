import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { AssessmentConstants } from 'state/constants';
import { Dispatch } from 'state/types';

export const getWalkthrough = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get(`${config.apiRoot}/patient/walkthrough`);
        const json = response.data;
        dispatch({ type: AssessmentConstants.SET_WALKTHROUGH, walkthrough: json });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
