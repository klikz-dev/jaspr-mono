import { useCallback, useContext, useEffect, useState } from 'react';
import Modal, { Styles } from 'react-modal';
import { useHistory, useLocation } from 'lib/router';
import { saveTimeSinceCheckin } from 'state/actions/user';
import { getAnswers } from 'state/actions/assessment';
import zIndexHelper from 'lib/zIndexHelper';
import jazIcon from 'assets/jazz.png';
import jasperIcon from 'assets/jasper.png';
import styles from './index.module.scss';
import { Patient } from 'state/types';

import StoreContext from 'state/context/store';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'space-evenly',
        backgroundColor: 'rgba(45, 44, 63, 0.0)',
        zIndex: zIndexHelper('patient.checkin-banner'),
        top: 16,
        height: 154,
        maxWidth: 679,
        margin: '0 auto',
    },
    content: {
        position: 'static',
        display: 'flex',
        flexDirection: 'column',
        width: '100%',
        height: '100%',
        alignSelf: 'center',
        borderRadius: 24,
        boxShadow: '0 9px 14px 7px rgba(0,0,0,0.5)',
    },
};

const CheckinMonitor = () => {
    const history = useHistory();
    const location = useLocation();
    const [store, dispatch] = useContext(StoreContext);
    const { pathname } = location;
    const { assessment, user } = store;
    const {
        authenticated,
        guide,
        userType,
        token,
        timeSinceCheckin,
        inEr,
        assessmentLockTimer,
        tourComplete,
        sessionLocked,
        activities = { csa: false, csp: false },
    } = user as Patient;
    const { /*answers,*/ assessmentLocked, currentSectionUid } = assessment;
    //const { checkInTime0 } = answers;

    const [snoozed, setSnoozed] = useState(false);
    const [startTime, setStartTime] = useState<Date>();

    const whitelist = ['/', '/stories', '/skills', '/takeaway'];

    const isPath3 = !activities.csa && !activities.csp;

    useEffect(() => {
        if (tourComplete) {
            setStartTime(new Date());
        }
    }, [tourComplete, assessmentLockTimer]);

    const checkTime = useCallback(() => {
        if (authenticated && startTime && userType === 'patient') {
            const now = +new Date();
            const diff = now - +startTime;
            const minutesSince = Math.round(diff / 1000 / 60); // minutes
            saveTimeSinceCheckin(dispatch, minutesSince);
        }
    }, [authenticated, startTime, userType, dispatch]);

    useEffect(() => {
        if (token && authenticated && userType === 'patient') {
            getAnswers(dispatch);
        }
    }, [authenticated, token, dispatch, userType]);

    // Update time since last checkin every minute
    useEffect(() => {
        checkTime();
        const timer = window.setInterval(() => {
            checkTime();
        }, 120 * 1000);
        return () => window.clearInterval(timer);
    }, [assessment, checkTime, dispatch]);

    const shouldShowBanner = () => {
        if (
            inEr &&
            !isPath3 &&
            !assessmentLocked &&
            !sessionLocked &&
            authenticated &&
            whitelist.includes(pathname)
        ) {
            if (
                timeSinceCheckin >= 20 &&
                (currentSectionUid === 'ratePsych' || currentSectionUid === 'explore') &&
                !snoozed
            ) {
                return true;
            }
        }
        return false;
    };

    const snooze = () => {
        if (
            timeSinceCheckin &&
            timeSinceCheckin >= 20 &&
            (currentSectionUid === 'ratePsych' || currentSectionUid === 'explore')
        ) {
            setSnoozed(true);
        }
    };

    const open = () => {
        snooze();
        history.push('/question');
    };

    return (
        <>
            <Modal isOpen={shouldShowBanner()} style={modalStyle}>
                <div className={styles.guideRow}>
                    <img
                        className={styles.guide}
                        src={guide === 'Jaz' ? jazIcon : jasperIcon}
                        alt={`Your guide ${guide || 'Jaz'}`}
                    />

                    <div className={styles.message}>
                        Hey there, just checking in - I'd like to ask you a few questions on the
                        interview page.
                    </div>
                </div>

                <div className={styles.buttons}>
                    <div className={styles.button} onClick={snooze}>
                        Snooze
                    </div>
                    <div className={styles.button} onClick={open}>
                        Open
                    </div>
                </div>
                <div className={styles.close} onClick={snooze}>
                    ⨉
                </div>
            </Modal>
        </>
    );
};

export { CheckinMonitor };
export default CheckinMonitor;
