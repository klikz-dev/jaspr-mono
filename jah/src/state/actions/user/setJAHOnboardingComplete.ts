import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import Segment from 'lib/segment';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';

export const completedJAHOnboarding = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    dispatch({ type: UserConstants.COMPLETE_JAH_ONBOARDING });
    Segment.track('JAH Onboarding Complete');

    try {
        const response = await axios.patch(`${config.apiRoot}/me`, {
            onboarded: true,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
