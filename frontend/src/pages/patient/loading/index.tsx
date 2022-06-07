import { useContext, useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Modal, { Styles } from 'react-modal';
import StoreContext from 'state/context/store';
import zIndexHelper from 'lib/zIndexHelper';
import logo from 'assets/logo.svg';
import styles from './index.module.scss';

const fullScreenModalStyle: Styles = {
    overlay: {
        backgroundColor: 'rgba(0,0,0,0)',
        zIndex: zIndexHelper('patient.loading'),
    },
    content: {
        position: 'static',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        border: 'none',
        backgroundColor: 'transparent',
        padding: 0,
        height: '100%',
        width: '100%',
        overflow: 'hidden',
    },
};

const Loading = () => {
    const location = useLocation();
    const [store] = useContext(StoreContext);
    const { user, device } = store;
    const { code, codeType } = device;
    const { authenticated, userType } = user;
    const [percent, setPercent] = useState(0);
    const [complete, setComplete] = useState(false);
    const [open, setOpen] = useState(false);
    const prevUserType = useRef<'' | 'technician' | 'patient' | null>(null);

    // Open modal when usertype changes from technician to patient
    useEffect(() => {
        // Users won't be shown the loading screen if they are on the patient confirmation screen route.  They will
        // be shown the loading screen, when a patient has been loaded after the patient leaves the
        // confirmation page.  This is currently used to show a confirmation screen to the technician
        // when activating a patient via a pin
        if (!location.pathname.startsWith('/start-patient-session')) {
            if (prevUserType.current !== 'patient' && userType === 'patient') {
                setOpen(true);
            }
            prevUserType.current = userType;
        }
    }, [userType, location.pathname, codeType, code]);

    // Run through the progress bar
    useEffect(() => {
        if (open) {
            // Short delay to ensure the component is mounted and the css transition state fires
            const initialProgress = window.setTimeout(() => setPercent(32), 100);
            const firstProgress = window.setTimeout(() => setPercent(50), 600);
            const secondProgress = window.setTimeout(() => setPercent(76), 1300);
            const thirdProgress = window.setTimeout(() => setPercent(100), 1700);
            const completeProgress = window.setTimeout(() => setComplete(true), 2300);

            return () => {
                window.clearTimeout(initialProgress);
                window.clearTimeout(firstProgress);
                window.clearTimeout(secondProgress);
                window.clearTimeout(thirdProgress);
                window.clearTimeout(completeProgress);
            };
        }
    }, [open]);

    // Fade out the modal when the progress bar finishes
    useEffect(() => {
        if (complete) {
            const timeout = window.setTimeout(() => setOpen(false), 1000);
            return () => window.clearTimeout(timeout);
        }
    }, [complete]);

    // Reset the loading indicator after logging out
    useEffect(() => {
        if (!authenticated) {
            prevUserType.current = null;
            setPercent(0);
            setComplete(false);
            setOpen(false);
        }
    }, [authenticated]);

    return (
        <Modal isOpen={open} style={fullScreenModalStyle}>
            <div className={styles.container} style={{ opacity: complete ? 0 : 1 }}>
                <img className={styles.logo} src={logo} alt="" />
                <div className={styles.center}>
                    <div className={styles.message}>
                        {percent < 33 && <span>Logging out of staff account</span>}
                        {percent >= 33 && percent <= 100 && !complete && (
                            <span>Initiating patient session</span>
                        )}
                        {complete && <span>Loading Complete</span>}
                    </div>
                    <div className={styles.progress}>
                        <div className={styles.track} style={{ width: `${percent}%` }} />
                    </div>
                </div>
            </div>
        </Modal>
    );
};

export default Loading;
