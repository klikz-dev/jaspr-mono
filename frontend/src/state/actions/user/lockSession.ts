import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import Segment, { AnalyticNames } from 'lib/segment';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { PostResponse } from 'state/types/api/patient/session-lock';

export const lockSession = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    Segment.track(AnalyticNames.SESSION_LOCKED);
    try {
        const response = await axios.post<PostResponse>(
            `${config.apiRoot}/patient/session-lock`,
            {},
        );
        dispatch({
            type: UserConstants.LOCK_SESSION,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
