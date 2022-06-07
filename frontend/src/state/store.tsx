import React, { useMemo, useReducer } from 'react';
import StoreContext from 'state/context/store';
import { initialState as InitialReducerState } from 'state/reducers';
import { CombinedReducer, ActionResetApp } from './reducers';
import { Actions } from 'state/types';

interface StoreProps {
    children: React.ReactNode;
    rootReducer: (state: CombinedReducer, action: Actions | ActionResetApp) => void;
}

const Store = ({ rootReducer, children }: StoreProps) => {
    // @ts-ignore
    const initialState = rootReducer(InitialReducerState, { type: '__INIT__' });
    // @ts-ignore
    const [state, dispatch] = useReducer(rootReducer, initialState);
    const store = useMemo(() => [state, dispatch], [state]);
    // @ts-ignore
    return <StoreContext.Provider value={store}>{children}</StoreContext.Provider>;
};

export default Store;
