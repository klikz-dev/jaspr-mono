import React, { forwardRef, useEffect, useImperativeHandle, useState } from 'react';
import axios from 'axios';
import Styled from 'styled-components/native';
import parser from 'subtitles-parser-vtt';
import { Video } from 'expo-av';
import { ControlStates } from '../types';
import { Cue, Props } from './types';

const Container = Styled.View`
    position: absolute;
    bottom: ${({ controlsOpen }: { controlsOpen: boolean }) => (controlsOpen ? '65px' : '5px')}
    z-index: 1000;
`;
const Caption = Styled.Text`
    text-align: center;
    color: white;
`;

const ClosedCaptions = forwardRef(({ video, videoState, setVideoState }: Props, ref) => {
    const [cues, setCues] = useState<Cue[] | []>([]);
    const [currentTime, setCurrentTime] = useState<number>(0);

    useImperativeHandle(ref, () => ({
        setCurrentTime(position: number) {
            setCurrentTime(position);
        },
    }));

    useEffect(() => {
        (async () => {
            if (video instanceof Video && typeof video.props.source === 'object') {
                const src = video.props.source.uri;

                if (src) {
                    const filebase = src.split('/').slice(-2, -1)[0];
                    const vttFile = `kiosk_${filebase}_fpm4_en.vtt`;
                    const captionSrc = src.replace(/index.mpd|index.m3u8/, vttFile);

                    try {
                        const response = await axios.get(captionSrc, {
                            transformRequest: [
                                (data, headers) => {
                                    delete headers.common.Authorization;
                                    return data;
                                },
                            ],
                        });
                        const json = response.data;
                        setCues(parser.fromVtt(json, 'ms'));
                        setVideoState((videoState) => ({ ...videoState, hasCaptions: true }));
                    } catch (err) {
                        setVideoState((videoState) => ({ ...videoState, hasCaptions: false }));
                    }
                }
            }
        })();
    }, [setVideoState, video]);

    const currentCue = cues.find(
        (cue: Cue) => currentTime >= cue.startTime && cue.endTime > currentTime,
    );
    return (
        <Container controlsOpen={videoState.showControls !== ControlStates.Hidden}>
            {videoState.hasCaptions && videoState.captions && Boolean(currentCue?.text) && (
                <Caption>{currentCue?.text || ''}</Caption>
            )}
        </Container>
    );
});

export default ClosedCaptions;
