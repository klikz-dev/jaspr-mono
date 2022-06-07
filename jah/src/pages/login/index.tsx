import React, { useRef, useCallback, useState, useEffect, useContext } from 'react';
import StoreContext from 'state/context/store';
import { loginAction } from 'state/actions/user';
import { Platform, TextInput } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as LocalAuthentication from 'expo-local-authentication';
import axios from 'axios';
import Styled from 'styled-components/native';
import { useHistory, Link } from 'lib/router';
import { useLocalStorage } from 'lib/storage/useLocalStorage';
import Storage from 'lib/storage';
import { setToken, getMe } from 'state/actions/user';
import { displayError } from 'state/actions/error';
import Logo from 'assets/logo.svg';
import styles from './login.module.css';
import { Patient } from 'state/types';

const StyledLogin = Styled.View`${styles.login}; background-color: #3b4a67`;
const StyledContainer = Styled.KeyboardAvoidingView`${styles.container} flex: 1;`;
const StyledLogoContainer = Styled.View`${styles.logo}; margin: auto;`;
const StyledForm = Styled.View`${styles.form} flex: 1;`;
const ScrollView = Styled.ScrollView``;
const InputContainer = Styled.View`${styles.inputContainer}`;
const StyledInput = Styled.TextInput`${styles.input}`;
const StyledError = Styled.Text`${styles.error}`;
const StyledForgot = Styled.Text`${styles.forgot}`;
const SubmitButton = Styled.TouchableOpacity`${styles.submitButton}`;
const SubmitText = Styled.Text`${styles.submitText}`;
const Label = Styled.Text`${styles.label}`;

const KeepMeLoggedInRow = Styled.TouchableOpacity`flex-direction: row; align-items: center;`;
const KeepMeLoggedInLabel = Styled.Text`margin-left: 15px; color: #fff; font-size: 20px;`;
const CheckboxOuter = Styled.View`
    margin-left: 20px;
    width: 20px;
    height: 20px;
    border-color: white;
    border-width: 1px;
    align-items: center;
    justify-content: center;
`;
const CheckboxInner = Styled.View`
    width: 12px;
    height: 12px;
    background-color: ${({ checked }: { checked: boolean }) =>
        checked ? '#179BB0' : 'transparent'} 
`;
const SignupButton = Styled.TouchableOpacity`${styles.signupButton}; margin-bottom: 20px;`;
const SignupButtonText = Styled.Text`${styles.signupButtonText}`;
const SignupRule = Styled.View`${styles.signupRule}`;
const Strong = Styled.Text`font-weight: 600`;

