import { useEffect, useContext } from 'react';
import NetInfo from '@react-native-community/netinfo';
import { toggleOnline } from 'state/actions/user';
import StoreContext from 'state/context/store';

const OnlineDetector = (): null => {
    const [, dispatch] = useContext(StoreContext);
    // Detect when Jaspr if offline
    useEffect(() => {
        const unsubscribe = NetInfo.addEventListener((state) => {
            toggleOnline(dispatch, state.isConnected);
        });

        return unsubscribe;
    }, [dispatch]);
    return null;
};

export default OnlineDetector;
