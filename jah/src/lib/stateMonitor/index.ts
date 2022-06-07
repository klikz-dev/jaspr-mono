import { useEffect } from 'react';
import { AppState, AppStateStatus } from 'react-native';
import Segment from 'lib/segment';

/** Monitor app state on native and report to analytics */
const StateMonitor = (): null => {
    useEffect(() => {
        const recordAppState = (state: AppStateStatus) => {
            Segment.track('jah-state-change', {
                state,
            });
            if (state === 'active') {
                Segment.track('APP_LOADED');
            }
        };

        AppState.addEventListener('change', recordAppState);

        return () => AppState.removeEventListener('change', recordAppState);
    }, []);

    return null;
};

export default StateMonitor;
