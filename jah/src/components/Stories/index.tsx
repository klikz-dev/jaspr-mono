import React, { useEffect, useState, useContext } from 'react';
import Segment from 'lib/segment';
import Sentry from 'lib/sentry';
import StoreContext from 'state/context/store';

import {
    getStoriesVideos,
    getVideoRatings,
    saveStoryForLater,
    rateVideo,
} from 'state/actions/stories';

import TabbedView from './tabbed';
import { Video } from 'state/types';

export interface SelectedStory {
    name: string;
    videos: Video[];
}

const Stories = () => {
    const [store, dispatch] = useContext(StoreContext);
    const { stories, user } = store;
    const { ratingsFetched, storiesFetched, videoRatings, people, topics } = stories;

    const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);
    const [tab, setTab] = useState<'person' | 'topic'>('person');
    const [openThumbnail, setOpenThumbnail] = useState<string | null>(null);
    const [selectedStory, setSelectedStory] = useState<SelectedStory | null>(null);

    useEffect(() => {
        if (!selectedVideo) {
            Segment.track('Video player closed');
        }
    }, [selectedVideo]);

    useEffect(() => {
        if (!storiesFetched) {
            getStoriesVideos(dispatch);
        }
        if (!ratingsFetched) {
            getVideoRatings(dispatch);
        }
    }, [dispatch, ratingsFetched, storiesFetched]);

    const videoRating = videoRatings.find(
        (rating) => rating.video === (selectedVideo ? selectedVideo.id : null),
    );

    const rate = (rating: 0 | 1 | 2 | 3 | 4 | 5) => {
        const id = videoRating ? videoRating.id : null;
        if (selectedVideo?.id) {
            const videoId = selectedVideo.id;
            rateVideo(dispatch, id || null, videoId, rating);
        }
    };

    // TODO: For these two functions below, we might want to check if the
    // patient videos have been fully loaded first.
    const save = () => {
        const id = videoRating ? videoRating.id : null;
        const saveForLater = videoRating ? videoRating.saveForLater : false;
        if (selectedVideo?.id) {
            const videoId = selectedVideo.id;
            saveStoryForLater(dispatch, id || null, videoId, !saveForLater);
        }
    };

    const getTopicLabel = (name: string): string => {
        try {
            return name.split('-')[0];
        } catch {
            Sentry.captureMessage(`video tag ${name} is nor formatted correctly.`);
            return name;
        }
    };

    const getPersonLabel = (name: string): string => {
        try {
            return name.split('-')[1];
        } catch {
            Sentry.captureMessage(`video tag ${name} is nor formatted correctly.`);
            return name;
        }
    };

    return (
        <TabbedView
            people={people}
            topics={topics}
            selectedVideo={selectedVideo}
            setSelectedVideo={setSelectedVideo}
            tab={tab}
            setTab={setTab}
            setOpenThumbnail={setOpenThumbnail}
            save={save}
            rate={rate}
            getPersonLabel={getPersonLabel}
            getTopicLabel={getTopicLabel}
            selectedStory={selectedStory}
            setSelectedStory={setSelectedStory}
            videoRating={videoRating}
        />
    );
};

export default Stories;
