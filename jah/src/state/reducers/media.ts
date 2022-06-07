import { MediaConstants } from 'state/constants';
import { StaticMedia } from 'state/types/media';
import { ActionSetCaptionsEnabled, ActionSetFullscreen, ActionSetMedia } from 'state/types/actions';

export interface MediaReducerState {
    isFullScreen: boolean;
    media: StaticMedia;
    captionsEnabled: boolean;
}

export type MediaReducerType = ActionSetFullscreen | ActionSetMedia | ActionSetCaptionsEnabled;

const initialMedia = {
    dash: '',
    hls: '',
    poster: '',
    video: '',
};

const initialState: MediaReducerState = {
    isFullScreen: false,
    captionsEnabled: true,
    media: {
        intro: initialMedia,
        expect: initialMedia,
        tutorialJasper: initialMedia,
        tutorialJaz: initialMedia,
        nationalHotline: initialMedia,
        crisisLines: initialMedia,
        crisisLinesExpect: initialMedia,
        supportivePeople: initialMedia,
        copingStrategies: initialMedia,
        reasonsLive: initialMedia,
        saferHome: initialMedia,
        warningSignals: initialMedia,
        mediaUrl: '',
        sampleGuide: {
            Jasper: '',
            Jaz: '',
        },
    },
};

const MediaReducer = (
    state: MediaReducerState = initialState,
    action: MediaReducerType,
): MediaReducerState => {
    switch (action.type) {
        case MediaConstants.SET_FULLSCREEN:
            return { ...state, isFullScreen: action.isFullScreen };
        case MediaConstants.SET_MEDIA:
            return { ...state, media: action.media };
        case MediaConstants.SET_CAPTIONS_ENABLED:
            return { ...state, captionsEnabled: action.captionsEnabled };
        default:
            return state;
    }
};

export { MediaReducer, initialState };
