import axios from 'axios';
import config from '../../config';
import { MediaConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { GetResponse } from 'state/types/api/static-media';

export const getMedia = async (dispatch: Dispatch) => {
    try {
        const result = await axios.get<GetResponse>(`${config.apiRoot}/static-media`);
        const media = result.data;
        return dispatch({
            type: MediaConstants.SET_MEDIA,
            media,
        });
    } catch (err) {
        console.error(err);
    }
};

export const setFullscreen = (dispatch: Dispatch, isFullScreen: boolean) => {
    return dispatch({ type: MediaConstants.SET_FULLSCREEN, isFullScreen });
};

export const setCaptionsEnabled = (dispatch: Dispatch, captionsEnabled: boolean) => {
    return dispatch({ type: MediaConstants.SET_CAPTIONS_ENABLED, captionsEnabled });
};