const Login = () => {
    const history = useHistory();
    const passwordRef = useRef<TextInput>(null);
    const [compatible, setCompatible] = useState(false);
    const [enrolled, setEnrolled] = useState(false);
    const [checkingCapabilities, setCheckingCapabilities] = useState(true);
    const [hasFingerprint, setHasFingerprint] = useState(false);
    const [hasFace, setHasFace] = useState(false);
    const [successfullyAuthenticated, setSuccessfullyAuthenticated] = useState(false);
    const [authenticationInProgress, setAuthenticationInProgress] = useState(false);
    const [userCancelledAuthentication, setUserCancelledAuthentication] = useState(false);
    const [fingerprintErrorCount, setFingerprintErrorCount] = useState(0);
    const [keepMeLoggedIn, setKeepMeLoggedIn] = useLocalStorage('keepMeLoggedIn', 'false');
    const [credentialsStored, setCredentialsStored] = useLocalStorage('credentialsStored', 'false');
    const [store, dispatch] = useContext(StoreContext);
    const { device, user } = store;
    const { authenticated } = user as Patient;
    const { isTablet } = device;
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [loggingIn, setLoggingIn] = useState<boolean>(false);
    const [loginError, setLoginError] = useState<string>('');

    const handleLogin = async () => {
        setLoggingIn(true);
        let response;
        response = await loginAction(dispatch, username, password);

        if (response?.status === 400 || response?.status === 403) {
            // @ts-ignore We know this is always the ErrorResponse.  How to assert?
            const json: {
                nonFieldErrors?: string[];
                email?: string[];
                password?: string[];
                detail?: string;
            } = response?.data;

            if (json?.email?.length) {
                setLoginError(json.email[0]);
            } else if (json?.password?.length) {
                setLoginError(json.password[0]);
            } else if (json.nonFieldErrors && json.nonFieldErrors.length > 0) {
                setLoginError(json.nonFieldErrors[0]);
            } else if (json.detail) {
                setLoginError(json.detail);
            } else {
                setLoginError('There was an unknown error');
            }
        }
    };

    useEffect(() => {
        if (authenticated) {
            history.push('/');
        }
    }, [authenticated, history]);

    useEffect(() => {
        setUsername('');
        setPassword('');
    }, []);

    const handleLogout = () => {
        dispatch({ type: 'RESET_APP' });
    };

    const login = () => {
        if (keepMeLoggedIn === 'true') {
            setCredentialsStored('true');
        }
        handleLogin();
    };

    const checkDeviceForHardwareAuthMechanism = useCallback(async () => {
        const compatible = await LocalAuthentication.hasHardwareAsync();
        const enrolled = await LocalAuthentication.isEnrolledAsync();
        const [hasFingerprint, hasFace] =
            await LocalAuthentication.supportedAuthenticationTypesAsync();
        setCompatible(compatible);
        setEnrolled(enrolled);
        setHasFingerprint(!!hasFingerprint); // 1 to boolean
        setHasFace(!!hasFace); // 2 to boolean
        setCheckingCapabilities(false);
    }, []);

    const cancelAuthentication = () => {
        if (Platform.OS === 'android') {
            LocalAuthentication.cancelAuthenticate();
        }
    };

    const restoreSession = useCallback(async () => {
        const token = await Storage.getSecureItem('token');
        if (token) {
            axios.defaults.headers.common['Authorization'] = `Token ${token}`;
            setToken(dispatch, token);
            getMe(dispatch);
        }
    }, [dispatch]);

    const scanBiometrics = useCallback(async () => {
        if (
            !successfullyAuthenticated &&
            !authenticationInProgress &&
            !userCancelledAuthentication
        ) {
            try {
                setAuthenticationInProgress(true);
                const result = await LocalAuthentication.authenticateAsync({
                    promptMessage: 'Sign-in to Jaspr',
                });
                if (result.success) {
                    setSuccessfullyAuthenticated(true);
                    restoreSession();
                }
            } catch (e) {
                if (e.error === 'lockout') {
                    // To many attempts on device and OS lockout
                    // TODO Show fail message and tell to login with PW
                    setAuthenticationInProgress(false);
                } else if (e.error === 'user_cancel') {
                    setUserCancelledAuthentication(true);
                } else {
                    setFingerprintErrorCount(fingerprintErrorCount + 1);
                    setAuthenticationInProgress(false);
                    cancelAuthentication();
                    if (fingerprintErrorCount + 1 === 3) {
                        // Jaspr reset threshold
                        // TODO Show try again message?
                    } else if (fingerprintErrorCount + 1 >= 5) {
                        // TODO Cancel alert in Android
                        // TODO Show fail message and tell to login with PW
                        // Device auto lockout
                    } else {
                        //scanBiometrics();
                    }
                }
                console.log('error authenticating', e);
                displayError(dispatch);
            }
        }
    }, [
        successfullyAuthenticated,
        authenticationInProgress,
        userCancelledAuthentication,
        restoreSession,
        fingerprintErrorCount,
        dispatch,
    ]);

    useEffect(() => {
        checkDeviceForHardwareAuthMechanism();
    }, [checkDeviceForHardwareAuthMechanism]);

    useEffect(() => {
        if (credentialsStored === 'true' && compatible && enrolled && !authenticated) {
            scanBiometrics();
        } else if (
            !checkingCapabilities &&
            credentialsStored === 'true' &&
            !enrolled &&
            !authenticated
        ) {
            restoreSession();
        } else {
            cancelAuthentication();
        }
    }, [
        credentialsStored,
        scanBiometrics,
        restoreSession,
        compatible,
        enrolled,
        hasFingerprint,
        hasFace,
        authenticated,
        checkingCapabilities,
    ]);

    useEffect(() => {
        return cancelAuthentication;
    }, []);

    return (
        <StyledLogin>
            <LinearGradient style={{ flex: 1 }} colors={['#383C58', '#4C526B']}>
                <StyledContainer
                    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                    style={{ flex: 1 }}
                >
                    <StyledForm>
                        <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
                            <StyledLogoContainer>
                                <Logo width="85" height="85" />
                            </StyledLogoContainer>

                            {!authenticated && (
                                <>
                                    <SignupRule style={{ marginTop: 15 }} />
                                    <StyledForgot>Don't have a mobile account?</StyledForgot>
                                    <SignupButton onPress={() => history.push('/jah-signup')}>
                                        <SignupButtonText>Set Your Password</SignupButtonText>
                                    </SignupButton>
                                    <SignupRule style={{ marginBottom: 15 }} />
                                    <Label>Email</Label>
                                    <InputContainer>
                                        <StyledInput
                                            autoCompleteType="email"
                                            autoCapitalize="none"
                                            keyboardType="email-address"
                                            value={username}
                                            returnKeyType="next"
                                            textContentType="username"
                                            onChangeText={(e) => {
                                                setUsername(e);
                                            }}
                                            onSubmitEditing={() =>
                                                passwordRef.current && passwordRef.current.focus()
                                            }
                                        />
                                    </InputContainer>
                                    <Label>Password</Label>
                                    <InputContainer>
                                        <TextInput
                                            autoCompleteType="password"
                                            ref={passwordRef}
                                            autoCapitalize="none"
                                            value={password}
                                            secureTextEntry={true}
                                            returnKeyType="go"
                                            textContentType="password"
                                            onChangeText={(e) => {
                                                setPassword(e);
                                            }}
                                            onSubmitEditing={login}
                                        />
                                    </InputContainer>
                                    <KeepMeLoggedInRow
                                        onPress={() =>
                                            setKeepMeLoggedIn(
                                                keepMeLoggedIn === 'true' ? 'false' : 'true',
                                            )
                                        }
                                    >
                                        <CheckboxOuter>
                                            <CheckboxInner checked={keepMeLoggedIn === 'true'} />
                                        </CheckboxOuter>
                                        <KeepMeLoggedInLabel>Keep me logged in</KeepMeLoggedInLabel>
                                    </KeepMeLoggedInRow>
                                    <StyledError>{loginError}</StyledError>
                                    <SubmitButton onPress={login}>
                                        <SubmitText>Login</SubmitText>
                                    </SubmitButton>
                                    <Link to="/jah-forgot-password">
                                        <StyledForgot>
                                            Forgot your password? <Strong>Click here</Strong>
                                        </StyledForgot>
                                    </Link>
                                </>
                            )}
                            {authenticated && (
                                <SubmitButton onPress={handleLogout}>
                                    <SubmitText>Logout</SubmitText>
                                </SubmitButton>
                            )}
                        </ScrollView>
                    </StyledForm>
                </StyledContainer>
            </LinearGradient>
        </StyledLogin>
    );
};

export default Login;
