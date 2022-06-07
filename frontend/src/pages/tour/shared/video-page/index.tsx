import { useState, useRef, useContext } from 'react';
import { useHistory } from 'lib/router';
import StoreContext from 'state/context/store';
import Player from 'components/Videos/player';
import Hamburger from 'components/Hamburger';
import Button from 'components/Button';
import logo from 'assets/logo.png';
import styles from './video.module.scss';
import { completeTour } from 'state/actions/user';

interface VideoProps {
    poster: string;
    dashPlaylist: string;
    hlsPlaylist: string;
    mp4Transcode?: string;
    nextPage: string;
    nextPageParams?: string;
    noReplay?: boolean;
    noSkip?: boolean;
    back?: string;
}

const Video = (props: VideoProps) => {
    const history = useHistory();
    const {
        poster,
        dashPlaylist,
        hlsPlaylist,
        mp4Transcode,
        nextPageParams,
        nextPage,
        back,
        noSkip,
        noReplay,
    } = props;
    const [skipLabel, setSkipLabel] = useState('Skip this ›');
    const [videoComplete, setVideoComplete] = useState(false);
    const [, dispatch] = useContext(StoreContext);
    const playerRef = useRef<typeof Player>(null!);
    const ccButtonNodeRef = useRef<HTMLDivElement>(null);

    // Change skip button to next button when > 95% of video has been watched
    const timeupdate = (currentTime: number, duration: number) => {
        if (videoComplete) return;
        if (currentTime / duration > 0.95 && skipLabel !== 'Next') {
            setSkipLabel('Next');
            setVideoComplete(true);
        }
    };

    const replayVideo = () => {
        // @ts-ignore
        playerRef.current.replayVideo();
    };

    const next = () => {
        if (nextPageParams === '?completeTour=true') {
            // This is a hack.  It doesn't really belong in this component
            completeTour(dispatch);
        }
        history.push({ pathname: nextPage, search: nextPageParams || '' });
    };

    return (
        <div
            className={styles.container}
            style={{ background: 'linear-gradient(90deg, #383c58 0%, #343245 100%)' }}
        >
            <header>
                <img src={logo} className={styles.logo} alt="" />
                <Hamburger dark={true} />
            </header>
            <div className={styles.videoContainer}>
                <Player
                    ref={playerRef}
                    videoId={null}
                    poster={poster}
                    fpm4Transcode={dashPlaylist}
                    hlsPlaylist={hlsPlaylist}
                    mp4Transcode={mp4Transcode}
                    name=""
                    timeupdateCallback={timeupdate}
                    ccButtonNodeRef={ccButtonNodeRef}
                />
            </div>
            <div className={styles.controls}>
                {Boolean(back) && back !== undefined && (
                    <div className={styles.col}>
                        <div className={styles.back} onClick={() => history.push(back)}>
                            ‹ Back
                        </div>
                    </div>
                )}
                {!noReplay && (
                    <div className={styles.col} style={{ alignItems: 'center' }}>
                        <div className={styles.replay} onClick={replayVideo}>
                            Replay
                        </div>
                    </div>
                )}
                {(videoComplete || !noSkip) && (
                    <div className={styles.col}>
                        <Button onClick={next}>{skipLabel}</Button>
                    </div>
                )}
                <div className={styles.col}>
                    <div className={styles.ccButtonContainer} ref={ccButtonNodeRef} />
                </div>
            </div>
        </div>
    );
};

export default Video;
