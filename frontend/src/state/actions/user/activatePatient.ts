import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { UserConstants, ErrorConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import Segment, { AnalyticNames } from 'lib/segment';
import Sentry from 'lib/sentry';
import { PostResponse } from 'state/types/api/technician/activate-patient';

export const activatePatient = async (
    dispatch: Dispatch,
    payload: {
        patient: number;
        department: number;
    },
    firstActivation: boolean,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.post<PostResponse>(
            `${config.apiRoot}/technician/activate-patient`,
            {
                ...payload,
            },
        );

        const json = response.data;

        Segment.track(
            firstActivation
                ? AnalyticNames.ACTIVATE_NEW_PATIENT
                : AnalyticNames.REACTIVATE_EXISTING_PATIENT,
            {
                department: payload.department,
                patient: json.patient.analyticsToken,
            },
        );

        dispatch({ type: 'RESET_APP' });

        axios.defaults.headers.common['Authorization'] = `Token ${json.token}`;

        dispatch({
            type: UserConstants.SET_TOKEN,
            token: json.token,
        });

        dispatch({
            type: UserConstants.ACTIVATE_PATIENT,
            token: json.token,
            patient: json.patient,
            technicianOperated: false,
        });
        return response;
    } catch (err) {
        const { response } = err;

        if (response.status === 500) {
            Sentry.captureException(err);
            dispatch({ type: ErrorConstants.SET_ERROR, showError: true });
        }

        return response;
    }
};
