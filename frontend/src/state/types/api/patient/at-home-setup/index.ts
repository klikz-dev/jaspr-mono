import { MePatient } from 'state/types/api/me';

export type PostResponse = MePatient;

export interface PostRequest {
    email: string;
    mobilePhone: string;
}
