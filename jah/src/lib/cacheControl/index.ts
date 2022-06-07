import { useContext, useEffect } from 'react';
import { Image } from 'react-native';
import StoreContext from 'state/context/store';
import { getStoriesVideos, getVideoRatings } from 'state/actions/stories';
import { getSkills } from 'state/actions/skills';
import { getWalkthrough } from 'state/actions/assessment';

const CacheControl = (): null => {
    const [store, dispatch] = useContext(StoreContext);
    const { assessment, skills, stories, user } = store;
    const { videos } = stories;
    const { walkthrough } = assessment;
    const { authenticated, userType } = user;
    useEffect(() => {
        if (authenticated && userType === 'patient') {
            getStoriesVideos(dispatch);
            getVideoRatings(dispatch);
            getSkills(dispatch);
            getWalkthrough(dispatch);
        }
    }, [authenticated, dispatch, userType]);

    useEffect(() => {
        const urls: Array<string> = [];
        // @ts-ignore
        walkthrough.forEach((step) => {
            if (['videoDescription', 'video'].includes(step.frontendRenderType)) {
                if (step?.value?.poster) {
                    urls.push(step.value.poster);
                }
            } else if (step.frontendRenderType === 'copingStrategy') {
                if (step?.value?.image) {
                    urls.push(step.value.image);
                }
            }
        });
        Image.queryCache(urls).then((result) => {
            urls.forEach((url) => {
                if (!result[url]) {
                    Image.prefetch(url);
                }
            });
        });
    }, [walkthrough]);

    useEffect(() => {
        const urls = Array.from(
            new Set(videos.filter((video) => video.thumbnail).map((video) => video.thumbnail)),
        );

        Image.queryCache(urls).then((result) => {
            urls.forEach((url) => {
                if (!result[url]) {
                    Image.prefetch(url);
                }
            });
        });
    }, [videos]);

    useEffect(() => {
        const urls = Array.from(
            new Set(
                skills.filter((skill) => skill.thumbnailImage).map((skill) => skill.thumbnailImage),
            ),
        );
        Image.queryCache(urls).then((result) => {
            urls.forEach((url) => {
                if (!result[url]) {
                    Image.prefetch(url);
                }
            });
        });
    }, [skills]);

    return null;
};

export default CacheControl;
