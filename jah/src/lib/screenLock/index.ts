import { useEffect } from 'react';
import * as ScreenOrientation from 'expo-screen-orientation';

/** Lock the screen on mobile native devices to portrait orientation */
const ScreenLock = (): null => {
    useEffect(() => {
        // Lock the screen to portrait mode.  We don't force this in the expo settings
        // because we need to unlock the video page to allow landscape viewing of videos
        const lock = async () => {
            await ScreenOrientation.lockAsync(ScreenOrientation.OrientationLock.PORTRAIT_UP);
        };
        lock();
    }, []);

    return null;
};

export default ScreenLock;
