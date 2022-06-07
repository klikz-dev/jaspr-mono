export interface SharedStory {
    id: number;
    person: {
        id: number;
        name: string;
        image1x: string;
        image2x: string;
        image3x: string;
        labelColor: string; // hex color code
        order: number;
    };
    topic: {
        id: number;
        name: string;
        labelColor: string; // hex color code
        order: number;
    };
    video: {
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
    };
    order: number;
}

export type GetResponse = SharedStory[];
