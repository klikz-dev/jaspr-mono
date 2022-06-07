import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { AssessmentConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { GetResponse } from 'state/types/api/patient/answers';

export const getAnswers = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get<GetResponse>(`${config.apiRoot}/patient/answers`);
        const json = response.data;
        const currentSectionUid = json.metadata.currentSectionUid;
        const answers = { ...json.answers, ...json.metadata };

        dispatch({
            type: AssessmentConstants.SET_ANSWERS,
            currentSectionUid,
            answers,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
