import React, {
    forwardRef,
    useCallback,
    useContext,
    useEffect,
    useRef,
    useState,
    useImperativeHandle,
} from 'react';
import * as Sentry from 'sentry-expo';
import ClosedCaptions from './ClosedCaptions';
import PlayerControls from './PlayerControl';
import styles from './index.module.scss';
import playIconSource from 'assets/play.png';

import { Audio, Video, AVPlaybackStatus } from 'expo-av';
import * as ScreenOrientation from 'expo-screen-orientation';
import Styled from 'styled-components/native';
import { setFullscreen } from 'state/actions/media';

import { Animated, TouchableWithoutFeedback, Platform } from 'react-native';

import Segment from 'lib/segment';
import { addAction, actionNames } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import { getVideoRatings, updateProgress } from 'state/actions/stories';

const StyledVideoContainer = Styled.View`${styles.video} flex-shrink: 1;`;
const StyledPoster = Styled.Image`${styles.poster}`;
const StyledPosterView = Styled.TouchableOpacity`
    position: absolute;
    top: 0;
    margin: auto;
    width: 100%;
    height: 100%;
    align-items: center;
    justify-content: center;
`;
const PlayIcon = Styled.Image`
    display: flex;
    width: 65px;
`;
import { ControlStates, SeekStates, VideoState, VideoAnalyticEvents } from './types';

interface Props {
    videoId?: number | null;
    autoplay?: boolean;
    poster?: string;
    fpm4Transcode: string;
    hlsPlaylist: string;
    mp4Transcode?: string;
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
        const videoEl = useRef<Video | HTMLVideoElement>(null!);
        const [store, dispatch] = useContext(StoreContext);
        const { stories, media } = store;
        const { captionsEnabled = true } = media;
        const { videoRatings, ratingsFetched } = stories;
        const controlsOpacity = useRef(new Animated.Value(1)).current;
        const playerControlsRef = useRef();
        const closedCaptionsRef = useRef();

        const progress = useRef<number>(0);

        const [videoState, setVideoState] = useState<VideoState>({
            fullscreen: false,
            play: false,
            currentTime: 0,
            duration: 0,
            showControls: ControlStates.Visibile,
            captions: captionsEnabled,
            seekState: SeekStates.NotSeeking,
            loaded: false,
            hasCaptions: true,
        });

        const logVideoAnalytics = (event: VideoAnalyticEvents, properties: any) => {
            Segment.track(event, {
                content_asset_id: name,
                session_id: analyticsSessionId,
                video_player: Platform.OS,
                ad_enabled: false,
                livestream: false,
                ...properties,
            });
        };

        const setProgress = (percentWatched: number) => {
            // Progress only goes forward.  Don't set back if they watch again
            if (percentWatched > 95 && !watched) {
                setWatched(true);
            }
            progress.current =
                progress.current > percentWatched ? progress.current : percentWatched;
        };

        const hideControls = useCallback(() => {
            const hideAnimation = Animated.timing(controlsOpacity, {
                toValue: 0,
                duration: 500,
                useNativeDriver: true,
            });
            hideAnimation.start(({ finished }) => {
                if (finished) {
                    setVideoState((videoState) => ({
                        ...videoState,
                        showControls: ControlStates.Hidden,
                    }));
                }
            });
        }, [controlsOpacity, setVideoState]);

        const showControls = useCallback(() => {
            const showAnimation = Animated.timing(controlsOpacity, {
                toValue: 1,
                duration: 250,
                useNativeDriver: true,
            });

            showAnimation.start(({ finished }) => {
                if (finished) {
                    setVideoState((videoState) => ({
                        ...videoState,
                        showControls: ControlStates.Visibile,
                    }));
                }
            });
        }, [controlsOpacity, setVideoState]);

        const lastStatus = useRef<AVPlaybackStatus | null>(null);

        const recordAnalytic = (
            name: VideoAnalyticEvents,
            status: AVPlaybackStatus,
            additionalProperties: any = {},
        ) => {
            if (status.isLoaded) {
                const properties = {
                    total_length: status.durationMillis,
                    position: status.positionMillis,
                    sound: status.volume * 100,
                    ...additionalProperties,
                };
                logVideoAnalytics(name, properties);
            }
        };

        const toggleControls = () => {
            if (Platform.OS !== 'android') return;
            switch (videoState.showControls) {
                case ControlStates.Visibile:
                    setVideoState((videoState) => ({
                        ...videoState,
                        showControls: ControlStates.Hiding,
                    }));
                    hideControls();
                    break;
                case ControlStates.Hidden:
                    setVideoState((videoState) => ({
                        ...videoState,
                        showControls: ControlStates.Showing,
                    }));
                    showControls();
                    break;
                case ControlStates.Hiding:
                    setVideoState((videoState) => ({
                        ...videoState,
                        showControls: ControlStates.Showing,
                    }));
                    showControls();
                    break;
                case ControlStates.Showing:
                    break;
                default:
                    break;
            }
        };

