import { useContext, useEffect, useState } from 'react';
import * as serviceWorkerRegistration from '../../serviceWorkerRegistration';
import Segment, { AnalyticNames } from 'lib/segment';
import StoreContext from 'state/context/store';
import { setDevice } from 'state/actions/device';

interface ServiceWorkerEvent extends Event {
    target: (Partial<ServiceWorker> & EventTarget) | null;
}

const useServiceWorker = (): [boolean, () => void] => {
    const [, dispatch] = useContext(StoreContext);
    const [registration, setRegistration] = useState<ServiceWorkerRegistration | null>(null);

    useEffect(() => {
        if (registration) {
            const interval = window.setInterval(() => {
                registration.update();
            }, 5000 /*15 * 60 * 1_000*/); // Check for new update every 15 minutes
            return () => window.clearInterval(interval);
        }
    }, [registration]);

    useEffect(() => {
        serviceWorkerRegistration.register({
            onRegistration: (registration) => setRegistration(registration),
            onUpdate: (registration) => {
                const { waiting } = registration;
                if (waiting) {
                    waiting.addEventListener('statechange', (event: ServiceWorkerEvent) => {
                        if (event.target.state === 'activated') {
                            Segment.track(AnalyticNames.APP_UPDATE_AVAILABLE);
                            setDevice(dispatch, { updateAvailable: true });
                        }
                    });
                    // Tell the service worker to update the service worker.  This doesn't update the site
                    // to the latest version immediately, but makes it so the new content will be applied
                    // during the next refresh
                    waiting.postMessage({ type: 'SKIP_WAITING' });
                }
            },
            onSuccess: (registration) => console.log('success', registration),
        });
    }, [dispatch]);

    return null;
};

export default useServiceWorker;
