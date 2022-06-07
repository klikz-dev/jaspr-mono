export type Patient = {
    id: number;
    currentEncounter: number | null;
    currentEncounterCreated: string;
    currentEncounterDepartment: number;
    suggestNewEncounter: boolean;
    analyticsToken: string;
    email: string;
    mobilePhone: string;
    departments: number[];
    activities: { csa: boolean | null; csp: boolean | null; skills: boolean | null };
    lastLoggedInAt: string; // 2021-05-21T17:05:29.244777Z
    toolsToGoStatus: 'Not Started' | 'Email Sent' | 'Phone Number Verified' | 'Setup Finished';
    tourComplete: boolean;
    created: string; // 2020-07-14T19:50:46.273000Z
} & (
    | {
          ssid: string;
          firstName: '';
          lastName: '';
          dateOfBirth: null;
          mrn: '';
      }
    | {
          ssid: '';
          firstName: string;
          lastName: string;
          dateOfBirth: string | null; // 1985-10-11
          mrn: string;
      }
);
export type PostRequest = Pick<
    Patient,
    'firstName' | 'lastName' | 'dateOfBirth' | 'mrn' | 'ssid' | 'departments' | 'mobilePhone'
>;

export type PostResponse = Patient;

export type GetResponse = Patient[];
