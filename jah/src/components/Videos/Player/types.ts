import { Video } from 'expo-av';

export enum ControlStates {
    Visibile = 'VISIBLE',
    Showing = 'SHOWING',
    Hidden = 'HIDDEN',
    Hiding = 'HIDING',
}

export enum SeekStates {
    NotSeeking = 'NotSeeking',
    Seeking = 'Seeking',
    Seeked = 'Seeked',
}

export enum VideoAnalyticEvents {
    BufferStarted = 'Video Playback Buffer Started',
    BufferCompleted = 'Video Playback Buffer Completed',
    PlaybackStarted = 'Video playback Started',
    PlaybackPaused = 'Video Playback Paused',
    PlaybackCompleted = 'Video Playback Completed',
    PlaybackInterrupted = 'Video Playback Interrupted',
}

export interface VideoState {
    fullscreen: boolean;
    play: boolean;
    currentTime: number;
    duration: number;
    showControls: ControlStates;
    captions: boolean;
    seekState: SeekStates;
    loaded: boolean;
    hasCaptions: boolean;
}
