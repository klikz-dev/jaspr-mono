import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { CrisisStabilityPlanConstants } from 'state/constants';
import { CrisisStabilityPlan, Dispatch } from 'state/types';

export const saveCrisisStabilityPlan = async (
    dispatch: Dispatch,
    updatedCrisisStabilityPlan: Partial<CrisisStabilityPlan>,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));

    try {
        dispatch({
            type: CrisisStabilityPlanConstants.SET_CRISIS_STABILITY_PLAN,
            crisisStabilityPlan: updatedCrisisStabilityPlan,
        });
        const response = await axios.patch(
            `${config.apiRoot}/patient/crisis-stability-plan`,
            updatedCrisisStabilityPlan,
        );
        const crisisStabilityPlan = response.data;

        dispatch({
            type: CrisisStabilityPlanConstants.SET_CRISIS_STABILITY_PLAN,
            crisisStabilityPlan,
        });
        return response;
    } catch (err) {
        const { response } = err;
        // No extra error handling
        return response;
    }
};
