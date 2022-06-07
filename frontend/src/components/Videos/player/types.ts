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

export interface ViewProps {
    autoplay: boolean;
    playVideo: () => void;
    showPoster: boolean;
    poster?: string;
    fpm4Transcode: string;
    hlsPlaylist: string;
    mp4Transcode?: string;
    videoEl: React.RefObject<HTMLVideoElement>;
    timeupdate: (currentTime: number, duration: number) => void;
    onVideoFinishedPlaying: () => void;
    setProgress: (progress: number) => void;
    progress: React.RefObject<number>;
    logVideoAnalytics: (event: VideoAnalyticEvents, properties: any) => void;
    setVideoState: (videoState: VideoState | ((videoState: VideoState) => any)) => void;
    videoState: VideoState;
    setShowPoster?: (show: boolean) => void;
    ccButtonNodeRef?: Node;
}
