import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { Dispatch, SkillActivity } from 'state/types';
import { SkillsConstants } from 'state/constants';

const saveNewSkillActivity = async (
    dispatch: Dispatch,
    activity: number,
    saveForLater: boolean,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.post(`${config.apiRoot}/patient/patient-activities`, {
            activity,
            saveForLater,
        });
        const skillActivity: SkillActivity = response.data;
        dispatch({
            type: SkillsConstants.SAVE_SKILL_FOR_LATER,
            skillActivity,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};

const updateExistingSkillActivity = async (
    dispatch: Dispatch,
    id: number,
    activity: number,
    saveForLater: boolean,
): Promise<AxiosResponse> => {
    dispatch({
        type: SkillsConstants.SAVE_SKILL_FOR_LATER,
        skillActivity: { id, activity, saveForLater },
    });

    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.patch(`${config.apiRoot}/patient/patient-activities/${id}`, {
            activity,
            saveForLater,
        });
        const skillActivity: SkillActivity = response.data;
        dispatch({
            type: SkillsConstants.SAVE_SKILL_FOR_LATER,
            skillActivity,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};

export const saveSkillForLater = (
    dispatch: Dispatch,
    id: number | null,
    activity: number,
    saveForLater: boolean,
): Promise<AxiosResponse> => {
    if (id) {
        return updateExistingSkillActivity(dispatch, id, activity, saveForLater);
    }
    return saveNewSkillActivity(dispatch, activity, saveForLater);
};
