import { useEffect, useState } from 'react';
import * as LocalAuthentication from 'expo-local-authentication';

interface RequestPermissionProps {
    permission: string; // TODO more specific
}

const RequestPermission = ({ permission }: RequestPermissionProps): null => {
    const [requestMade, setRequestMade] = useState(false);

    useEffect(() => {
        const getLocalAuthenticationPermission = async () => {
            if (!requestMade) {
                setRequestMade(true);
                await LocalAuthentication.authenticateAsync({
                    promptMessage: 'Sign-in to Jaspr',
                });
            }
        };

        if (permission === 'local authentication') {
            getLocalAuthenticationPermission();
        }
    }, [permission, requestMade, setRequestMade]);
    return null;
};

export default RequestPermission;
