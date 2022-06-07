import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { Dispatch, Stories } from 'state/types';
import { StoriesConstants } from 'state/constants';

export const getStoriesVideos = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get(`${config.apiRoot}/shared-stories`);
        const json: Stories = response.data;
        dispatch({
            type: StoriesConstants.SET_STORIES,
            stories: json,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
