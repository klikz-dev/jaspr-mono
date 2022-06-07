import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { Dispatch } from 'state/types';
import Segment, { AnalyticNames } from 'lib/segment';
import { PatchResponse } from 'state/types/api/patient/privacy-screen-image';

export const setSecurityImage = async (dispatch: Dispatch, id: number): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));

    try {
        const response = await axios.patch<PatchResponse>(
            `${config.apiRoot}/patient/privacy-screen-image`,
            {
                privacyScreenImage: id,
            },
        );
        Segment.track(AnalyticNames.SECURITY_IMAGE_SET, { imageId: id });
        return response;
    } catch (err) {
        const { response } = err;
        // No extra error handling
        return response;
    }
};
