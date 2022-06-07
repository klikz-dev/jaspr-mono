export const setSecureItem = (key: string, value: string) => {
    window.sessionStorage.setItem(key, value);
};

export const getSecureItem = (key: string): string | null => {
    if (key) {
        return window.sessionStorage.getItem(key);
    }
    return null;
};

export const removeSecureItem = (key: string) => {
    if (key) {
        window.sessionStorage.removeItem(key);
    }
};

export const clearSecure = (): void => {
    window.sessionStorage.clear();
};

const Storage = {
    setSecureItem,
    getSecureItem,
    removeSecureItem,
    removeStorageItem: removeSecureItem,
    clearSecure,
};

export default Storage;
