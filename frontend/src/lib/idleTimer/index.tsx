import React, { useCallback, useContext, useEffect, useRef } from 'react';
import IdleTimer from 'react-idle-timer';
import throttle from 'lodash/throttle';
import Segment, { AnalyticNames } from 'lib/segment';
import { useHistory, useLocation } from 'react-router-dom';
import TimerContext from 'state/context/timer';
import StoreContext from 'state/context/store';
import { triggerHeartbeat, logout } from 'state/actions/user';

interface TimerProps {
    setShowTimeoutModal: (open: boolean) => void;
    children: React.ReactNode;
    timeout?: number;
}

const Timer = ({ setShowTimeoutModal, children }: TimerProps) => {
    const history = useHistory();
    const location = useLocation();
    const [store, dispatch] = useContext(StoreContext);
    const { authenticated, userType } = store.user;
    const { isEhrEmbedded } = store.device;
    const userTypeRef = useRef(userType);
    const authenticatedRef = useRef(authenticated);
    const timerRef = useRef<IdleTimer | null>(null);
    const throttleRef = useRef<ReturnType<typeof throttle> | null>(null);
    const shortTimeoutRoutes = ['/question'];

    // Set to 9 min for patients because they get a 1 minute warning popup which brings the timeout to 10 minutes
    let timeoutMs = (userType === 'technician' ? 10 : 9) * 1_000 * 60;

    if (shortTimeoutRoutes.includes(location.pathname)) {
        timeoutMs = 4 * 1_000 * 60;
    }

    useEffect(() => {
        userTypeRef.current = userType;
        authenticatedRef.current = authenticated;
        if (throttleRef.current) {
            // Cancel any queued events when authentication or usertype changes
            // to prevent sending a stale heartbeat
            throttleRef.current.cancel();
        }
    }, [userType, authenticated]);

    useEffect(() => {
        throttleRef.current = throttle(
            () => {
                if (authenticatedRef.current) {
                    triggerHeartbeat(dispatch, userTypeRef.current);
                }
            },
            60_000, // Once per minute
            { leading: true, trailing: true },
        );
        return () => {
            // Cancel queued events when unmounting
            if (throttleRef.current) {
                throttleRef.current.cancel();
            }
        };
    }, [dispatch]);

    const action = () => {
        if (throttleRef.current) {
            throttleRef.current();
        }
    };

    const onIdle = useCallback(
        (e) => {
            if (authenticated && userType === 'patient') {
                setShowTimeoutModal(true);
            } else if (authenticated && userType === 'technician') {
                Segment.track(AnalyticNames.LOG_OUT_TIMEOUT);
                if (isEhrEmbedded) {
                    history.push('/ehr-timeout');
                }
                logout(dispatch);
            }
        },
        [authenticated, userType, setShowTimeoutModal, isEhrEmbedded, dispatch, history],
    );

    const sendHeartbeat = useCallback(() => {
        if (authenticated) {
            triggerHeartbeat(dispatch, userType);

            if (timerRef.current) {
                timerRef.current.reset();
            }
        }
    }, [dispatch, userType, authenticated]);

    return (
        <>
            <IdleTimer
                // @ts-ignore // TODO Need version 4.6.4
                ref={timerRef}
                onIdle={onIdle}
                timeout={timeoutMs}
                onAction={action}
                onActive={action}
            />
            <TimerContext.Provider value={{ sendHeartbeat }}>
                {React.Children.map(children, (child) => {
                    if (React.isValidElement(child)) {
                        return React.cloneElement(child, { setShowTimeoutModal });
                    }
                    return child;
                })}
            </TimerContext.Provider>
        </>
    );
};

export default Timer;
