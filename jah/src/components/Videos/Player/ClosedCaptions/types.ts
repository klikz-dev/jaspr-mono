import { Video } from 'expo-av';
import { VideoState } from '../types';

export interface Props {
    video: Video | HTMLVideoElement;
    videoState: VideoState;
    setVideoState: (videoState: VideoState | ((videoState: VideoState) => any)) => void;
}

export interface Cue {
    startTime: number;
    endTime: number;
    text: string;
}
