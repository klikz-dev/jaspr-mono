import { useEffect } from 'react';
import { Alert } from 'react-native';

interface ConfirmLogoutModalProps {
    goBack: () => void;
    logout: () => void;
    confirmLogoutOpen: boolean;
}

const ConfirmLogoutModal = (props: ConfirmLogoutModalProps): null => {
    const { goBack, logout, confirmLogoutOpen } = props;

    useEffect(() => {
        if (confirmLogoutOpen) {
            Alert.alert(
                'Log out of Jaspr?',
                '',
                [
                    {
                        text: 'Log Out',
                        onPress: logout,
                    },
                    {
                        text: 'Cancel',
                        onPress: goBack,
                        style: 'cancel',
                    },
                ],
                { cancelable: false },
            );
        }
    }, [confirmLogoutOpen, logout, goBack]);

    return null;
};

export default ConfirmLogoutModal;
