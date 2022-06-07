export type PostResponse = {
    id: number;
    currentEncounter: number;
    currentEncounterCreated: string; // 2022-02-26T01:14:34.115860Z
    currentEncounterDepartment: number;
    suggestNewEncounter: boolean;
    email: string;
    mobilePhone: string;
    departments: number[];
    activities: {
        csp: boolean;
        csa: boolean;
        skills: boolean;
    };
    lastLoggedInAt: null | string; // 2022-02-26T01:14:34.115860Z
    toolsToGoStatus: 'Not Started' | 'Email Sent' | 'Phone Number Verified' | 'Setup Finished';
    tourComplete: boolean;
    created: string; // 2022-02-26T01:14:34.115860Z
    analyticsToken: string;
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
