import React, { forwardRef, useContext, useImperativeHandle, useRef } from 'react';
import Styled from 'styled-components/native';
import ProgressSlider from './ProgressSlider';
import PlayIcon from 'assets/video/play.svg';
import PauseIcon from 'assets/video/pause.svg';
import FullscreenOpen from 'assets/video/fullscreen-open.svg';
import FullscreenClose from 'assets/video/fullscreen-closed.svg';
import CaptionsOffIcon from 'assets/video/captions-off.svg';
import CaptionsOnIcon from 'assets/video/captions-on.svg';
import { TouchableOpacity, TouchableWithoutFeedback } from 'react-native';
import { setFullscreen } from 'state/actions/media';
import StoreContext from 'state/context/store';

import { Props } from './types';
import { ControlStates, SeekStates } from '../types';

const Container = Styled.View`
    position: relative;
    padding-left: 14px;
    padding-right: 14px;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    height: 40px;
    margin-top: auto;
    margin-bottom: 20px;
    margin-left: 4px;
    margin-right: 4px;
    border-radius: 12px;
    background-color: rgba(74, 74, 74, 0.7);
`;

const PlayPause = Styled.TouchableOpacity`
    display: flex;
    height: 20px;
    width: 16px;
`;

const Captions = Styled.TouchableOpacity`
    display: flex;
    height: 20px;
`;

const View = Styled.View``;

const PlayerControls = forwardRef(
    ({ video, videoState, lastStatus, setVideoState }: Props, ref) => {
        const [, dispatch] = useContext(StoreContext);
        const progressSliderRef = useRef<typeof ProgressSlider>(null);
        const play = () => {
            if (!video.current) return;
            setVideoState((videoState) => ({ ...videoState, play: true }));
            if (videoState.currentTime >= videoState.duration - 500) {
                video.current.replayAsync();
            } else {
                video.current.playAsync();
            }
        };

        const pause = () => {
            if (!video.current) return;
            setVideoState((videoState) => ({ ...videoState, play: false }));
            video.current.pauseAsync();
        };

        const toggleFullScreen = () => {
            setFullscreen(dispatch, !videoState.fullscreen);
            setVideoState((videoState) => ({ ...videoState, fullscreen: !videoState.fullscreen }));
        };

        const toggleCaptions = () => {
            setVideoState((videoState) => ({ ...videoState, captions: !videoState.captions }));
        };

        const seek = async (time: number) => {
            setVideoState((videoState) => ({
                ...videoState,
                seekState: SeekStates.Seeking,
                currentTime: time,
            }));
        };

        const seekEnd = async (time: number) => {
            if (!video.current) return;
            setVideoState((videoState) => ({
                ...videoState,
                seekState: SeekStates.Seeked,
                currentTime: time,
            }));
            await video.current.setStatusAsync({
                positionMillis: time,
                shouldPlay: true,
            });
            setVideoState((videoState) => ({
                ...videoState,
                seekState: SeekStates.NotSeeking,
                play: true,
            }));
        };

        useImperativeHandle(ref, () => ({
            updateCurrentTime(position: number) {
                if (progressSliderRef.current) {
                    // @ts-ignore
                    progressSliderRef.current.setProgressSlider(position);
                }
            },
        }));

        return (
            <View
                pointerEvents={videoState.showControls !== ControlStates.Hidden ? 'auto' : 'none'}
                style={{
                    position: 'absolute',
                    top: 0,
                    bottom: 0,
                    left: 0,
                    right: 0,
                }}
            >
                <View style={{ display: 'flex', flex: 1 }}>
                    <TouchableOpacity
                        onPress={toggleFullScreen}
                        hitSlop={{ top: 10, bottom: 20, left: 20, right: 10 }}
                        style={{
                            position: 'absolute',
                            top: 10,
                            right: 10,
                        }}
                    >
                        {videoState.fullscreen ? <FullscreenClose /> : <FullscreenOpen />}
                    </TouchableOpacity>
                    <TouchableWithoutFeedback>
                        <Container>
                            <PlayPause onPress={videoState?.play ? pause : play}>
                                {videoState.play ? <PauseIcon /> : <PlayIcon />}
                            </PlayPause>
                            <ProgressSlider
                                duration={videoState.duration}
                                pause={pause}
                                play={play}
                                seek={seek}
                                seekEnd={seekEnd}
                                // @ts-ignore
                                ref={progressSliderRef}
                            />
                            {videoState.hasCaptions && (
                                <Captions
                                    onPress={toggleCaptions}
                                    hitSlop={{ top: 20, left: 20, bottom: 20, right: 20 }}
                                >
                                    {videoState.captions && <CaptionsOnIcon />}
                                    {!videoState.captions && <CaptionsOffIcon />}
                                </Captions>
                            )}
                        </Container>
                    </TouchableWithoutFeedback>
                </View>
            </View>
        );
    },
);

export default PlayerControls;
