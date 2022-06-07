import React, { useState, useContext, MouseEvent, TouchEvent } from 'react';
import Segment from 'lib/segment';
import { addAction, actionNames } from 'state/actions/analytics';
import { useHistory } from 'lib/router';
import { SafeAreaView, GestureResponderEvent, TouchableOpacity, View } from 'react-native';
import { Modal } from 'react-native';
import { Link } from 'react-router-native';
import * as Linking from 'expo-linking';
import Styled from 'styled-components/native';
import ConfirmLogoutModal from 'components/ConfirmLogoutModal';
import CloseButton from 'assets/close.png';
import StoreContext from 'state/context/store';
import { logout } from 'state/actions/user';
import { Patient } from 'state/types';
import styles from './index.module.scss';

const StyledMenu = Styled.View`${styles.menu}; height: 100%; top: 0; background-color: #383c58;`;
const StyledBufferButtons = Styled.View`${styles.buttonBuffer}
    background-color: #383c58;
`;
const StyledCloseButton = Styled.Image`${styles.closeButton}
    margin-top: 10px;
`;
const StyledLinks = Styled.View`
    padding: 20px;
    padding-bottom: 100px;
`;
const StyledLink = Styled(Link)`${styles.link}`;
const StyledLinkText = Styled.Text`${styles.linkText}`;
const StyledHamburger = Styled.TouchableOpacity<{ inline: boolean }>`${({ inline }) =>
    styles.hamburger}
`;
const StyledStack = Styled.View`${styles.stack}`;
const StyledCopyright = Styled.View`${styles.copyright}`;
const StyledCopyrightText = Styled.Text`${styles.copyrightText}`;

