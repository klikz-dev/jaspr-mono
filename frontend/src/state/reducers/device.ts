import { DeviceConstants } from 'state/constants';
import { ActionSetDevice } from 'state/types/actions';

export interface DeviceReducerState {
    loaded: boolean;
    isTablet: boolean;
    code: string;
    codeType: 'system' | 'department' | null;
    inPatientContext: boolean;
    isEhrEmbedded: boolean;
    patientContextId: number | null;
    updateAvailable: boolean;
}

type DeviceReducerType = ActionSetDevice;

const code = window.sessionStorage.getItem('code');
const codeType = window.sessionStorage.getItem('codeType');

const initialState: DeviceReducerState = {
    loaded: false,
    isTablet: Boolean(code), // Indicates if this device is used by patients.
    code: code || null,
    // @ts-ignore
    codeType: ['system', 'department'].includes(codeType) ? codeType : null,
    inPatientContext: false, // Indicates if the EHR embedded session was launched with a specific patient context.  For now, this is always true if isEhrEmbedded is true
    isEhrEmbedded: false, // Indicates that the Device is embedded (iFrame) within an EHR instance.  If true, this will never be a patient device
    patientContextId: null,
    updateAvailable: false,
};

const DeviceReducer = (
    state: DeviceReducerState = initialState,
    action: DeviceReducerType,
): DeviceReducerState => {
    const { type, ...rest } = action;
    switch (
        action.type // TODO Fix constant after merging in typescript branch
    ) {
        case DeviceConstants.SET_DEVICE:
            return {
                ...state,
                ...rest,
            };
        default:
            return state;
    }
};

export { DeviceReducer, initialState };
