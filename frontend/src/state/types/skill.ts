import { Video } from './media';

export interface Skill {
    id: number;
    name: string;
    video: Video | null;
    mainPageImage: string | null;
    thumbnailImage: string;
    targetUrl: string | null;
    labelColor: string | null;
    rating?: 1 | 2 | 3 | 4 | 5 | null;
    saveForLater?: boolean | null;
    viewed?: boolean | null;
    order: number;
    patientActivity?: number | null; // ForeignKey to SkillActivity
}

export interface SkillActivity {
    activity: number; // ForeignKey to Skill
    id: number;
    saveForLater?: boolean | null;
    rating?: 1 | 2 | 3 | 4 | 5 | null;
    viewed?: boolean;
}

export type Skills = Skill[];
