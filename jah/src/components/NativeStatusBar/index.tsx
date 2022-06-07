import React, { useContext } from 'react';
import { StatusBar } from 'expo-status-bar';
import StoreContext from 'state/context/store';

const NativeStatusBar = () => {
    const [store] = useContext(StoreContext);
    const { media } = store;
    const { isFullScreen } = media;

    return (
        <StatusBar
            translucent={false}
            backgroundColor="#2f344f"
            // eslint-disable-next-line react/style-prop-object
            style="light"
            hidden={isFullScreen}
        />
    );
};

export default NativeStatusBar;
