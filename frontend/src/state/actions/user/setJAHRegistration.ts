import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import Segment, { AnalyticNames } from 'lib/segment';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { PostResponse, PostRequest } from 'state/types/api/patient/at-home-setup';

export const setupToolsToGo = async (
    dispatch: Dispatch,
    email: string,
    mobilePhone: string,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));

    Segment.track(AnalyticNames.JAH_SETUP_STARTED);

    try {
        const body: PostRequest = {
            email,
            mobilePhone,
        };
        const response = await axios.post<PostResponse>(
            `${config.apiRoot}/patient/at-home-setup`,
            body,
        );
        dispatch({ type: UserConstants.SETUP_TOOLS_TO_GO, ...response.data });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
