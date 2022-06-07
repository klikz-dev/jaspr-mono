import axios, { AxiosResponse } from 'axios';
import config from '../../../config';
import Segment, { AnalyticNames } from 'lib/segment';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { PostResponse } from 'state/types/api/patient/validate-session';

export const validateSession = async (
    dispatch: Dispatch,
    image: number,
    answer: string,
): Promise<AxiosResponse> => {
    Segment.track(AnalyticNames.SESSION_RESUMED);

    try {
        const response = await axios.post<PostResponse>(
            `${config.apiRoot}/patient/validate-session`,
            {
                image,
                securityQuestionAnswer: answer,
            },
        );
        dispatch({
            type: UserConstants.VALIDATE_SESSION,
        });
        return response;
    } catch (err) {
        const { response } = err;
        return response;
    }
};
