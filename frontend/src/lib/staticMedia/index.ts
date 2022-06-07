import { useEffect, useContext } from 'react';
import StoreContext from 'state/context/store';
import { getMedia } from 'state/actions/media';

/** Get static media assets from the server */
const StaticMedia = (): null => {
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { authenticated } = user;

    useEffect(() => {
        if (authenticated) {
            getMedia(dispatch);
        }
    }, [authenticated, dispatch]);
    return null;
};

export default StaticMedia;
