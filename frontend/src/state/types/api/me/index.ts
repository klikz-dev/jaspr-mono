import { PatientSerializer } from '../sharedSerializers';

export interface MeTechnician {
    id: number;
    location: {
        system: {
            id: number;
            name: string;
        };
    };
    userType: 'technician';
    analyticsToken: string;
    firstName: string;
    lastName: string;
    email: string;
    supportUrl: string; // Freshdesk
    role: ''; // TODO Future value not used yet
}

export type MePatient = PatientSerializer;

export type GetResponse = MeTechnician | MePatient;

export type PatchRequest = Partial<
    Pick<MePatient, 'guide' | 'tourComplete' | 'email' | 'mobilePhone'>
>;

export type PatchResponse = GetResponse;
