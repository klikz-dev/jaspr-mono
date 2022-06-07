import { useEffect } from 'react';
import modalStyles from '../layouts/modals/index.module.scss';

interface TimeoutModalProps {
    resetTimer: () => void;
    lockout: () => void;
    logout: () => void;
}

const TimeoutModal = (props: TimeoutModalProps): JSX.Element => {
    const { resetTimer, lockout, logout } = props;

    useEffect(() => {
        const timer = setTimeout(lockout, 60 * 1000);
        return () => clearTimeout(timer);
    }, [lockout]);

    return (
        <div className={modalStyles.modal}>
            <h2>Your session is about to expire</h2>
            <p>
                You've been inactive for a while. For your security, you will be logged out in
                approximately <strong>60 seconds</strong>.
            </p>
            <p>Tap "Continue" to stay logged in.</p>
            <div className={modalStyles.buttonGroup}>
                <div className={modalStyles.outlinedButton} onClick={logout}>
                    Log out
                </div>
                <div className={modalStyles.filledButton} onClick={resetTimer}>
                    Continue
                </div>
            </div>
        </div>
    );
};

export default TimeoutModal;
