import { PixelRatio } from 'react-native';
import { StoriesConstants } from 'state/constants';
import { Video, VideoRatings, Stories, VideoRating } from 'state/types';

import {
    ActionSetStories,
    ActionSetStoriesFetching,
    ActionFetchPatientVideos,
    ActionSavePatientVideo,
} from 'state/types/actions';

const getPixelRatio = (): 1 | 2 | 3 => {
    const pixelRatio = PixelRatio.get();
    if (pixelRatio <= 1) {
        return 1;
    }
    if (pixelRatio <= 2) {
        return 2;
    }
    if (pixelRatio > 2) {
        return 3;
    }
    return 1;
};

export interface StoriesReducerState {
    people: {
        id: number;
        labelColor: string; // TODO Remove
        name: string;
        order: number;
        thumbnail: string;
        videos: Video[];
    }[];
    topics: {
        id: number;
        labelColor: string; // TODO Remove
        name: string;
        order: number;
        videos: Video[];
    }[];
    videos: Video[];
    tags: { [tag: string]: Video[] };
    storiesFetched: boolean;
    ratingsFetched: boolean;
    videoRatings: VideoRatings;
}

export type StoriesReducerType =
    | ActionSetStories
    | ActionSetStoriesFetching
    | ActionFetchPatientVideos
    | ActionSavePatientVideo;

const initialState: StoriesReducerState = {
    people: [],
    topics: [],
    videos: [],
    tags: {},
    storiesFetched: false,
    ratingsFetched: false,
    videoRatings: [],
};

const saveForLater = (videoRatings: VideoRatings, videoRating: VideoRating) => {
    const newVideoRatings = [...videoRatings];
    const { video, rating, saveForLater, viewed } = videoRating;
    const idx = newVideoRatings.findIndex((vid) => vid.video === video);

    if (idx > -1) {
        newVideoRatings[idx] = {
            ...newVideoRatings[idx],
            progress: videoRating?.progress || 0,
            rating: rating !== undefined ? rating : newVideoRatings[idx].rating,
            saveForLater:
                saveForLater !== undefined ? saveForLater : newVideoRatings[idx].saveForLater,
            viewed,
        };
    } else {
        newVideoRatings.push(videoRating);
    }
    return newVideoRatings;
};

const organizeStories = (
    state: StoriesReducerState,
    stories: Stories = [],
): StoriesReducerState => {
    const people = stories
        .map((story) => {
            const { image1x, image2x, image3x, ...rest } = story.person;
            return {
                ...rest,
                thumbnail:
                    story.person[`image${getPixelRatio()}x` as 'image1x' | 'image2x' | 'image3x'],
                videos: [],
            };
        })
        .filter((item, pos, self) => self.findIndex((person) => person.id === item.id) === pos)
        .sort((a, b) => a.order - b.order);

    const topics = stories
        .map((story) => ({ ...story.topic, videos: [] }))
        .filter((item, pos, self) => self.findIndex((topic) => topic.id === item.id) === pos)
        .sort((a, b) => a.order - b.order);

    const videos = stories.map((story) => ({
        ...story.video,
        thumbnail:
            story.video.thumbnail ||
            story.person[`image${getPixelRatio()}x` as 'image1x' | 'image2x' | 'image3x'],
    }));

    stories.forEach((story) => {
        const person = people.find((person) => story.person.id === person.id);
        if (person) {
            //@ts-ignore TODO
            person.videos = [...person.videos, story.video];
        }

        const topic = topics.find((topic) => story.topic.id === topic.id);
        if (topic) {
            //@ts-ignore TODO
            topic.videos = [...topic.videos, story.video];
        }
    });
    return { ...state, people, topics, videos, storiesFetched: true };
};

const StoriesReducer = (
    state: StoriesReducerState = initialState,
    action: StoriesReducerType,
): StoriesReducerState => {
    switch (action.type) {
        case StoriesConstants.SET_STORIES:
            return organizeStories(state, action.stories);
        case StoriesConstants.SET_STORIES_FETCHING:
            return { ...state, storiesFetched: true };
        case StoriesConstants.FETCH_PATIENT_VIDEOS:
            return { ...state, videoRatings: action.videoRatings, ratingsFetched: true };
        case StoriesConstants.SAVE_PATIENT_VIDEO:
            return { ...state, videoRatings: saveForLater(state.videoRatings, action.videoRating) };
        default:
            return state;
    }
};

export { StoriesReducer, initialState };
