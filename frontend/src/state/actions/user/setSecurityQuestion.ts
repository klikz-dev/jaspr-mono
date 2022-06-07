import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import Segment, { AnalyticNames } from 'lib/segment';
import { PostResponse } from 'state/types/api/patient/security-questions';
import { PatchResponse } from 'state/types/api/patient/security-questions/_id';

const saveNewSecurityQuestion = async (
    dispatch: Dispatch,
    question: string,
    answer: string,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));

    try {
        // Set this right away to avoid race condition
        dispatch({ type: UserConstants.SAVE_SECURITY_QUESTION });
        const response = await axios.post<PostResponse>(
            `${config.apiRoot}/patient/security-questions`,
            {
                question,
                answer,
            },
        );
        Segment.track(AnalyticNames.SECURITY_QUESTION_SET, { question });
        return response;
    } catch (err) {
        const { response } = err;
        // No extra error handling
        return response;
    }
};

const updateExistingSecurityQuestion = async (
    dispatch: Dispatch,
    id: number,
    question: string,
    answer: string,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));

    try {
        // Needs to update before the POST so patient gets routed correctly
        dispatch({ type: UserConstants.SAVE_SECURITY_QUESTION });
        const response = await axios.patch<PatchResponse>(
            `${config.apiRoot}/patient/security-questions/${id}`,
            {
                question,
                answer,
            },
        );
        return response;
    } catch (err) {
        const { response } = err;
        // No extra error handling
        return response;
    }
};

export const saveSecurityQuestion = async (
    dispatch: Dispatch,
    id: number | null,
    question: string,
    answer: string,
): Promise<AxiosResponse> => {
    // Needs to update before the POST so patient gets routed correctly
    dispatch({ type: UserConstants.SAVE_SECURITY_QUESTION });
    if (id) {
        return updateExistingSecurityQuestion(dispatch, id, question, answer);
    } else {
        return saveNewSecurityQuestion(dispatch, question, answer);
    }
};
