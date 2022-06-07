import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from '../../../config';
import { Dispatch, SkillActivity } from 'state/types';
import { SkillsConstants } from 'state/constants';
import { PostResponse } from 'state/types/api/patient/patient-activities';
import { PatchResponse } from 'state/types/api/patient/patient-activities/_id';

const saveNewSkillActivity = async (
    dispatch: Dispatch,
    activity: number,
    saveForLater: boolean,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.post<PostResponse>(
            `${config.apiRoot}/patient/patient-activities`,
            {
                activity,
                saveForLater,
            },
        );
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
        const response = await axios.patch<PatchResponse>(
            `${config.apiRoot}/patient/patient-activities/${id}`,
            {
                activity,
                saveForLater,
            },
        );
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
