import { Video } from './media';

export interface Person {
    id: number;
    image1x: string;
    image2x: string;
    image3x: string;
    labelColor: string; // TODO We don't use labelColor anymore
    name: string;
    order: number;
}

interface Topic {
    id: number;
    labelColor: string; // TODO We don't use labelColor anymore
    name: string;
    order: number;
}

export interface Story {
    id: number;
    order: number;
    person: Person;
    topic: Topic;
    video: Video;
}

export type Stories = Story[];
