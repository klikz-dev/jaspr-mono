import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { AssessmentConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { GetResponse } from 'state/types/api/patient/interview';

export const getQuestions = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));

    try {
        const response = await axios.get<GetResponse>(`${config.apiRoot}/patient/interview`);
        const json = response.data;
        dispatch({ type: AssessmentConstants.SET_ACTIVITIES, activities: json });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
