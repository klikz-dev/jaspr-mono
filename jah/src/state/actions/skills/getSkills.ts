import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { Dispatch, Skills } from 'state/types';
import { SkillsConstants } from 'state/constants';

export const getSkills = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get(`${config.apiRoot}/patient/activities`);
        const json: Skills = response.data;
        dispatch({
            type: SkillsConstants.SET_SKILLS,
            skills: json,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
