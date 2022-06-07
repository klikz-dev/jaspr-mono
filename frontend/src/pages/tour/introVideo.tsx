import { useContext } from 'react';
import Video from 'pages/tour/shared/video-page';
import StoreContext from 'state/context/store';

const IntroVideo = () => {
    const [store] = useContext(StoreContext);
    const { media } = store.media;
    const { intro } = media;
    const { video, dash, hls, poster } = intro;

    return (
        <Video
            poster={poster}
            dashPlaylist={dash}
            hlsPlaylist={hls}
            mp4Transcode={video}
            nextPage="/baseline"
            noSkip
        />
    );
};

export default IntroVideo;
