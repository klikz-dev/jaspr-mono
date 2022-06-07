import { Video } from './media';

interface WalkthroughVideo {
    stepName: string;
    frontendRenderType: 'videoDescription' | 'video';
    value: Video;
}

interface WalkthroughCopingStrategy {
    stepName: string;
    frontendRenderType: 'copingStrategy';
    value: {
        category: {
            id: number;
            name: string;
            whyText: string;
        };
    };
    title: string;
    image: string; // url
}

interface WalkthroughGuideMessage {
    stepName: string;
    frontendRenderType: 'guide';
    value: {
        message: string;
    };
}

interface WalkthroughCrisisLine {
    stepName: string;
    frontendRenderType: 'nationalHotline';
    value: {
        name: string;
        phone: string;
        text: string;
    };
}

interface WalkthroughRecap {
    stepName: string;
    frontendRenderType: 'recap';
    value: null;
}

type WalkthroughItem =
    | WalkthroughVideo
    | WalkthroughCopingStrategy
    | WalkthroughGuideMessage
    | WalkthroughCrisisLine
    | WalkthroughRecap;

export type Walkthrough = WalkthroughItem[];
