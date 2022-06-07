import { useContext, useEffect, useCallback } from 'react';
import axios from 'axios';
import Storage from 'lib/storage';
import Segment, { AnalyticNames } from 'lib/segment';
import StoreContext from 'state/context/store';
import Modal, { Styles } from 'react-modal';
import { lockSession, logout, getMe, setToken } from 'state/actions/user';
import zIndexHelper from 'lib/zIndexHelper';
import TimeoutModal from 'components/TimeoutModal';
import LockoutModal from 'components/LockoutModal';
import { Patient } from 'state/types';
import { setDevice } from 'state/actions/device';

const modalTimeoutStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'space-evenly',
        backgroundColor: 'rgba(45, 44, 63, 0.85)',
        zIndex: zIndexHelper('patient.timeout'),
    },
    content: {
        position: 'static',
        display: 'flex',
        width: '523px',
        height: '286px',
        alignSelf: 'center',
    },
};

const modalLockStyle: Styles = {
    overlay: {
        display: 'flex',
        backgroundColor: 'rgba(0,0,0,1)',
        zIndex: zIndexHelper('patient.lockout'),
    },
    content: {
        position: 'static',
        display: 'flex',
        alignSelf: 'center',
        width: '100%',
        height: '100%',
        backgroundColor: 'transparent',
        border: 'none',
        borderRadius: 0,
        padding: 0,
    },
};

interface TimersProps {
    setShowTimeoutModal: (showTimeoutModal: boolean) => void;
    showTimeoutModal: boolean;
}

const Timers = ({ setShowTimeoutModal, showTimeoutModal }: TimersProps) => {
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { hasSecuritySteps, sessionLocked, userType } = user as Patient;

    const resetTimer = () => {
        setShowTimeoutModal(false);
    };

    const lock = useCallback(() => {
        setShowTimeoutModal(false);
        if (hasSecuritySteps && userType === 'patient') {
            Segment.track(AnalyticNames.SESSION_LOCKED);
            lockSession(dispatch);
        } else {
            Segment.track(AnalyticNames.SESSION_TIMEOUT);
            logout(dispatch, userType, false);
        }
    }, [dispatch, hasSecuritySteps, setShowTimeoutModal, userType]);

    const logoutCallback = useCallback(() => {
        setShowTimeoutModal(false);
        // This is from a button press from the timeout modal right now,
        // so it is manually initiated.
        Segment.track(AnalyticNames.LOG_OUT_BY_USER);
        logout(dispatch, userType, true);
    }, [dispatch, setShowTimeoutModal, userType]);

    // Application startup functions.  Check if the app is loaded and restore state
    useEffect(() => {
        (async () => {
            const token = Storage.getSecureItem('token');
            if (token) {
                // Do not include user here as it may be changing from localstorage.
                // It'll get updated with the getme
                setToken(dispatch, token);
                axios.defaults.headers.common['Authorization'] = `Token ${token}`;
                const response = await getMe(dispatch);
                if (response.status === 403) {
                    Storage.removeSecureItem('token');
                    delete axios.defaults.headers.common['Authorization'];
                    dispatch({ type: 'RESET_APP' });
                }
            }
            setDevice(dispatch, { loaded: true });
        })();
    }, [dispatch]);

    return (
        <>
            <Modal isOpen={showTimeoutModal} style={modalTimeoutStyle}>
                <TimeoutModal resetTimer={resetTimer} lockout={lock} logout={logoutCallback} />
            </Modal>
            <Modal isOpen={sessionLocked || false} style={modalLockStyle}>
                <LockoutModal />
            </Modal>
        </>
    );
};

export default Timers;
