type Status = 'Not Assigned' | 'Not Started' | 'In Progress' | 'Completed' | 'Updated';

export type ResponsePatient = {
    id: number;
    currentSession: number | null;
    dateOfBirth: string; // 1985-10-11
    firstName: string;
    lastName: string;
    mrn: string;
    ssid: string;
    path: { srat: boolean | null; csp: boolean | null };
    departments: number[];
    mobilePhone: string;
    email: string;
    toolsToGoStatus: 'Not Started' | 'Email Sent' | 'Phone Number Verified' | 'Setup Finished';
    tourComplete: boolean;
    created: string; // 2020-07-14T19:50:46.273000Z
    lastLoggedInAt: string; // 2021-05-21T17:05:29.244777Z
    interviewProgressSection: 'Initial' | 'SSF-A/B' | 'Lethal Means' | 'Plan to Cope';
    status: {
        sratStatus?: Status;
        crisisStabilityPlan?: Status;
        lethalMeans?: Status;
        review?: Status;
    };
    statusChange: {
        srat?: string;
        lethalMeans?: string;
        crisisStabilityPlan?: string;
        review?: string;
        ehrNoteSent?: string;
    };
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
          dateOfBirth: string | null;
          mrn: string;
      }
);

export type ResponsePatients = ResponsePatient[];
