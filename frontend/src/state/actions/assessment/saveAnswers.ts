import axios, { AxiosResponse } from 'axios';
import Sentry from 'lib/sentry';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { AssessmentConstants } from 'state/constants';
import { AssessmentAnswers, Dispatch } from 'state/types';
import { PatchResponse } from 'state/types/api/patient/answers';

export const saveAnswers = async (
    dispatch: Dispatch,
    newAnswers: Partial<AssessmentAnswers>,
    isTakeaway: boolean = false,
    activityId: number = null,
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
        const response = await axios.patch<PatchResponse>(
            `${config.apiRoot}/patient/answers${isTakeaway ? '?takeaway=true' : ''}${
                activityId ? `?activity=${activityId}` : ''
            }`,
            newAnswers,
        );
        const json = response.data;

        const answers = json.answers;

        dispatch({
            type: AssessmentConstants.SET_ANSWERS,
            answers,
        });
        return response;
    } catch (err) {
        const { response } = err;
        const json = response.data;
        if (response.status === 400) {
            if (process.env.environment !== 'production') {
                // Log on development for easier debugging assessment issues
                Sentry.captureException(JSON.stringify(json));
            }
            // No extra error handling
        } else {
            Sentry.captureException(err);
        }
        return response;
    }
};
