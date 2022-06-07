import { useCallback, useContext, useRef, useState } from 'react';
import StoreContext from 'state/context/store';
import styles from './index.module.scss';
import PlayButton from 'assets/PlayButton.png';
import { QuestionProps } from '../../question';
import { StaticMediaVideo, StaticMedia } from 'state/types';
import { KeysWithValsOfType } from '../../questions';

type VideoQuestionProps = Pick<QuestionProps, 'next' | 'setAnswered' | 'answered'> & {
    dashPlaylist?: string;
    hlsPlaylist?: string;
    mp4Transcode?: string;
    name?: string;
    poster?: string;
    mediaKey?: keyof StaticMedia; // TODO Not every key is media.  Need to subset
    skippable?: boolean;
};

const VideoQuestion = (props: VideoQuestionProps): JSX.Element => {
    const {
        next,
        setAnswered,
        answered,
        skippable = true,
        mediaKey,
        dashPlaylist,
        hlsPlaylist,
        mp4Transcode,
        poster: sourcePoster,
    } = props;
    const [showPoster, setShowPoster] = useState(true);
    const [store] = useContext(StoreContext);
    const { media } = store.media;
    let mediaContent: StaticMedia | StaticMediaVideo = {} as StaticMedia;
    if (media[mediaKey]) {
        mediaContent = (media[mediaKey] || {}) as StaticMedia[KeysWithValsOfType<
            StaticMedia,
            StaticMediaVideo
        >];
    } else {
        mediaContent = {
            dash: dashPlaylist,
            hls: hlsPlaylist,
            video: mp4Transcode,
            poster: sourcePoster,
        };
    }

    const { dash, hls, poster, video } = mediaContent;
    const videoEl = useRef<HTMLVideoElement>(null!);
    const goFullScreen = () => {
        if (videoEl.current.requestFullscreen) {
            videoEl.current.requestFullscreen();
            // @ts-ignore
        } else if (videoEl.current.webkitRequestFullscreen) {
            // @ts-ignore
            videoEl.current.webkitRequestFullscreen();
            // @ts-ignore
        } else if (videoEl.current.mozRequestFullScreen) {
            // @ts-ignore
            videoEl.current.mozRequestFullScreen();
            // @ts-ignore
        } else if (videoEl.current.msRequestFullscreen) {
            // @ts-ignore
            videoEl.current.msRequestFullscreen();
        }
    };

    // TODO Fix with EBPI-1190
    const exitFullScreen = () => {
        if (document.fullscreenElement && document.exitFullscreen) {
            document.exitFullscreen();
            // TODO Remove when IE11 Support is dropped
            // @ts-ignore
        } else if (document.msFullScreenElement && document.msExitFullscreen) {
            // @ts-ignore
            document.msExitFullscreen();
            // @ts-ignore
        } else if (videoEl.current.exitFullscreen) {
            // @ts-ignore
            videoEl.current.exitFullscreen();
            // @ts-ignore
        } else if (videoEl.current.webkitExitFullscreen) {
            // @ts-ignore
            videoEl.current.webkitExitFullscreen();
        }
    };

    const videoEnded = () => {
        exitFullScreen();
        setShowPoster(true);
        if (!answered) {
            window.setTimeout(() => {
                setAnswered(true);
                next();
            }, 750); // Wait for full screen to exit before.  TODO Use onfullscreenchange event and requestanimationframe to fire this as soon as ready */
        }
    };

    const playVideo = useCallback(() => {
        goFullScreen();
        setShowPoster(false);
        setTimeout(() => {
            if (videoEl.current) videoEl.current.play();
        }, 0);
    }, []);

    const checkAndPlayVideo = useCallback(() => {
        if (showPoster) {
            playVideo();
        }
    }, [playVideo, showPoster]);

    const skip = () => {
        if (videoEl.current) videoEl.current.pause();
        setShowPoster(true);
        setAnswered(true);
        next();
    };

    return (
        <div className={styles.container}>
            <div className={styles.video} onClick={checkAndPlayVideo}>
                <video
                    key={hls + dash + video}
                    data-dashjs-player="data-dashjs-player"
                    ref={videoEl}
                    style={{ opacity: showPoster ? 0 : 1 }}
                    controls
                    disablePictureInPicture
                    onEnded={videoEnded}
                    onPlay={() => showPoster && setShowPoster(false)}
                >
                    <source type="application/vnd.apple.mpegurl" src={hls} />
                    <source type="video/mp4" src={video} />
                </video>
                {showPoster && (
                    <>
                        <img className={styles.poster} alt="Play video" src={poster} />
                        <img
                            alt="Play video"
                            src={PlayButton}
                            style={{ zIndex: 1, width: '114px' }}
                        />
                    </>
                )}
            </div>
            {!answered && skippable && (
                <div className={styles.skip} onClick={skip}>
                    Skip
                </div>
            )}
        </div>
    );
};

export { VideoQuestion };
export default VideoQuestion;
