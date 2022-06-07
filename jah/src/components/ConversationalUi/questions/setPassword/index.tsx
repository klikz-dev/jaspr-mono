import React, { useContext, useEffect, useRef, useState } from 'react';
import axios from 'axios';
import Segment from 'lib/segment';
import StoreContext from 'state/context/store';
import { setToken, setMe } from 'state/actions/user';
import config from 'config';
import { TextInput } from 'react-native';
import Styled from 'styled-components/native';
import { QuestionProps } from '../../question';
import { AnonymousUser } from 'state/types';
import styles from './index.module.scss';

const Container = Styled.View`${styles.container}`;
const Instruction = Styled.Text`${styles.instruction}`;
const Label = Styled.View`${styles.label}`;
const FieldTitle = Styled.Text`${styles['field-title']}`;
const Input = Styled.TextInput`${styles.input}`;

type SetPasswordProps = Pick<
    QuestionProps,
    'answered' | 'showValidation' | 'setShowValidation' | 'isValid' | 'setIsValid' | 'validate'
>;

const SetPasswordQuestion = (props: SetPasswordProps) => {
    const { answered, showValidation, setShowValidation, setIsValid, isValid, validate } = props;
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    // TODO Fix to use location state props?
    const { setupToken, alreadySetUp, setPasswordToken, setupUid } = user as AnonymousUser;
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const confirmPasswordRef = useRef() as React.MutableRefObject<TextInput>;

    useEffect(() => {
        const payload = {
            password,
            token: setupToken,
            uid: setupUid,
            setPasswordToken,
            authToken: true,
        };
        validate.current = () => {
            return new Promise((resolve, reject) => {
                if (!password) {
                    setShowValidation('Please provide a password.');
                    return reject();
                } else if (!confirmPassword) {
                    setShowValidation('Please confirm your password.');
                    return reject();
                } else if (password !== confirmPassword) {
                    setShowValidation('The two passwords do not match.');
                    return reject();
                }

                axios
                    .post(
                        `${config.apiRoot}/${
                            alreadySetUp
                                ? 'patient/reset-password/set-password'
                                : 'patient/set-password'
                        }`,
                        payload,
                    )
                    .then((response) => {
                        const { token, patient } = response.data;
                        if (token) {
                            axios.defaults.headers.common['Authorization'] = `Token ${token}`;
                            // Patients had to accept the policy to to the set password page.  We defer
                            // sending the API the acceptance until we are authenticated.  If workflows change
                            // where they can set their password without accepting the policy, then this will
                            // need to be moved.  Note, we set the token directly on the post even though
                            // we set the default above, because the change hasn't been affected yet on
                            // this instance of axios
                            axios.post(
                                `${config.apiRoot}/patient/accept-privacy-policy`,
                                {},
                                {
                                    headers: {
                                        Authorization: `Token ${token}`,
                                    },
                                },
                            );
                            setToken(dispatch, token);
                            setMe(dispatch, patient);
                        }
                        Segment.track('set-password', {
                            [alreadySetUp ? 'reset-password' : 'set-password']: 'success',
                        });
                        setIsValid(true);
                        resolve();
                    })
                    .catch((err) => {
                        const { data } = err.response;
                        const { nonFieldErrors, password, token, detail } = data;

                        if (password) {
                            setShowValidation(password?.join('\n'));
                        } else if (token) {
                            setShowValidation(token?.join('\n'));
                        } else if (detail) {
                            setShowValidation(detail);
                        } else if (nonFieldErrors) {
                            setShowValidation(nonFieldErrors?.join('\n'));
                        }
                        Segment.track('set-password', {
                            [alreadySetUp ? 'reset-password' : 'set-password']: 'failed',
                        });
                        reject();
                    });
            });
        };
    }, [
        password,
        confirmPassword,
        setupToken,
        setupUid,
        setPasswordToken,
        validate,
        alreadySetUp,
        setShowValidation,
        setIsValid,
        dispatch,
    ]);

    return (
        <Container>
            <Label>
                <FieldTitle>Password</FieldTitle>
                <Input
                    value={password}
                    secureTextEntry
                    editable={!answered}
                    autoCapitalize="none"
                    keyboardType="default"
                    returnKeyType="next"
                    textContentType="newPassword"
                    onChangeText={(e) => setPassword(e)}
                    onSubmitEditing={() => confirmPasswordRef.current.focus()}
                />
            </Label>

            <Label>
                <FieldTitle>Confirm Password</FieldTitle>
                <Input
                    maxLength={255}
                    secureTextEntry
                    keyboardType="default"
                    autoCapitalize="none"
                    returnKeyType="go"
                    value={confirmPassword}
                    editable={!answered}
                    ref={confirmPasswordRef as any}
                    textContentType="newPassword"
                    onChangeText={(e) => setConfirmPassword(e)}
                />
            </Label>

            {!isValid && Boolean(showValidation) && <Instruction>{showValidation}</Instruction>}
        </Container>
    );
};

export default SetPasswordQuestion;
