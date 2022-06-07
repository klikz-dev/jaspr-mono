import axios, { AxiosResponse } from 'axios';
import config from '../../../config';
import Segment, { AnalyticNames } from 'lib/segment';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';
import { removeSecureItem } from 'lib/storage';
import { PostResponse as TechnicianPostResponse } from 'state/types/api/technician/logout';
import { PostResponse as PatientPostResponse } from 'state/types/api/patient/logout';

export const logout = async (
    dispatch: Dispatch,
    userType?: 'patient' | 'technician' | '' | null, // TODO Cleanup
    manuallyInitiated: boolean | null = null,
): Promise<AxiosResponse> => {
    Segment.track(AnalyticNames.LOGOUT);
    Segment.reset();

    // Remove the token from local storage immediatly, in case the application is refreshed before the logout completes
    removeSecureItem('token');

    const url: string =
        userType === 'patient'
            ? `${config.apiRoot}/patient/logout`
            : `${config.apiRoot}/technician/logout`;

    let response;
    try {
        response = await axios.post<TechnicianPostResponse | PatientPostResponse>(
            url,
            manuallyInitiated ? { manuallyInitiated: true } : {},
        );
        delete axios.defaults.headers.common['Authorization'];
    } catch (err) {
        response = err.response;
        delete axios.defaults.headers.common['Authorization'];
    } finally {
        dispatch({ type: UserConstants.RESET_APP });
        return response;
    }
};
