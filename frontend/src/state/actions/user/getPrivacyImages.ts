import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { GetResponse } from 'state/types/api/patient/privacy-screen-images';

export const getPrivacyImages = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get<GetResponse>(
            `${config.apiRoot}/patient/privacy-screen-images`,
        );
        const privacyImages = response.data;
        dispatch({
            type: UserConstants.SET_PRIVACY_IMAGES,
            privacyImages,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
