export interface Video {
    id: number;
    name: string;
    description: string;
    subtitleFile: string | null;
    poster: string | null;
    thumbnail: string | null;
    fpm4Transcode: string; // Duplicate of dashPlaylist
    mp4Transcode: string;
    hlsPlaylist: string;
    dashPlaylist: string;
    fileType: 'video';
    tags?: string[];
}

export interface VideoRating {
    id?: number;
    rating?: 1 | 2 | 3 | 4 | 5 | null;
    saveForLater?: boolean | null;
    video: number;
    viewed?: boolean | null;
    progress?: number | null;
}

export type VideoRatings = VideoRating[];

export interface StaticMediaVideo {
    dash: string;
    hls: string;
    poster: string;
    video?: string;
}

export interface StaticMedia {
    intro: StaticMediaVideo;
    expect: StaticMediaVideo;
    nationalHotline: StaticMediaVideo;
    crisisLines: StaticMediaVideo;
    crisisLinesExpect: StaticMediaVideo;
    supportivePeople: StaticMediaVideo;
    copingStrategies: StaticMediaVideo;
    reasonsLive: StaticMediaVideo;
    saferHome: StaticMediaVideo;
    warningSignals: StaticMediaVideo;
}

export interface Media {
    captionsEnabled?: boolean;
    isFullScreen?: boolean;
    mediaUrl: string;
    media: StaticMedia;
}
