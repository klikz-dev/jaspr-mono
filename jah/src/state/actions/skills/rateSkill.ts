import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { Dispatch, SkillActivity } from 'state/types';
import { SkillsConstants } from 'state/constants';

const saveNewRating = async (
    dispatch: Dispatch,
    activity: number,
    rating: number,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.post(`${config.apiRoot}/patient/patient-activities`, {
            activity,
            rating,
        });
        const skillActivity: SkillActivity = response.data;
        dispatch({
            type: SkillsConstants.RATE_SKILL,
            skillActivity,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};

const updateExistingRating = async (
    dispatch: Dispatch,
    id: number,
    activity: number,
    rating: number,
): Promise<AxiosResponse> => {
    dispatch({ type: SkillsConstants.RATE_SKILL, skillActivity: { id, activity, rating } });

    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.patch(`${config.apiRoot}/patient/patient-activities/${id}`, {
            activity,
            rating,
        });
        const skillActivity: SkillActivity = response.data;
        dispatch({
            type: SkillsConstants.RATE_SKILL,
            skillActivity,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};

export const rateSkill = (
    dispatch: Dispatch,
    id: number | null,
    activity: number,
    rating: number,
): Promise<AxiosResponse> => {
    if (id) {
        return updateExistingRating(dispatch, id, activity, rating);
    }
    return saveNewRating(dispatch, activity, rating);
};
