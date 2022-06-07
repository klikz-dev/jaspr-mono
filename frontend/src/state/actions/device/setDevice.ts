import { DeviceConstants } from 'state/constants';
import { Device, Dispatch } from 'state/types';

export const setDevice = (dispatch: Dispatch, device: Device) => {
    return dispatch({ type: DeviceConstants.SET_DEVICE, ...device });
};
