import React, { useEffect, useState, useRef } from 'react';
import { useHistory } from 'lib/router';
import axios from 'axios';
import config from 'config';
import { Keyboard, TextInput, TouchableWithoutFeedback } from 'react-native';
import Styled from 'styled-components/native';
import Menu from 'components/HamburgerMenu';
import Button from '../button';
import Check from './check.svg';
import styles from './index.module.scss';

const DismissKeyboard = ({ children }: { children: React.ReactNode }) => (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss}>{children}</TouchableWithoutFeedback>
);

const StyledContainer = Styled.View`${styles.container}`;
const StyledBox = Styled.View`${styles.box} flex: 1;`;
const StyledForm = Styled.View`${styles.form}`;
const StyledHeader = Styled.TouchableOpacity`${styles.header}`;
const HeaderText = Styled.Text`${styles.headerText}`;
const FormField = Styled.View``;
const FormHeader = Styled.View`${styles.formHeader}`;
const FormHeaderText = Styled.Text``;
const StyledInput = Styled.TextInput<{ last?: boolean }>`${styles.input} ${({ last }) =>
    last
        ? `
    border-bottom-width: 1px;
    border-bottom-color: #c4c4c4;
    `
        : ''}`;
const StyledButtons = Styled.View`${styles.buttons}`;
const StyledError = Styled.Text`${styles.error}`;
const StyledOverlay = Styled.View`${styles.overlay} top: 0px; bottom: 0;`;
const StyledOverlayBox = Styled.View`${styles.overlayBox}`;
const Text = Styled.Text``;

const ChangePassword = (): JSX.Element => {
    const history = useHistory();
    const newPasswordRef = useRef<TextInput>(null!);
    const confirmNewPasswordRef = useRef<TextInput>(null!);
    const [error, setError] = useState('');
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [submitted, setSubmitted] = useState(false);
    const [fade, setFade] = useState(false);
    const [confirmNewPassword, setConfirmNewPassword] = useState('');

    useEffect(() => {
        if (submitted) {
            const fadeTimer = setTimeout(() => setFade(true), 2000); // global
            const awayTimer = setTimeout(() => history.push('/account'), 3000); // global
            return () => {
                clearTimeout(fadeTimer); // global
                clearTimeout(awayTimer); // global
            };
        }
    }, [history, submitted]);

    const submit = async () => {
        if (!currentPassword) {
            setError('Your current password is required');
            return;
        }
        if (!newPassword) {
            setError('You must set a new password');
            return;
        }
        if (!confirmNewPassword) {
            setError('You must confirm your new password');
            return;
        }
        if (newPassword !== confirmNewPassword) {
            setError('New passwords do not match, please try again');
            return;
        }

        try {
            await axios.post(`${config.apiRoot}/patient/change-password`, {
                currentPassword,
                password: newPassword,
            });
            setSubmitted(true);
        } catch (err) {
            const json = err.response.data;
            if (json.nonFieldErrors && json.nonFieldErrors?.length > 0) {
                setError(json.nonFieldErrors[0]);
            } else if (json.currentPassword) {
                setError(json.currentPassword[0]);
            } else if (json.password) {
                setError(json.password[0]);
            } else {
                setError(json.detail);
            }
            setSubmitted(false);
        }
    };

    const cancel = () => {
        history.push('/account');
    };

    return (
        <StyledContainer>
            <Menu />
            <DismissKeyboard>
                <StyledBox>
                    <StyledForm>
                        <StyledHeader onPress={() => history.push('/account')}>
                            <HeaderText style={{ fontSize: 33 }}>‹</HeaderText>
                            <HeaderText style={{ marginLeft: 'auto', marginRight: 'auto' }}>
                                Change Password
                            </HeaderText>
                        </StyledHeader>
                        <FormField>
                            <FormHeader>
                                <FormHeaderText>Current password</FormHeaderText>
                            </FormHeader>
                            <StyledInput
                                value={currentPassword}
                                secureTextEntry={true}
                                autoCapitalize="none"
                                returnKeyType="next"
                                textContentType="password"
                                onChangeText={(value) => {
                                    setError('');
                                    setCurrentPassword(value);
                                }}
                                onSubmitEditing={() => newPasswordRef.current.focus()}
                            />
                        </FormField>
                        <FormField>
                            <FormHeader>
                                <FormHeaderText>New password</FormHeaderText>
                            </FormHeader>
                            <StyledInput
                                // @ts-ignore
                                ref={newPasswordRef}
                                value={newPassword}
                                autoCapitalize="none"
                                returnKeyType="next"
                                textContentType="password"
                                secureTextEntry={true}
                                onChangeText={(value) => {
                                    setError('');
                                    setNewPassword(value);
                                }}
                                onSubmitEditing={() => confirmNewPasswordRef.current.focus()}
                            />
                        </FormField>
                        <FormField>
                            <FormHeader>
                                <FormHeaderText>Confirm new password</FormHeaderText>
                            </FormHeader>
                            <StyledInput
                                // @ts-ignore
                                ref={confirmNewPasswordRef}
                                value={confirmNewPassword}
                                autoCapitalize="none"
                                secureTextEntry={true}
                                returnKeyType="go"
                                textContentType="password"
                                onChangeText={(value) => {
                                    setError('');
                                    setConfirmNewPassword(value);
                                }}
                                onSubmitEditing={submit}
                                last
                            />
                        </FormField>
                    </StyledForm>

                    <StyledButtons>
                        <StyledError>{error}</StyledError>
                        <Button onClick={submit} label="Submit" />
                        <Button onClick={cancel} label="Cancel" primary={false} />
                    </StyledButtons>

                    {submitted && (
                        <StyledOverlay>
                            <StyledOverlayBox>
                                <Check />
                                <Text>Password change successful</Text>
                            </StyledOverlayBox>
                        </StyledOverlay>
                    )}
                </StyledBox>
            </DismissKeyboard>
        </StyledContainer>
    );
};

export default ChangePassword;
