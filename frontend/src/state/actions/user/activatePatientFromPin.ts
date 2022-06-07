import axios, { AxiosResponse } from 'axios';
import config from '../../../config';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import Segment, { AnalyticNames } from 'lib/segment';
import { PostResponse } from 'state/types/api/patient/tablet-pin';

export const activatePatientFromPin = async (
    dispatch: Dispatch,
    codeType: 'system' | 'department' | undefined,
    code: string | undefined,
    pin: String,
): Promise<AxiosResponse> => {
    try {
        const response = await axios.post<PostResponse>(
            `${config.apiRoot}/patient/tablet-pin`,
            {
                departmentCode: codeType === 'department' ? code : undefined,
                systemCode: codeType === 'system' ? code : undefined,
                pinCode: pin,
            },
            { timeout: 10_000 },
        );

        const { patient, token, technicianOperated } = response.data;

        dispatch({ type: 'RESET_APP' });

        axios.defaults.headers.common['Authorization'] = `Token ${token}`;
        Segment.track(AnalyticNames.PATIENT_ACTIVATED_BY_PIN);

        dispatch({
            type: UserConstants.SET_TOKEN,
            token: token,
        });

        dispatch({
            type: UserConstants.ACTIVATE_PATIENT,
            token: token,
            patient: patient,
            technicianOperated,
        });

        return response;
    } catch (err) {
        // Rethrow the error so the appropriate error codes can be resolved
        // by the calling application
        throw err;
    }
};
