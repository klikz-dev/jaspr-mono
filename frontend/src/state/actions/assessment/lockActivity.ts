import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import Segment, { AnalyticNames } from 'lib/segment';
import config from '../../../config';
import { Dispatch } from 'state/types';
import { AssessmentConstants } from 'state/constants';
import { AssignedActivity } from 'components/ConversationalUi/questions';

export const lockActivity = async (
    dispatch: Dispatch,
    activity: AssignedActivity,
): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    // Mark activity locked locally to prevent render issues while request is pending
    dispatch({
        type: AssessmentConstants.UPDATE_ACTIVITIES,
        activity: { ...activity, locked: true },
    });

    const response = await axios.patch<AssignedActivity>(
        `${config.apiRoot}/patient/interview-activity/${activity.id}`,
        {
            locked: true,
        },
    );
    const updatedActivity = response.data;
    dispatch({ type: AssessmentConstants.UPDATE_ACTIVITIES, activity: updatedActivity });
    Segment.track(AnalyticNames.LOCK_ACTIVITY, {
        userType: 'patient',
        activity: activity.type,
        locked: true,
    });
    return response;
};
