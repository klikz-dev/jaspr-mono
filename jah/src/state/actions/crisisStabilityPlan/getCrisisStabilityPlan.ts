import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { CrisisStabilityPlanConstants } from 'state/constants';
import { Dispatch } from 'state/types';

export const getCrisisStabilityPlan = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get(`${config.apiRoot}/patient/crisis-stability-plan`);
        const crisisStabilityPlan = response.data;
        dispatch({
            type: CrisisStabilityPlanConstants.SET_CRISIS_STABILITY_PLAN,
            crisisStabilityPlan,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
