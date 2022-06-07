import React, { useState, useEffect, useContext, useRef } from 'react';
import zIndexHelper from 'lib/zIndexHelper';
import Segment, { AnalyticNames } from 'lib/segment';
import ConfirmLogoutModal from 'components/ConfirmLogoutModal';
import { formatDate } from 'lib/helpers';
import LogoutIcon from 'assets/logoutIcon.png';
import CloseButton from 'assets/close.png';
import { addAction, actionNames } from 'state/actions/analytics';
import { useHistory } from 'lib/router';
import StoreContext from 'state/context/store';
import { logout } from 'state/actions/user';
import { Patient } from 'state/types';
import { Link } from 'react-router-dom';

import styles from './index.module.scss';

const Hamburger = ({ dark = false }: { dark?: boolean }) => {
    const menuRef = useRef<HTMLDivElement>(null);
    const history = useHistory();
    const [menuOpen, setMenuOpen] = useState(false);
    const [confirmLogoutOpen, setConfirmLogoutOpen] = useState(false);
    const [store, dispatch] = useContext(StoreContext);

    const { device, user } = store;
    const {
        firstName,
        lastName,
        dateOfBirth,
        ssid,
        userType,
        sessionLocked,
        hasSecuritySteps,
        tourComplete,
        activities = { csp: false, csa: false, skills: false },
    } = user as Patient;
    const { isEhrEmbedded } = device;
    const { location } = history;
    const { pathname } = location;
    const isPath3 = !activities.csa && !activities.csp;

    enum Routes {
        HOME = '/',
        STORIES = '/stories',
        SKILLS = '/skills',
        ASSESSMENT = '/question',
        TAKEAWAY = '/takeaway',
        ACCOUNT = '/account',
        JAH_STABILITY_PLAN = '/jah-stability-playlist',
        JAH_CONTACTS = '/jah-contacts',
        JAH_WALKTHROUGH = '/jah-walkthrough',
    }

    const linkToMenuAction = {
        [Routes.HOME]: actionNames.HAMBURGER_HOME,
        [Routes.STORIES]: actionNames.HAMBURGER_SS,
        [Routes.SKILLS]: actionNames.HAMBURGER_CS,
        [Routes.ASSESSMENT]: actionNames.HAMBURGER_CAMS,
        [Routes.TAKEAWAY]: actionNames.HAMBURGER_TK,
        [Routes.ACCOUNT]: actionNames.HAMBURGER_MY_ACCOUNT,
        [Routes.JAH_STABILITY_PLAN]: actionNames.HAMBURGER_STABILITY_PLAN,
        [Routes.JAH_CONTACTS]: actionNames.HAMBURGER_CONTACTS,
        [Routes.JAH_WALKTHROUGH]: actionNames.HAMBURGER_WALKTHROUGH,
    };

    const goBack = () => setConfirmLogoutOpen(false);
    const doLogout = () => {
        Segment.track(AnalyticNames.LOG_OUT_BY_USER);
        logout(dispatch, userType, true);
        history.push('/');
    };

    const onLogout = async () => {
        setMenuOpen(false);
        if (userType === 'patient') {
            setConfirmLogoutOpen(true);
        } else {
            const shouldGoToEhrLockout = isEhrEmbedded;
            Segment.track(AnalyticNames.LOG_OUT_BY_USER);
            await logout(dispatch, userType);
            history.push(shouldGoToEhrLockout ? '/ehr-timeout' : '/');
        }
    };

    const onLinkClick = (
        e: React.TouchEvent | React.MouseEvent | null,
        to: Routes,
        ready: boolean,
    ) => {
        if (e && !ready) {
            e.preventDefault();
        } else if (to.startsWith('/question')) {
            addAction(linkToMenuAction['/question']);
        } else {
            addAction(linkToMenuAction[to]);
        }
    };

    useEffect(() => {
        // Close menu when clicking outside of menu
        const clickOutside = (e: MouseEvent) => {
            if (e.target && menuRef?.current && menuRef.current.contains(e.target as Node)) {
                return;
            }
            setMenuOpen(false);
        };

        if (menuOpen) {
            document.addEventListener('mousedown', clickOutside, false);
            document.addEventListener('touchstart', clickOutside, false);
        } else {
            document.removeEventListener('mousedown', clickOutside, false);
            document.removeEventListener('touchstart', clickOutside, false);
        }
        return () => {
            document.removeEventListener('mousedown', clickOutside, false);
            document.removeEventListener('touchstart', clickOutside, false);
        };
    }, [menuOpen, menuRef, setMenuOpen]);

    const availableHome =
        hasSecuritySteps &&
        !sessionLocked &&
        (isPath3 || tourComplete) &&
        (activities.skills || activities.csp);
    const availableStories =
        hasSecuritySteps && (isPath3 || tourComplete) && !sessionLocked && activities.skills;
    const availableSkills =
        hasSecuritySteps && (isPath3 || tourComplete) && !sessionLocked && activities.skills;
    const availableTakeaway =
        hasSecuritySteps && (isPath3 || tourComplete) && !sessionLocked && activities.csp;
    const availableInterview =
        hasSecuritySteps &&
        (isPath3 || tourComplete) &&
        !sessionLocked &&
        (activities.csa || activities.csp);

    return (
        <>
            {menuOpen && (
                <div
                    className={styles.menu}
                    ref={menuRef}
                    style={{ boxShadow: '0 1px 4px 0 rgba(0,0,0,0.5)' }}
                >
                    <div className={styles.buttonBuffer}>
                        {menuOpen && (
                            <img
                                className={styles.closeButton}
                                style={{ cursor: 'pointer' }}
                                src={CloseButton}
                                alt="Close menu"
                                onClick={() => {
                                    Segment.track(AnalyticNames.OPEN_HAMBURGER_MENU);
                                    setMenuOpen(false);
                                }}
                            />
                        )}
                    </div>

                    <div className={styles.links}>
                        <Link
                            to={Routes.HOME}
                            className={`${styles.link} ${styles.linkText} ${
                                pathname === Routes.HOME ? styles.active : ''
                            } ${availableHome ? '' : styles.notReady}`}
                            onClick={(e) => onLinkClick(e, Routes.HOME, availableHome)}
                        >
                            Home
                        </Link>
                        <Link
                            to={Routes.SKILLS}
                            className={`${styles.link} ${styles.linkText} ${
                                pathname === Routes.SKILLS ? styles.active : ''
                            } ${availableSkills ? '' : styles.notReady}`}
                            onClick={(e) => onLinkClick(e, Routes.SKILLS, availableSkills)}
                        >
                            Comfort &amp; Skills
                        </Link>
                        <Link
                            to={Routes.STORIES}
                            className={`${styles.link} ${styles.linkText} ${
                                pathname === Routes.STORIES ? styles.active : ''
                            } ${availableStories ? '' : styles.notReady}`}
                            onClick={(e) => onLinkClick(e, Routes.STORIES, availableStories)}
                        >
                            Shared Stories
                        </Link>
                        {!isPath3 && (
                            <Link
                                to={Routes.ASSESSMENT}
                                className={`${styles.link} ${styles.linkText} ${
                                    pathname.indexOf(Routes.ASSESSMENT) > -1 ? styles.active : ''
                                } ${availableInterview ? '' : styles.notReady} ${styles.camsLink}`}
                                onClick={(e) =>
                                    onLinkClick(e, Routes.ASSESSMENT, availableInterview)
                                }
                            >
                                Suicide Status Interview
                            </Link>
                        )}
                        {!isPath3 && (
                            <Link
                                to={Routes.TAKEAWAY}
                                className={`${styles.link} ${styles.linkText} ${
                                    pathname === Routes.TAKEAWAY ? styles.active : ''
                                } ${availableTakeaway ? '' : styles.notReady}`}
                                onClick={(e) => onLinkClick(e, Routes.TAKEAWAY, availableTakeaway)}
                            >
                                Takeaway Kit
                            </Link>
                        )}
                        {user.userType === 'technician' && user.supportUrl && (
                            <a
                                className={`${styles.link} ${styles.linkText}`}
                                href={user.supportUrl}
                                rel="noopener noreferrer"
                            >
                                Support
                            </a>
                        )}
                        <a
                            className={`${styles.link} ${styles.linkText}`}
                            href="https://www.surveymonkey.com/r/J9KYF3T"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Report Adverse Event
                        </a>
                        <Link
                            to="#"
                            className={`${styles.linkText} ${styles.link} ${styles.logout}`}
                            onClick={onLogout}
                        >
                            <span>Log out</span>
                            <img
                                className={styles.logoutImage}
                                src={LogoutIcon}
                                alt="logout of JASPER"
                            />
                        </Link>
                    </div>

                    <div className={styles.patientInfo}>
                        {!sessionLocked && (
                            <>
                                {lastName}
                                {lastName && firstName ? ', ' : ''}
                                {firstName}
                                {ssid}
                                {dateOfBirth && (
                                    <>
                                        <br />({formatDate(dateOfBirth)})
                                    </>
                                )}
                            </>
                        )}
                        {/* @ts-ignore */}
                        {userType === 'technician' && (
                            <div className={styles.copyright}>
                                <span className={styles.copyrightText}>
                                    &#xA9; {new Date().getFullYear()} Jaspr Health
                                </span>
                            </div>
                        )}
                    </div>
                </div>
            )}
            {!menuOpen && (
                <div
                    className={styles.hamburger}
                    onClick={() => setMenuOpen(true)}
                    style={{ zIndex: zIndexHelper('patient.hamburger') }}
                >
                    <span className={`${styles.stack} ${dark ? styles.dark : ''}`} />
                    <span className={`${styles.stack} ${dark ? styles.dark : ''}`} />
                    <span className={`${styles.stack} ${dark ? styles.dark : ''}`} />
                </div>
            )}

            <ConfirmLogoutModal
                confirmLogoutOpen={confirmLogoutOpen}
                goBack={goBack}
                logout={doLogout}
            />
        </>
    );
};

export { Hamburger };
export default Hamburger;