const Hamburger = ({ inline = false }: { inline?: boolean }) => {
    const history = useHistory();
    const [menuOpen, setMenuOpen] = useState(false);
    const [confirmLogoutOpen, setConfirmLogoutOpen] = useState(false);
    const [store, dispatch] = useContext(StoreContext);

    const { device, user } = store;
    const { userType, tourComplete } = user as Patient;
    const { isEhrEmbedded } = device;

    // TODO Not all these routes exist in JAH
    enum Routes {
        HOME = '/',
        STORIES = '/stories',
        SKILLS = '/skills',
        ASSESSMENT = '/question',
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
        [Routes.ACCOUNT]: actionNames.HAMBURGER_MY_ACCOUNT,
        [Routes.JAH_STABILITY_PLAN]: actionNames.HAMBURGER_STABILITY_PLAN,
        [Routes.JAH_CONTACTS]: actionNames.HAMBURGER_CONTACTS,
        [Routes.JAH_WALKTHROUGH]: actionNames.HAMBURGER_WALKTHROUGH,
    };

    const goBack = () => setConfirmLogoutOpen(false);
    const doLogout = () => {
        Segment.track(actionNames.LOG_OUT_BY_USER);
        logout(dispatch, userType, true);
        history.push('/login');
    };

    const onLogout = () => {
        setMenuOpen(false);
        if (userType === 'patient') {
            setConfirmLogoutOpen(true);
        } else {
            const shouldGoToEhrLockout = isEhrEmbedded;
            Segment.track(actionNames.LOG_OUT_BY_USER);
            logout(dispatch, userType);
            history.push(shouldGoToEhrLockout ? '/ehr-timeout' : '/login');
        }
    };

    const onLinkClick = (e: GestureResponderEvent | null, to: Routes, ready: boolean) => {
        if (e && !ready) {
            e.preventDefault();
        } else if (to.startsWith('/question')) {
            addAction(linkToMenuAction['/question']);
        } else {
            addAction(linkToMenuAction[to]);
        }
    };

    const openAdverseEvents = (e: GestureResponderEvent | null, to: Routes, ready: boolean) => {
        if (e) {
            e.preventDefault();
        }
        Linking.openURL('https://www.surveymonkey.com/r/J9KYF3T');
    };

    return (
        <>
            <Modal visible={menuOpen} animationType="none" transparent={false}>
                <SafeAreaView style={{ backgroundColor: '#383c58' }}>
                    <View style={{ flex: 0, height: '100%', backgroundColor: 'green' }}>
                        <StyledMenu>
                            <SafeAreaView>
                                <StyledBufferButtons>
                                    <TouchableOpacity
                                        onPress={() => setMenuOpen(false)}
                                        hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
                                    >
                                        <StyledCloseButton source={CloseButton} />
                                    </TouchableOpacity>
                                </StyledBufferButtons>
                            </SafeAreaView>

                            <StyledLinks>
                                <StyledLink
                                    to={Routes.HOME}
                                    onClick={(e: GestureResponderEvent) =>
                                        onLinkClick(e, Routes.HOME, tourComplete)
                                    }
                                    component={TouchableOpacity}
                                    hitSlop={{ top: 10, bottom: 10 }}
                                >
                                    <StyledLinkText>Home</StyledLinkText>
                                </StyledLink>

                                <StyledLink
                                    to={Routes.STORIES}
                                    onPress={(e: GestureResponderEvent) =>
                                        onLinkClick(e, Routes.STORIES, tourComplete)
                                    }
                                    component={TouchableOpacity}
                                    hitSlop={{ top: 10, bottom: 10 }}
                                >
                                    <StyledLinkText>Shared Stories</StyledLinkText>
                                </StyledLink>
                                <StyledLink
                                    to={Routes.JAH_STABILITY_PLAN}
                                    onPress={(e: GestureResponderEvent) =>
                                        onLinkClick(e, Routes.JAH_STABILITY_PLAN, tourComplete)
                                    }
                                    component={TouchableOpacity}
                                    hitSlop={{ top: 10, bottom: 10 }}
                                >
                                    <StyledLinkText>Stability Plan</StyledLinkText>
                                </StyledLink>
                                <StyledLink
                                    to={Routes.JAH_WALKTHROUGH}
                                    onPress={(e: GestureResponderEvent) =>
                                        onLinkClick(e, Routes.JAH_WALKTHROUGH, tourComplete)
                                    }
                                    component={TouchableOpacity}
                                    hitSlop={{ top: 10, bottom: 10 }}
                                >
                                    <StyledLinkText>Distress Survival Guide</StyledLinkText>
                                </StyledLink>

                                <StyledLink
                                    to={Routes.SKILLS}
                                    onPress={(e: GestureResponderEvent) =>
                                        onLinkClick(e, Routes.SKILLS, tourComplete)
                                    }
                                    component={TouchableOpacity}
                                    hitSlop={{ top: 10, bottom: 10 }}
                                >
                                    <StyledLinkText>Comfort &amp; Skills</StyledLinkText>
                                </StyledLink>
                                <StyledLink
                                    to={Routes.JAH_CONTACTS}
                                    onPress={(e: GestureResponderEvent) =>
                                        onLinkClick(e, Routes.JAH_CONTACTS, tourComplete)
                                    }
                                    component={TouchableOpacity}
                                    hitSlop={{ top: 10, bottom: 10 }}
                                >
                                    <StyledLinkText>Contacts</StyledLinkText>
                                </StyledLink>

                                <StyledLink
                                    to={Routes.ACCOUNT}
                                    onPress={(e: GestureResponderEvent) =>
                                        onLinkClick(e, Routes.ACCOUNT, tourComplete)
                                    }
                                    component={TouchableOpacity}
                                    hitSlop={{ top: 10, bottom: 10 }}
                                >
                                    <StyledLinkText>My Account</StyledLinkText>
                                </StyledLink>

                                <StyledLink
                                    to=""
                                    onPress={openAdverseEvents}
                                    component={TouchableOpacity}
                                    hitSlop={{ top: 10, bottom: 10 }}
                                >
                                    <StyledLinkText>Report Adverse Event</StyledLinkText>
                                </StyledLink>

                                <StyledLink
                                    to="#"
                                    onPress={onLogout}
                                    component={TouchableOpacity}
                                    hitSlop={{ top: 10, bottom: 10 }}
                                >
                                    <StyledLinkText>Log out</StyledLinkText>
                                </StyledLink>
                            </StyledLinks>
                            <StyledCopyright>
                                <StyledCopyrightText>&#xA9; 2021 Jaspr Health</StyledCopyrightText>
                            </StyledCopyright>
                        </StyledMenu>
                    </View>
                </SafeAreaView>
            </Modal>

            {!menuOpen && (
                <SafeAreaView>
                    <View style={{ flex: 1 }}>
                        <StyledHamburger
                            onPress={() => setMenuOpen(true)}
                            inline={inline}
                            hitSlop={{ top: 20, bottom: 20, left: 20, right: 20 }}
                        >
                            <StyledStack />
                            <StyledStack />
                            <StyledStack />
                        </StyledHamburger>
                    </View>
                </SafeAreaView>
            )}

            <ConfirmLogoutModal
                goBack={goBack}
                logout={doLogout}
                confirmLogoutOpen={confirmLogoutOpen}
            />
        </>
    );
};

export default Hamburger;
