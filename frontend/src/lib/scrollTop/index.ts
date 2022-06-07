import { useEffect } from 'react';
import { useLocation } from 'lib/router';

/** Scroll to the top of the page when the route changes */
const ScrollToTop = (): null => {
    const { pathname } = useLocation();

    useEffect(() => {
        window.scrollTo(0, 0);
    }, [pathname]);

    return null;
};

export default ScrollToTop;
