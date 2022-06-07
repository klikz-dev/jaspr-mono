import axios, { AxiosResponse } from 'axios';
import Sentry from 'lib/sentry';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { AssessmentConstants } from 'state/constants';
import { Assessment, AssessmentAnswers, Dispatch } from 'state/types';

export const saveAnswers = async (
    dispatch: Dispatch,
    newAnswers: Partial<AssessmentAnswers>,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    // Set answers in store so they are immediately available
    // TODO If request fails - we need to revert this.  Save a copy of the
    // previous answers being set and restore on failure
    dispatch({
        type: AssessmentConstants.UPDATE_ANSWERS,
        answers: newAnswers,
    });
    try {
        const response = await axios.patch(`${config.apiRoot}/patient/answers`, newAnswers);
        const json: Assessment & AssessmentAnswers & { id: number } = response.data;

        const { id, assessmentFinished, ssid, currentSectionUid, ...answers } = json;

        dispatch({
            type: AssessmentConstants.SET_ANSWERS,
            assessmentFinished,
            answers,
        });
        return response;
    } catch (err) {
        const { response } = err;
        const json = response.data;
        if (response.status === 400) {
            // Log on development for easier debugging assessment issues
            if (process.env.environment !== 'production') {
                Sentry.captureException(JSON.stringify(json));
            }
            // No extra error handling
        }
        return response;
    }
};
