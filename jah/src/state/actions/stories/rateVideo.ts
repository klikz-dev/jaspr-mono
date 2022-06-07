import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { Dispatch, VideoRating } from 'state/types';
import { StoriesConstants } from 'state/constants';

export const rateVideo = async (
    dispatch: Dispatch,
    id: number | null,
    videoId: number,
    rating: number,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        if (id) {
            dispatch({
                type: StoriesConstants.SAVE_PATIENT_VIDEO,
                videoRating: {
                    video: videoId,
                    rating: rating,
                },
            }); // Speed up UI.  TODO undo if request fails
            const response = await axios.patch(`${config.apiRoot}/patient/patient-videos/${id}`, {
                rating,
            });
            const json: VideoRating = response.data;
            dispatch({
                type: StoriesConstants.SAVE_PATIENT_VIDEO,
                videoRating: json,
            });
            return response;
        }

        const response = await axios.post(`${config.apiRoot}/patient/patient-videos`, {
            video: videoId,
            rating,
        });
        const json: VideoRating = response.data;
        dispatch({
            type: StoriesConstants.SAVE_PATIENT_VIDEO,
            videoRating: json,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
