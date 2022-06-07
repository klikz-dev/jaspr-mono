import { useEffect } from 'react';
import { useLocation } from 'lib/router';
import Segment from 'lib/segment';

const usePageView = () => {
    const location = useLocation();

    useEffect(() => {
        Segment.page(location.pathname);
    }, [location]);
};

const PageRouteMonitor = (): null => {
    usePageView();
    return null;
};

export default PageRouteMonitor;
