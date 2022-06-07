import { DeviceConstants } from 'state/constants';
import { ActionSetDevice } from 'state/types/actions';

export interface DeviceReducerState {
    isTablet: boolean;
    deptId?: string;
    inPatientContext: boolean;
    isEhrEmbedded: boolean;
}

type DeviceReducerType = ActionSetDevice;

const initialState: DeviceReducerState = {
    isTablet: false, // Indicates if this device is used by patients.
    inPatientContext: false, // Indicates if the EHR embedded session was launched with a specific patient context.  For now, this is always true if isEhrEmbedded is true
    isEhrEmbedded: false, // Indicates that the Device is embedded (iFrame) within an EHR instance.  If true, this will never be a patient device
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
