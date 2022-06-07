import React, { useContext } from 'react';
import * as Linking from 'expo-linking';
import { useHistory } from 'lib/router';
import Sentry from 'lib/sentry';
import Styled from 'styled-components/native';
import Menu from 'components/HamburgerMenu';
import styles from './index.module.scss';
import StoreContext from 'state/context/store';
import { Patient } from 'state/types';

const StyledContainer = Styled.View`${styles.container}}`;
const StyledBox = Styled.View`${styles.box}`;
const StyledHeader = Styled.View`${styles.header}`;
const StyledHeaderText = Styled.Text`${styles.headerText}`;
const StyledEmail = Styled.View`${styles.email}`;
const StyledEmailColumn = Styled.Text`${styles.emailColumn}`;
const StyledNavButton = Styled.TouchableOpacity`${styles.navButton}`;
const StyledNavButtonColumn = Styled.Text`${styles.navButtonColumn}`;
const StyledNavLink = Styled.TouchableOpacity`${styles.navLink}`;

const Account = () => {
    const history = useHistory();
    const [store] = useContext(StoreContext);
    const { user } = store;
    const { email } = user as Patient;

    const openExternalLink = (url: string) => {
        Linking.openURL(url).catch((err) => {
            Sentry.captureException(err.message);
        });
    };

    return (
        <StyledContainer>
            <Menu />
            <StyledBox>
                <StyledHeader>
                    <StyledHeaderText>My Account</StyledHeaderText>
                </StyledHeader>
                <StyledEmail>
                    <StyledEmailColumn style={{ fontWeight: 'bold' }}>Email</StyledEmailColumn>
                    <StyledEmailColumn>{email}</StyledEmailColumn>
                </StyledEmail>
                <StyledNavButton onPress={() => history.push('/change-password')}>
                    <>
                        <StyledNavButtonColumn style={{ fontWeight: 'bold' }}>
                            Change Password
                        </StyledNavButtonColumn>
                        <StyledNavButtonColumn style={{ fontSize: 33 }}>›</StyledNavButtonColumn>
                    </>
                </StyledNavButton>
                <StyledNavLink
                    onPress={() => openExternalLink('https://jasprhealth.com/terms-of-service/')}
                >
                    <>
                        <StyledNavButtonColumn style={{ fontWeight: 'bold' }}>
                            Terms and Conditions
                        </StyledNavButtonColumn>
                        <StyledNavButtonColumn style={{ fontSize: 33 }}>›</StyledNavButtonColumn>
                    </>
                </StyledNavLink>
                <StyledNavLink
                    onPress={() => openExternalLink('https://jasprhealth.com/privacy-policy/')}
                >
                    <>
                        <StyledNavButtonColumn style={{ fontWeight: 'bold' }}>
                            Privacy Policy
                        </StyledNavButtonColumn>
                        <StyledNavButtonColumn style={{ fontSize: 33 }}>›</StyledNavButtonColumn>
                    </>
                </StyledNavLink>
            </StyledBox>
        </StyledContainer>
    );
};

export default Account;
