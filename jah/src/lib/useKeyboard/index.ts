import { useEffect, useState } from 'react';
import { Keyboard, KeyboardEvent } from 'react-native';

/** Returns the height of the onscreen keyboard */
export const useKeyboard = (): [number] => {
    const [keyboardHeight, setKeyboardHeight] = useState(0);

    function onKeyboardWillShow(e: KeyboardEvent): void {
        setKeyboardHeight(e.endCoordinates.height);
    }

    function onKeyboardWillHide(): void {
        setKeyboardHeight(0);
    }

    useEffect(() => {
        Keyboard.addListener('keyboardWillShow', onKeyboardWillShow);
        Keyboard.addListener('keyboardWillHide', onKeyboardWillHide);
        return (): void => {
            Keyboard.removeListener('keyboardWillShow', onKeyboardWillShow);
            Keyboard.removeListener('keyboardWillHide', onKeyboardWillHide);
        };
    }, []);

    return [keyboardHeight];
};
