import { useContext, useEffect } from 'react';
import { useHistory, useLocation } from 'lib/router';
import { setDevice } from 'state/actions/device';
import StoreContext from 'state/context/store';
import Segment, { AnalyticNames } from 'lib/segment';
import { Device } from 'state/types';

/**
 * DEPRECATED: We can remove this monitor after we have upgraded Providence and Allina to use the new tablet URLS
 * Monitors the environment to determine if this is a patient tablet running in a clinical setting.
 * Expects the dept and tablet=1 url paramters to be set in the webclip url used to launch the app.
 * @return null
 */
const ClinicMonitor = (): null => {
    const location = useLocation();
    const history = useHistory();
    const [, dispatch] = useContext(StoreContext);

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const deptId = params.get('dept');
        const systemId = params.get('system');
        const isTablet = Boolean(deptId || systemId);

        if (isTablet) {
            const device: Device = {
                isTablet,
                code: systemId || deptId,
                codeType: systemId ? 'system' : 'department',
            };
            setDevice(dispatch, device);
            Segment.track(AnalyticNames.SET_DEVICE, device);
            if (deptId) {
                window.sessionStorage.setItem('deptId', deptId);
            }

            if (systemId) {
                window.sessionStorage.setItem('systemId', systemId);
            }
        }
        // DEPRECATED.  This handles the old query parameters until all the old Providence and Allina
        // app installations can be upgraded
        if (location.pathname === '/start-patient-session' && isTablet) {
            history.replace(
                `/start-patient-session/${systemId ? 'system' : 'department'}/${
                    systemId ? systemId : deptId
                }`,
            );
        }
    }, [dispatch, history, location]);

    return null;
};

export default ClinicMonitor;
