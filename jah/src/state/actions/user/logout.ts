import axios, { AxiosResponse } from 'axios';
import config from 'config';
import Segment from 'lib/segment';
import { UserConstants } from 'state/constants';
import { Dispatch } from 'state/types';

export const logout = async (
    dispatch: Dispatch,
    userType?: 'patient' | '' | null,
    manuallyInitiated: boolean | null = null,
): Promise<AxiosResponse> => {
    Segment.track('logout');
    Segment.reset();

    const url: string = `${config.apiRoot}/patient/logout`;

    let response;
    try {
        response = await axios.post(url, manuallyInitiated ? { manuallyInitiated: true } : {});
        delete axios.defaults.headers.common['Authorization'];
    } catch (err) {
        response = err.response;
        delete axios.defaults.headers.common['Authorization'];
    } finally {
        dispatch({ type: UserConstants.RESET_APP });
        return response;
    }
};
