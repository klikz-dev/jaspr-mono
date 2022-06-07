import React, { useEffect } from 'react';

const useClickOutside = (
    ref: React.RefObject<HTMLDivElement>,
    callback: () => any,
    enabled: boolean = true,
) => {
    useEffect(() => {
        const listener = (event: MouseEvent): void => {
            // Do nothing if clicking inside ref
            // @ts-ignore
            if (!ref.current || ref.current.contains(event.target)) {
                return;
            }

            // Run callback if clicking outside ref;
            event.stopPropagation();
            callback();
        };

        if (enabled) {
            document.addEventListener('mousedown', listener);
            document.addEventListener('touchstart', listener);
        }

        return () => {
            document.removeEventListener('mousedown', listener);
            document.removeEventListener('touchstart', listener);
        };
    }, [ref, enabled, callback]);
};

export default useClickOutside;
