import React, { forwardRef, useImperativeHandle, useRef, useState } from 'react';
import Slider from '@react-native-community/slider';
import Styled from 'styled-components/native';
import { Props } from './types';

const Container = Styled.View`
    flex: 1;
    flex-direction: row;
    margin-left: 10px;
    margin-right: 10px;
    align-items: center;
`;

const SliderContainer = Styled.View`
    flex: 1;
`;

const TimeElapsed = Styled.Text`
    font-size: 14px;
    color: #FFFFFF;
`;

const TimeTotal = Styled.Text`
    font-size: 14px;
    color: #FFFFFF;
    text-align: right;
`;

const ProgressSlider = forwardRef(
    ({ currentTime = 0, duration = 0, pause, seek, seekEnd }: Props, ref) => {
        const tracking = useRef(false);
        const [progress, setProgress] = useState<number>(currentTime);
        const [time, setTime] = useState('00:00');

        const getMinutesFromMs = (time: number) => {
            const totalSeconds = time / 1000;
            const hours = totalSeconds > 3600 ? Math.floor(totalSeconds / 3600) : 0;
            const minutes = totalSeconds >= 60 ? Math.floor(totalSeconds / 60) : 0;
            const seconds = Math.floor(totalSeconds - minutes * 60);

            return `${hours ? `${hours}:` : ''}${minutes >= 10 ? minutes : '0' + minutes}:${
                seconds >= 10 ? seconds : '0' + seconds
            }`;
        };

        const fullDuration = getMinutesFromMs(duration);

        const onSlidingStart = () => {
            tracking.current = true;
            pause();
        };

        const onSlidingComplete = (time: number) => {
            tracking.current = false;
            seekEnd(time);
        };

        const onSeek = (time: number) => {
            setTime(getMinutesFromMs(time));
            seek(time);
        };

        useImperativeHandle(ref, () => ({
            setProgressSlider(position: number) {
                if (!tracking.current) {
                    setProgress(position);
                    setTime(getMinutesFromMs(position));
                }
            },
        }));

        return (
            <Container>
                <TimeElapsed>{time}</TimeElapsed>
                <SliderContainer>
                    <Slider
                        value={progress}
                        minimumValue={0}
                        maximumValue={duration}
                        step={duration / 1000}
                        onSlidingStart={onSlidingStart}
                        onValueChange={onSeek}
                        onSlidingComplete={onSlidingComplete} // TODO Track if paused before slide start
                        minimumTrackTintColor="rgba(255, 255, 255, 0.9)"
                        maximumTrackTintColor={'#FFFFFF'}
                        thumbTintColor="rgba(255, 255, 255, 0.9)"
                    />
                </SliderContainer>
                <TimeTotal>{fullDuration}</TimeTotal>
            </Container>
        );
    },
);

export default ProgressSlider;
