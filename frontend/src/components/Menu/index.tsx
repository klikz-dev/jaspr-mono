import { useContext } from 'react';
import { useHistory, useLocation } from 'lib/router';
import StoreContext from 'state/context/store';
import { addAction, actionNames } from 'state/actions/analytics';
import Hamburger from 'components/Hamburger';
import circleCheckIcon from 'assets/circle-check.svg';
import logo from 'assets/logo.png';
import { Patient } from 'state/types';
import Home from 'assets/icons/Home';
import Skills from 'assets/icons/Skills';
import Interview from 'assets/icons/Interview';
import Heart from 'assets/icons/Heart';
import Stories from 'assets/icons/Stories';
import styles from './menu.module.scss';

type Props = {
    selectedItem?: 'home' | 'stories' | 'skills' | 'cams' | 'takeaway';
    hideLogo?: boolean;
    dark?: boolean;
};

const routeToMenuAction = {
    '/': actionNames.MENU_HOME,
    '/stories': actionNames.MENU_SS,
    '/skills': actionNames.MENU_CS,
    '/question': actionNames.MENU_CAMS,
    '/takeaway': actionNames.MENU_TK,
};

const Menu = ({ selectedItem, hideLogo = false, dark = false }: Props) => {
    const history = useHistory();
    const location = useLocation();
    const [store] = useContext(StoreContext);
    const { pathname } = location;
    const { user, assessment } = store;
    const {
        timeSinceCheckin,
        //assessmentLockTimer,
        activities = { csp: false, csa: false, skills: false },
    } = user as Patient;

    const isPath3 = !activities.csa && !activities.csp;

    const { assessmentLocked, currentSectionUid } = assessment;

    const blacklist = ['/question', '/breathe'];

    const navigate = (route: keyof typeof routeToMenuAction) => {
        if (route.startsWith('/question')) {
            addAction(routeToMenuAction['/question']);
        } else {
            addAction(routeToMenuAction[route]);
        }
        history.push(route);
    };

    // Not DRY.  Updates to logic need to be reflected in checkinMonitor and CUI
    const shouldShowCheckinDot = (): boolean => {
        if (/*assessmentLockTimer &&*/ !assessmentLocked && timeSinceCheckin >= 5) {
            return true;
        } else if (
            timeSinceCheckin >= 20 &&
            (currentSectionUid === 'ratePsych' || currentSectionUid === 'explore')
        ) {
            return true;
        }
        return false;
    };

    const shouldPulseCheckinDot = (): boolean => {
        if (
            timeSinceCheckin >= 30 &&
            !assessmentLocked &&
            (currentSectionUid === 'ratePsych' || currentSectionUid === 'explore')
        ) {
            return true;
        }
        return false;
    };

    return (
        <div className={`${styles.container} ${isPath3 ? styles.hidden : ''}`}>
            <Hamburger dark={dark} />
            {!isPath3 && (
                <div
                    className={styles.menu}
                    style={{ boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.1)' }}
                >
                    {!hideLogo && (
                        <div className={styles.logoContainer}>
                            <img
                                src={logo}
                                className={styles.logo}
                                itemProp="logo"
                                alt="Jaspr"
                                style={{ cursor: 'pointer' }}
                                onClick={() => history.push('/')}
                            />
                        </div>
                    )}
                    {(activities.skills || activities.csp) && (
                        <div
                            className={styles.item}
                            style={{ cursor: 'pointer' }}
                            data-selected={selectedItem === 'home'}
                            data-testid="menu-home"
                            onClick={() => navigate('/')}
                        >
                            <Home
                                height={36}
                                color={
                                    selectedItem === 'home'
                                        ? 'rgba(0,0,0,1)'
                                        : 'rgba(192, 193, 202, 1)'
                                }
                            />
                        </div>
                    )}
                    {activities.skills && (
                        <div
                            className={styles.item}
                            style={{ cursor: 'pointer' }}
                            data-selected={selectedItem === 'stories'}
                            data-testid="menu-stories"
                            onClick={() => navigate('/stories')}
                        >
                            <Stories
                                height={40}
                                color={
                                    selectedItem === 'stories'
                                        ? 'rgba(0,0,0,1)'
                                        : 'rgba(192, 193, 202, 1)'
                                }
                            />
                        </div>
                    )}
                    {activities.skills && (
                        <div
                            className={styles.item}
                            style={{ cursor: 'pointer' }}
                            data-selected={selectedItem === 'skills'}
                            data-testid="menu-skills"
                            onClick={() => navigate('/skills')}
                        >
                            <Skills
                                height={44}
                                color={
                                    selectedItem === 'skills'
                                        ? 'rgba(0,0,0,1)'
                                        : 'rgba(192, 193, 202, 1)'
                                }
                            />
                        </div>
                    )}
                    <div
                        className={styles.item}
                        style={{ cursor: 'pointer' }}
                        data-selected={selectedItem === 'cams'}
                        data-testid="menu-assessment"
                        onClick={() => navigate('/question')}
                    >
                        <Interview
                            height={44}
                            color={
                                selectedItem === 'cams' ? 'rgba(0,0,0,1)' : 'rgba(192, 193, 202, 1)'
                            }
                        />
                        {assessmentLocked && (
                            <img
                                src={circleCheckIcon}
                                alt="Interview Complete"
                                style={{
                                    position: 'absolute',
                                    top: 24,
                                    right: 14,
                                }}
                            />
                        )}

                        {!blacklist.includes(pathname) && shouldShowCheckinDot() && (
                            <div
                                className={`${styles.checkIn} ${
                                    shouldPulseCheckinDot() ? styles.pulse : ''
                                }`}
                                style={{ boxShadow: '0 2px 4px 3px #e62a76' }}
                            />
                        )}
                    </div>
                    {activities.csp && (
                        <div
                            className={styles.item}
                            style={{ cursor: 'pointer' }}
                            data-selected={selectedItem === 'takeaway'}
                            data-testid="menu-takeaway"
                            onClick={() => navigate('/takeaway')}
                        >
                            <Heart
                                height={38}
                                color={
                                    selectedItem === 'takeaway'
                                        ? 'rgba(0,0,0,1)'
                                        : 'rgba(192, 193, 202, 1)'
                                }
                            />
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export { routeToMenuAction, Menu };
export default Menu;
