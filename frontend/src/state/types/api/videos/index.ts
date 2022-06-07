export interface Video {
    id: number;
    name: string;
    description: string;
    fileField: string;
    subtitleFile: null | string;
    transcript: string;
    poster: null | string;
    thumbnail: null | string;
    fpm4Transcode: null | string;
    mp4Transcode: null | string;
    mp3Transcode: null | string;
    tips: string;
    completionTime: null | number;
    hlsPlaylist: null | string;
    dashPlaylist: null | string;
    duration: null | number;
    fileType: 'video';
    tags: string[];
}

export type GetResponse = Video[];
