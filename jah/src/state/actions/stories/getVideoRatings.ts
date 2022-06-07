import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { Dispatch, VideoRating } from 'state/types';
import { StoriesConstants } from 'state/constants';

export const getVideoRatings = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get(`${config.apiRoot}/patient/patient-videos`);
        const json: VideoRating[] = response.data;
        dispatch({
            type: StoriesConstants.FETCH_PATIENT_VIDEOS, // TODO Rename SET_PATIENT_VIDEOS
            videoRatings: json,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
