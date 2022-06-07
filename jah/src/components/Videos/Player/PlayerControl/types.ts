import { Video } from 'expo-av';
import { VideoState } from '../types';

export interface Props {
    video: React.RefObject<Video>;
    videoState: VideoState;
    lastStatus: {};
    setVideoState: (videoState: VideoState | ((videoState: VideoState) => any)) => void;
}
