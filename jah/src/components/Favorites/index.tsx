import React, { useContext, useEffect } from 'react';
import StoreContext from 'state/context/store';
import { getSkills } from 'state/actions/skills';
import { getVideoRatings, getStoriesVideos } from 'state/actions/stories';
import VideoLink from 'components/VideoLink';

const Favorites = (): JSX.Element | null => {
    const [store, dispatch] = useContext(StoreContext);
    const { stories, skills } = store;
    const { videoRatings, videos } = stories;
    const { storiesFetched, ratingsFetched } = stories;

    useEffect(() => {
        if (!storiesFetched) {
            getStoriesVideos(dispatch);
        }
        if (!ratingsFetched) {
            getVideoRatings(dispatch);
        }
        if (skills.length === 0) {
            getSkills(dispatch);
        }
    }, [dispatch, ratingsFetched, storiesFetched, skills.length]);

    const favoriteStory = videos.find((video) => {
        return videoRatings
            .filter((videoRating) => videoRating.saveForLater)
            .find((videoRating) => videoRating.video === video.id);
    });

    const favoriteSkill = skills.find((skill) => skill.saveForLater);
    if (favoriteStory) {
        return <VideoLink {...favoriteStory} />;
    }
    if (favoriteSkill) {
        return (
            <VideoLink
                {...favoriteSkill.video}
                thumbnail={favoriteSkill.thumbnailImage || favoriteSkill?.video?.thumbnail || null}
            />
        );
    }
    // TODO Breathe app or other future not video skill favorites
    return null;
};

export default Favorites;
