import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import Segment, { AnalyticNames } from 'lib/segment';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { PatchResponse } from 'state/types/api/me';

export const selectGuide = async (
    dispatch: Dispatch,
    guide: 'Jaz' | 'Jasper',
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    dispatch({ type: UserConstants.SET_GUIDE, guide });
    Segment.track(AnalyticNames.GUIDE_SELECTED, { guide });

    try {
        const response = await axios.patch<PatchResponse>(`${config.apiRoot}/me`, {
            guide,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
