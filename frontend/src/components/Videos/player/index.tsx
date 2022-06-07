import React, {
    forwardRef,
    useContext,
    useCallback,
    useEffect,
    useRef,
    useState,
    useImperativeHandle,
} from 'react';
import dashjs from 'dashjs';
import PlayButton from 'assets/PlayButton.png';
import CCButton from './CCButton';
import styles from './index.module.scss';
import { setCaptionsEnabled } from 'state/actions/media';
import Segment, { AnalyticNames } from 'lib/segment';
import { addAction, actionNames } from 'state/actions/analytics';
import TimerContext from 'state/context/timer';
import StoreContext from 'state/context/store';
import { getVideoRatings, updateProgress } from 'state/actions/stories';

import { VideoAnalyticEvents } from './types';

interface Props {
    videoId?: number | null;
    autoplay?: boolean;
    poster?: string;
    fpm4Transcode: string;
    hlsPlaylist: string;
    mp4Transcode?: string;
    resetTimer?: () => void;
    name?: string;
    timeupdateCallback?: (currentTime: number, duration: number) => void;
    ccButtonNodeRef?: React.RefObject<HTMLDivElement>;
}

const Player = forwardRef(
    (
        {
            videoId,
            autoplay = false,
            poster,
            fpm4Transcode,
            hlsPlaylist,
            mp4Transcode,
            name = '',
            timeupdateCallback = (): null => null,
            ccButtonNodeRef,
        }: Props,
        ref,
    ) => {
        const [showPoster, setShowPoster] = useState<boolean>(true); // todo: !autoplay
        const [watched, setWatched] = useState<boolean>(false);
        const [analyticsSessionId] = useState<number>(new Date().getTime());
        const videoEl = useRef<HTMLVideoElement>(null!);
        const timeRef = useRef<number>(new Date().getTime());
        const { sendHeartbeat } = useContext(TimerContext);
        const [store, dispatch] = useContext(StoreContext);
        const { stories, media } = store;
        const { captionsEnabled = true } = media;
        const { videoRatings, ratingsFetched } = stories;

        const player = useRef<dashjs.MediaPlayerClass>();
        const unmounting = useRef(false);
        const [captionState, setCaptionState] = useState(captionsEnabled);
        const [initialized, setInitialized] = useState(false);
        const [hasClosedCaptions, setHasClosedCaptions] = useState(false);

        const isPlaying = useCallback(() => {
            const video = videoEl.current;
            return !!(
                video &&
                video.currentTime > 0 &&
                !video.paused &&
                !video.ended &&
                video.readyState > 2
            );
        }, [videoEl]);

        useEffect(() => {
            // Web only
            // DASH-MPEG Supported browsers
            if (window?.MediaSource && dashjs && fpm4Transcode) {
                if (initialized) return;
                if (isPlaying()) {
                    // Avoid replacing the media source while the video is playing
                    videoEl.current.pause();
                }
                player.current = dashjs.MediaPlayer().create();
                player.current.initialize(videoEl.current, fpm4Transcode, false);

                player.current.on(dashjs.MediaPlayer.events.STREAM_INITIALIZED, (event) => {
                    // Turn captions back off if they weren't enabled by default by the user
                    player.current.updateSettings({
                        streaming: {
                            text: {
                                defaultEnabled: captionState,
                            },
                        },
                    });
                    if (videoEl?.current.textTracks) {
                        videoEl.current.textTracks.addEventListener(
                            'change',
                            (e) => {
                                setCaptionsEnabled(
                                    dispatch,
                                    // @ts-ignore
                                    e.currentTarget?.[0]?.mode === 'showing' ? true : false,
                                );
                                setCaptionState(
                                    // @ts-ignore
                                    e.currentTarget?.[0]?.mode === 'showing' ? true : false,
                                );
                            },
                            false,
                        );
                    }
                });
                player.current.on(dashjs.MediaPlayer.events.MANIFEST_LOADED, (event) => {
                    // Captions need to be enabled by default for the browser to load and display
                    // the captions if toggled later in the stream
                    player.current.updateSettings({
                        streaming: {
                            text: {
                                defaultEnabled: true,
                            },
                        },
                    });
                    setCaptionState(true);
                    player.current.setTextTrack(0);
                });
                setInitialized(true);
            }
        }, [captionState, dispatch, fpm4Transcode, initialized, isPlaying, videoEl]);

        const recordAnalytic = useCallback(
            (eventLabel) => {
                if (
                    videoEl.current.currentTime <= 0 &&
                    eventLabel === AnalyticNames.VIDEO_PLAYBACK_INTERRUPTED
                )
                    return;

                if (!player) return;

                const logVideoAnalytics = (event: VideoAnalyticEvents, properties: any) => {
                    Segment.track(event, {
                        content_asset_id: name,
                        session_id: analyticsSessionId,
                        video_player: '',
                        ad_enabled: false,
                        livestream: false,
                        ...properties,
                    });
                };

                interface VideoProperties {
                    total_length: number;
                    position: number;
                    sound: number;
                    full_screen: boolean; // Why snake_case?
                    bitrate?: number;
                    framerate?: number;
                }

                const properties: VideoProperties = {
                    // @ts-ignore
                    total_length: parseInt(videoEl.current?.duration, 10),
                    // @ts-ignore
                    position: parseInt(videoEl.current?.currentTime, 10),
                    sound: videoEl.current?.volume * 100,
                    full_screen: Boolean(document.fullscreenElement),
                };

                const streamInfo = player.current?.getActiveStream()?.getStreamInfo();
                const dashMetrics = player.current?.getDashMetrics();
                const dashAdapter = player.current?.getDashAdapter();

                if (dashMetrics && streamInfo) {
                    const periodIdx = streamInfo.index;
                    const repSwitch = dashMetrics.getCurrentRepresentationSwitch('video');
                    const bitrate = repSwitch
                        ? Math.round(
                              // @ts-ignore parameters here are not correct
                              dashAdapter.getBandwidthForRepresentation(repSwitch.to, periodIdx) /
                                  1000,
                          )
                        : false;
                    if (bitrate) {
                        properties.bitrate = bitrate;
                    }
                    // @ts-ignore Function isn't typed?
                    const adaptation = dashAdapter.getAdaptationForType(
                        periodIdx,
                        'video',
                        streamInfo,
                    );
                    if (repSwitch) {
                        const framerate = adaptation.Representation_asArray.find(
                            // @ts-ignore // TODO Review arguments
                            (rep) => rep.id === repSwitch.to,
                        )?.frameRate;
                        if (framerate) {
                            properties.framerate = framerate;
                        }
                    }
                }
                logVideoAnalytics(eventLabel, properties);
            },
            [analyticsSessionId, name],
        );

        const onPlaybackStatusUpdate = () => {
            const { currentTime, duration } = videoEl?.current;
            const updatedProgress = Math.round(Math.ceil((currentTime / duration) * 100));
            if (!isNaN(updatedProgress)) {
                timeupdate(currentTime, duration);
                setProgress(updatedProgress);
            }
        };

        useEffect(() => {
            return () => {
                unmounting.current = true;
            };
        }, []);

        // This effect must come after the effect marking the component as unmounting
        useEffect(() => {
            return () => {
                if (unmounting.current) {
                    if (isPlaying()) {
                        recordAnalytic(VideoAnalyticEvents.PlaybackPaused);
                    }
                }
            };
        }, [recordAnalytic, isPlaying]);

        useEffect(() => {
            if (player.current) {
                player.current.setTextTrack(captionState ? 0 : null);
            }
        }, [captionState]);

        const progress = useRef<number>(0);

        const setProgress = (percentWatched: number) => {
            // Progress only goes forward.  Don't set back if they watch again
            if (percentWatched > 95 && !watched) {
                setWatched(true);
            }
            progress.current =
                progress.current > percentWatched ? progress.current : percentWatched;
        };

        useImperativeHandle(ref, () => ({
            replayVideo() {
                if (videoEl.current) {
                    videoEl.current.currentTime = 0;
                    playVideo();
                }
            },
        }));

        useEffect(() => {
            if (!ratingsFetched) {
                getVideoRatings(dispatch);
            }
        }, [dispatch, ratingsFetched]);

        useEffect(() => {
            if (watched) {
                addAction(actionNames.WATCH, { extra: name || fpm4Transcode });
            }
        }, [watched, fpm4Transcode, name]);

        // Save percent of video played when the component unmounts or the video changes
        useEffect(() => {
            return () => {
                const videoRating = videoRatings.find(
                    (video) => video.video === videoId && Boolean(videoId),
                );
                const ratingId = videoRating?.id;
                if (videoId !== undefined && videoId !== null) {
                    if (!videoRating?.progress && progress.current) {
                        updateProgress(dispatch, ratingId || null, videoId, progress.current);
                    } else if (
                        videoRating?.progress &&
                        progress.current > 0 &&
                        progress.current > videoRating.progress
                    ) {
                        updateProgress(dispatch, ratingId || null, videoId, progress.current);
                    }
                }
            };
        }, [dispatch, videoId, videoRatings]);

        const playVideo = () => {
            if (showPoster) {
                setShowPoster(false);
                if (videoEl.current) {
                    videoEl.current.play();
                }
            }
        };

        const timeupdate = (currentTime: number, duration: number) => {
            const timeNow = new Date().getTime();
            // If a minute has elapsed since we started or have last updated.
            if (timeNow - timeRef.current > 1000 * 60) {
                // Update the time in the ref to now.
                timeRef.current = timeNow;
                // Send off the heartbeat.
                sendHeartbeat();
            }
            timeupdateCallback(currentTime, duration);
        };

        const onVideoFinishedPlaying = () => {
            progress.current = 100;
            setShowPoster(true);
        };

        return (
            <div className={styles.video} onClick={playVideo}>
                <video
                    data-dashjs-player=""
                    preload="auto"
                    ref={videoEl}
                    style={{ opacity: showPoster && poster ? 0 : 1 }}
                    controls
                    controlsList="nodownload"
                    disablePictureInPicture
                    autoPlay={autoplay}
                    onTimeUpdate={onPlaybackStatusUpdate}
                    onLoadedMetadata={(e) => {
                        // @ts-ignore
                        if (e.target?.textTracks?.length) {
                            setHasClosedCaptions(true);
                        }
                    }}
                    onEnded={(e) => {
                        recordAnalytic(VideoAnalyticEvents.PlaybackCompleted);
                        onVideoFinishedPlaying();
                    }}
                    onAbort={(e) => {
                        e.persist();
                        recordAnalytic(VideoAnalyticEvents.PlaybackInterrupted);
                    }}
                    onPlay={() => showPoster && setShowPoster(false)}
                    onPlaying={() => recordAnalytic(VideoAnalyticEvents.PlaybackStarted)}
                    onError={(e) => {
                        e.persist();
                        recordAnalytic(VideoAnalyticEvents.PlaybackInterrupted);
                    }}
                    onPause={() => recordAnalytic(VideoAnalyticEvents.PlaybackPaused)}
                    onWaiting={() => recordAnalytic(VideoAnalyticEvents.BufferStarted)}
                    // onSeeking={(e) => console.log('seeking', e)}
                    // onSeeked={(e) => console.log('seeked', e)}
                    // TODO Event changes: Fullscreen, Buffer Start, Buffer End, Seeking, Resumed
                >
                    <>
                        {Boolean(fpm4Transcode) && (
                            <source
                                type="application/dash+xml"
                                src={fpm4Transcode}
                                onAbort={(e) => console.log('dash error', e)}
                            />
                        )}
                        {Boolean(hlsPlaylist) && (
                            <source
                                type="application/vnd.apple.mpegurl"
                                src={hlsPlaylist}
                                onAbort={(e) => console.log('hls error', e)}
                            />
                        )}

                        {Boolean(mp4Transcode) && (
                            <source
                                type="video/mp4"
                                src={mp4Transcode}
                                onAbort={(e) => console.log('mp4 error', e)}
                            />
                        )}
                    </>
                </video>

                {hasClosedCaptions && (
                    <CCButton
                        ccButtonNodeRef={ccButtonNodeRef}
                        captionState={captionState}
                        setCaptionState={setCaptionState}
                    />
                )}

                {showPoster && poster && (
                    <>
                        <img
                            alt=""
                            className={styles.poster}
                            style={{ cursor: 'pointer' }}
                            src={poster}
                        />
                        <img
                            alt="Play video"
                            src={PlayButton}
                            style={{ zIndex: 1, width: '114px' }}
                        />
                    </>
                )}
            </div>
        );
    },
);

export default Player;
