import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import Segment, { AnalyticNames } from 'lib/segment';
import { PatchResponse } from 'state/types/api/me';

export const completeTour = async (
    dispatch: Dispatch,
    saveToServer = true,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    Segment.track(AnalyticNames.TOUR_COMPLETED);
    try {
        // Set this right away to avoid race condition
        dispatch({ type: UserConstants.COMPLETE_TOUR });
        if (saveToServer) {
            const response = await axios.patch<PatchResponse>(`${config.apiRoot}/me`, {
                tourComplete: true,
            });
            return response;
        }
    } catch (err) {
        const { response } = err;
        // No extra error handling
        return response;
    }
};
