import axios, { AxiosResponse } from 'axios';
import { errorInterceptor } from 'lib/api';
import config from 'config';
import { ContactsConstants } from 'state/constants';
import { ConversationStarter, Dispatch } from 'state/types';

type ConversationStarters = ConversationStarter[];

export const getConversationStarters = async (dispatch: Dispatch): Promise<AxiosResponse> => {
    axios.interceptors.response.use(...errorInterceptor(dispatch));
    try {
        const response = await axios.get(`${config.apiRoot}/conversation-starters`);
        const json: ConversationStarters = response.data;
        dispatch({
            type: ContactsConstants.SET_CONVERSATION_STARTERS,
            starters: json,
        });
        return response;
    } catch (error) {
        const { response } = error;
        // No extra error handling
        return response;
    }
};
