import { useState, useEffect } from 'react';
import { getStorageItem, setStorageItem } from './';

/** useState hook backed by local storage */
export const useLocalStorage = (
    key: string,
    initialValue: string,
): [string, (value: string) => void] => {
    const [item, setItem] = useState(initialValue);

    useEffect(() => {
        getStorageItem(key).then((value) => {
            setItem(value || initialValue);
        });
    }, [key, initialValue]);

    const setValue = (value: string) => {
        setItem(value);
        setStorageItem(key, value);
    };

    return [item, setValue];
};

export default useLocalStorage;
