export interface Device {
    loaded?: boolean;
    isTablet?: boolean;
    code?: string;
    codeType?: 'system' | 'department' | null;
    inPatientContext?: boolean;
    isEhrEmbedded?: boolean;
    patientContextId?: number | null;
    updateAvailable?: boolean;
}
