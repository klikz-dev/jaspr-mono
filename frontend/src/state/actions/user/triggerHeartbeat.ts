import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { PostResponse as TechnicianPostResponse } from 'state/types/api/technician/heartbeat';
import { PostResponse as PatientPostResponse } from 'state/types/api/patient/heartbeat';

const triggerPatientHeartbeat = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    try {
        const response = await axios.post<PatientPostResponse>(
            `${config.apiRoot}/patient/heartbeat`,
            {},
        );
        dispatch({
            type: UserConstants.HEARTBEAT,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};

const triggerTechnicianHeartbeat = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    try {
        const response = await axios.post<TechnicianPostResponse>(
            `${config.apiRoot}/technician/heartbeat`,
            {},
        );
        dispatch({
            type: UserConstants.HEARTBEAT,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};

export const triggerHeartbeat = async (
    dispatch: Dispatch,
    userType?: 'technician' | 'patient' | '',
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    if (userType === 'technician') {
        return triggerTechnicianHeartbeat(dispatch);
    } else if (userType === 'patient') {
        return triggerPatientHeartbeat(dispatch);
    }
    // Unknown user type
    return await new Promise((resolve, reject) => reject());
};
