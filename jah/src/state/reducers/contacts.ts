import { ContactsConstants } from 'state/constants';
import { CommonConcern } from 'state/types';

import { ActionSetConversationStarters, ActionSetCommonConerns } from 'state/types/actions';

type ContactsReducerType = ActionSetConversationStarters | ActionSetCommonConerns;

export interface ContactsReducerState {
    starters: Array<string>;
    concerns: CommonConcern[];
}

const initialState: ContactsReducerState = {
    starters: [],
    concerns: [],
};

const ContactsReducer = (
    state: ContactsReducerState = initialState,
    action: ContactsReducerType,
): ContactsReducerState => {
    switch (action.type) {
        case ContactsConstants.SET_CONVERSATION_STARTERS:
            return { ...state, starters: action.starters.map((starter) => starter.content) };
        case ContactsConstants.SET_COMMON_CONCERNS:
            return {
                ...state,
                concerns: action.concerns,
            };
        default:
            return state;
    }
};

export { ContactsReducer, initialState };
