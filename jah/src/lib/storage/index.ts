import * as SecureStore from 'expo-secure-store';
import Sentry from 'lib/sentry';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const setSecureItem = async (key: string, value: string): Promise<boolean> => {
    if (key && value) {
        try {
            await SecureStore.setItemAsync(key, value, {
                keychainService: 'JASPR-SECURE',
                keychainAccessible: SecureStore.AFTER_FIRST_UNLOCK_THIS_DEVICE_ONLY,
            });
            return true;
        } catch (err) {
            Sentry.captureException(err);
            return false;
        }
    }
    return false;
};

export const getSecureItem = async (key: string): Promise<string | null> => {
    const value = await SecureStore.getItemAsync(key, {
        keychainService: 'JASPR-SECURE',
    });
    return value;
};

export const removeSecureItem = async (key: string): Promise<boolean> => {
    try {
        await SecureStore.deleteItemAsync(key, {
            keychainService: 'JASPR-SECURE',
        });
        return true;
    } catch (err) {
        Sentry.captureException(err);
        return false;
    }
};

export const clearSecure = (): void => {
    //AsyncStorage.clear(); // Note clears globally so we want to TODO
};

export const getStorageItem = async (name: string): Promise<string | null> => {
    try {
        const value = await AsyncStorage.getItem(name);
        if (value) {
            return JSON.parse(value)[name];
        }
        return value;
    } catch (error) {
        console.log('error retrieving storage item', error);
        return null;
    }
};

export const setStorageItem = async (name: string, value: string) => {
    try {
        await AsyncStorage.setItem(name, JSON.stringify({ [name]: value }));
    } catch (error) {
        console.log('error setting storage item', error);
    }
};

export const removeStorageItem = async (name: string) => {
    try {
        await AsyncStorage.removeItem(name);
    } catch (error) {
        console.log(error);
    }
};

const Storage = {
    setSecureItem,
    getSecureItem,
    removeSecureItem,
    clearSecure,
    getStorageItem,
    setStorageItem,
    removeStorageItem,
};

export default Storage;
