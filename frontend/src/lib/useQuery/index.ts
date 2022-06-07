import { useLocation } from 'lib/router';

/** Get a query parameter from the url */
export const useQuery = () => {
    const location = useLocation();
    return new URLSearchParams(location.search);
};