        useImperativeHandle(ref, () => ({
            replayVideo() {
                if (videoEl.current) {
                    if (videoEl.current instanceof HTMLVideoElement) {
                        videoEl.current.currentTime = 0;
                    }
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
                if (videoEl.current instanceof Video) {
                    videoEl.current.playAsync(); // Native
                } else if (videoEl.current) {
                    videoEl.current.play(); // Web
                }
                setVideoState((videoState) => ({
                    ...videoState,
                    play: true,
                }));
            }
        };

        const timeupdate = (currentTime: number, duration: number) => {
            const timeNow = new Date().getTime();
            // If a minute has elapsed since we started or have last updated.
            timeupdateCallback(currentTime, duration);
        };

        const onVideoFinishedPlaying = () => {
            progress.current = 100;
            setShowPoster(true);
        };

        // Allow audio to play even when the phone is switched to silent mode
        useEffect(() => {
            Audio.setAudioModeAsync({
                playsInSilentModeIOS: true,
            });
        }, []);

        const defaultOrientation = useRef<ScreenOrientation.PlatformOrientationInfo>();

        // Unlock device orientation so device can be rotated landscape
        useEffect(() => {
            const unlock = async () => {
                const platformOrientation =
                    await ScreenOrientation.getPlatformOrientationLockAsync();
                defaultOrientation.current = platformOrientation;
                await ScreenOrientation.unlockAsync();
            };
            unlock();
            return () => {
                // TODO Possible race condition if the asyncronous unlock doesn't finish before the
                // component umounts.  In that case, the rest of the app will be viewable in landscape mode
                if (defaultOrientation.current) {
                    ScreenOrientation.lockPlatformAsync(defaultOrientation.current);
                }
            };
        }, []);

        useEffect(() => {
            const controlsTimer = setTimeout(hideControls, 4000);
            return () => clearTimeout(controlsTimer);
        }, [
            videoState.seekState,
            videoState.play,
            videoState.captions,
            videoState.fullscreen,
            hideControls,
        ]);

        useEffect(() => {
            const checkFullScreenLandscape = async (
                e: ScreenOrientation.OrientationChangeEvent,
            ) => {
                if (!videoEl.current || !(videoEl.current instanceof Video)) return;
                const { orientationInfo } = e;
                const { LANDSCAPE_LEFT, LANDSCAPE_RIGHT } = ScreenOrientation.Orientation;
                const { orientation } = orientationInfo;
                const status = await videoEl.current.getStatusAsync();
                if (
                    status.isLoaded &&
                    status?.isPlaying &&
                    (orientation === LANDSCAPE_LEFT || orientation === LANDSCAPE_RIGHT)
                ) {
                    if (Platform.OS === 'ios') {
                        videoEl.current.presentIOSFullscreenPlayer();
                    } else {
                        setFullscreen(dispatch, true);
                        setVideoState((videoState) => ({ ...videoState, fullScreen: true }));
                    }
                } else {
                    if (Platform.OS === 'ios') {
                        videoEl.current.dismissIOSFullscreenPlayer();
                    } else {
                        setFullscreen(dispatch, false);
                        setVideoState((videoState) => ({ ...videoState, fullScreen: false }));
                    }
                }
            };

            const listener =
                ScreenOrientation.addOrientationChangeListener(checkFullScreenLandscape);
            return () => {
                ScreenOrientation.removeOrientationChangeListener(listener);
                setFullscreen(dispatch, false);
            };
        }, [dispatch, videoEl, setVideoState]);

        // Rotate and resize video to full screen when fullscreen button toggled
        useEffect(() => {
            try {
                if (videoState.fullscreen) {
                    ScreenOrientation.lockAsync(ScreenOrientation.OrientationLock.LANDSCAPE_LEFT);
                } else {
                    ScreenOrientation.unlockAsync();
                }
            } catch (err) {
                console.log('Unable to open video fullscreen');
                Sentry.Native.captureException(err);
            }
        }, [videoState.fullscreen]);

        return (
            <StyledVideoContainer style={{ aspectRatio: 16 / 9 }}>
                <>
                    <TouchableWithoutFeedback onPress={toggleControls}>
                        <Video
                            source={{
                                uri: Platform.OS === 'ios' ? hlsPlaylist : fpm4Transcode,
                            }}
                            // @ts-ignore
                            ref={videoEl}
                            rate={1.0}
                            volume={1.0}
                            isMuted={false}
                            progressUpdateIntervalMillis={100}
                            resizeMode={Video.RESIZE_MODE_CONTAIN}
                            useNativeControls={Platform.OS === 'ios'}
                            style={{ flex: 1, width: '100%', height: '100%' }}
                            onPlaybackStatusUpdate={(status) => {
                                if (!videoState.loaded && status.isLoaded) {
                                    setVideoState((videoState) => ({
                                        ...videoState,
                                        loaded: true,
                                        duration: status.durationMillis,
                                    }));
                                }

                                if (status.isLoaded && status.didJustFinish) {
                                    setVideoState((videoState) => ({ ...videoState, play: false }));
                                    onVideoFinishedPlaying();
                                    recordAnalytic(VideoAnalyticEvents.PlaybackCompleted, status);
                                } else {
                                    if (
                                        status.isLoaded &&
                                        status.isPlaying &&
                                        status.durationMillis
                                    ) {
                                        timeupdate(status.positionMillis, status.durationMillis);
                                        const updatedProgress = Math.ceil(
                                            (status.positionMillis / status.durationMillis) * 100,
                                        );

                                        if (!isNaN(updatedProgress)) {
                                            setProgress(updatedProgress);
                                        }

                                        if (playerControlsRef?.current) {
                                            // @ts-ignore
                                            playerControlsRef.current.updateCurrentTime(
                                                status.positionMillis,
                                            );
                                        }

                                        if (closedCaptionsRef?.current) {
                                            // @ts-ignore
                                            closedCaptionsRef.current.setCurrentTime(
                                                status.positionMillis,
                                            );
                                        }

                                        /*setVideoState((videoState) => ({
                                        ...videoState,
                                        currentTime: status.positionMillis,
                                    }));*/
                                    }
                                }

                                if (
                                    status.isLoaded &&
                                    lastStatus?.current?.isLoaded &&
                                    lastStatus.current.isBuffering !== status.isBuffering
                                ) {
                                    if (status.isBuffering) {
                                        logVideoAnalytics(
                                            VideoAnalyticEvents.BufferStarted,
                                            status,
                                        );
                                    } else {
                                        logVideoAnalytics(
                                            VideoAnalyticEvents.BufferCompleted,
                                            status,
                                        );
                                    }
                                } else if (
                                    lastStatus?.current?.isLoaded &&
                                    status.isLoaded &&
                                    lastStatus.current.isPlaying !== status.isPlaying
                                ) {
                                    if (status.isLoaded && status.isPlaying) {
                                        logVideoAnalytics(
                                            VideoAnalyticEvents.PlaybackStarted,
                                            status,
                                        );
                                    } else {
                                        logVideoAnalytics(
                                            VideoAnalyticEvents.PlaybackPaused,
                                            status,
                                        );
                                    }
                                }
                                lastStatus.current = status;
                            }}
                            videoState={videoState}
                        />
                    </TouchableWithoutFeedback>
                    {Platform.OS === 'android' && (
                        <>
                            <TouchableWithoutFeedback onPress={toggleControls}>
                                <Animated.View
                                    style={{
                                        position: 'absolute',
                                        top: 0,
                                        bottom: 0,
                                        left: 0,
                                        right: 0,
                                        opacity: controlsOpacity,
                                    }}
                                >
                                    <PlayerControls
                                        ref={playerControlsRef}
                                        // @ts-ignore
                                        video={videoEl}
                                        videoState={videoState}
                                        setVideoState={setVideoState}
                                    />
                                </Animated.View>
                            </TouchableWithoutFeedback>

                            <ClosedCaptions
                                // @ts-ignore
                                ref={closedCaptionsRef}
                                video={videoEl.current}
                                videoState={videoState}
                                setVideoState={setVideoState}
                            />
                        </>
                    )}
                </>

                {Boolean(showPoster) && Boolean(!poster) && (
                    <StyledPosterView onPress={playVideo} style={{ aspectRatio: 16 / 9 }}>
                        <PlayIcon source={playIconSource} />
                    </StyledPosterView>
                )}
                {Boolean(showPoster) && Boolean(poster) && (
                    <StyledPosterView onPress={playVideo} style={{ aspectRatio: 16 / 9 }}>
                        <StyledPoster source={{ uri: poster }} style={{ aspectRatio: 16 / 9 }} />
                        <PlayIcon source={playIconSource} />
                    </StyledPosterView>
                )}
            </StyledVideoContainer>
        );
    },
);

export default Player;
