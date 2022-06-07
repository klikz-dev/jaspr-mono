import { useContext, useEffect, useRef } from 'react';
import StoreContext from 'state/context/store';
import Segment from 'lib/segment';
import { getPreferences } from 'state/actions/user/getPreferences';

/**
 * Monitors for user changes.
 * @return null
 */
const UserMonitor = (): null => {
    const [store, dispatch] = useContext(StoreContext);
    const previousAnalyticsToken = useRef<string>(null);
    const { user } = store;

    useEffect(() => {
        if (user.userType === 'patient' && previousAnalyticsToken.current !== user.analyticsToken) {
            Segment.identify(user.analyticsToken, {
                userType: user.userType,
                system: user.location.system.name,
                systemId: user.location.system.id,
                clinic: user.location.clinic?.name,
                clinicId: user.location.clinic?.id,
                department: user.location.department?.name,
                departmentId: user.location.department?.id,
                activities: user.activities,
            });
            previousAnalyticsToken.current = user.analyticsToken;

            getPreferences(dispatch);
        } else if (
            user.userType === 'technician' &&
            previousAnalyticsToken.current !== user.analyticsToken
        ) {
            Segment.identify(user.analyticsToken, {
                userType: user.userType,
                system: user.location.system.name,
                systemId: user.location.system.id,
                role: user.role,
            });
            previousAnalyticsToken.current = user.analyticsToken;
        } else if (user.userType === '') {
            previousAnalyticsToken.current = null;
        }
    }, [dispatch, user]);

    return null;
};

export default UserMonitor;
