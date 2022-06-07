import { Video } from 'state/types';

export type GetResponse = {
    id: number;
    name: string;
    mainPageImage: null | string;
    thumbnailImage: null | string;
    targetUrl: string;
    labelColor: null | string;
    order: number;
    video: null | Video; // Most activities have videos.  Paced Breathing does not
    // Patient Activity objects get merged in at the API to facilitate simultaneous loading of ratings/favories
    patientActivity?: null | number;
    rating?: null | 1 | 2 | 3 | 4 | 5;
    saveForLater?: null | boolean;
    viewed?: null | boolean;
}[];
