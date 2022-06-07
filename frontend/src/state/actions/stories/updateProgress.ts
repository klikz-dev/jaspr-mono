import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { Dispatch } from 'state/types';
import { StoriesConstants } from 'state/constants';
import { PostResponse } from 'state/types/api/patient/patient-videos';
import { PatchResponse } from 'state/types/api/patient/patient-videos/_id';

export const updateProgress = async (
    dispatch: Dispatch,
    id: number | null,
    videoId: number,
    progress: number,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        if (id) {
            dispatch({
                type: StoriesConstants.SAVE_PATIENT_VIDEO,
                videoRating: {
                    video: videoId,
                    progress,
                },
            }); // Speed up UI.  TODO undo if request fails
            const response = await axios.patch<PatchResponse>(
                `${config.apiRoot}/patient/patient-videos/${id}`,
                {
                    progress,
                },
            );
            const json = response.data;
            dispatch({
                type: StoriesConstants.SAVE_PATIENT_VIDEO,
                videoRating: json,
            });
            return response;
        }

        const response = await axios.post<PostResponse>(
            `${config.apiRoot}/patient/patient-videos`,
            {
                video: videoId,
                progress,
            },
        );
        const json = response.data;
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
