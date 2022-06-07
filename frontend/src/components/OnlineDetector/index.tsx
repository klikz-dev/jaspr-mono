import { useEffect, useContext, useRef } from 'react';
import { toggleOnline } from 'state/actions/user';
import StoreContext from 'state/context/store';

const OnlineDetector = (): null => {
    const [, dispatch] = useContext(StoreContext);
    const timeOffline = useRef(0);

    // Detect when Jaspr if offline
    useEffect(() => {
        const toggleOn = () => {
            const secondsOffline = (new Date().getTime() - timeOffline.current) / 1000;
            toggleOnline(dispatch, true, Math.round(secondsOffline));
            timeOffline.current = 0;
        };

        const toggleOff = () => {
            timeOffline.current = new Date().getTime();
            toggleOnline(dispatch, false);
        };

        window.addEventListener('online', toggleOn);
        window.addEventListener('offline', toggleOff);
        return () => {
            window.removeEventListener('online', toggleOn);
            window.removeEventListener('offline', toggleOff);
        };
    }, [dispatch]);
    return null;
};

export default OnlineDetector;
