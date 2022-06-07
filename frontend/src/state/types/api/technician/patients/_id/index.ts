import { Patient } from '../';

export type GetResponse = Patient;

export type PutRequest = Pick<
    Patient,
    'firstName' | 'lastName' | 'dateOfBirth' | 'mrn' | 'ssid' | 'departments' | 'mobilePhone'
>;

export type PutResponse = Patient;
