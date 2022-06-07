import React, { useContext, useEffect, useRef, useState } from 'react';
import axios from 'axios';
import Segment from 'lib/segment';
import StoreContext from 'state/context/store';
import { updateMe } from 'state/actions/user';
import config from 'config';
import Styled from 'styled-components/native';
import { TextInput } from 'react-native';
import { QuestionProps } from '../../question';
import styles from './index.module.css';

const Container = Styled.View`${styles.container}`;
const Instruction = Styled.Text`${styles.instruction}`;
const Label = Styled.View`${styles.label}`;
const FieldTitle = Styled.Text`${styles['field-title']}`;
const Input = Styled.TextInput`${styles.input}`;

export type AccountActivationProps = Pick<
    QuestionProps,
    'answered' | 'showValidation' | 'isValid' | 'setIsValid' | 'validate' | 'setShowValidation'
> & {};

const AccountActivation = (props: AccountActivationProps) => {
    const { answered, showValidation, setShowValidation, setIsValid, validate, isValid } = props;
    const [, dispatch] = useContext(StoreContext);
    const [mobilePhone, setMobilePhone] = useState('');
    const [email, setEmail] = useState('');
    const phoneNumberRef = useRef<TextInput>(null!);

    useEffect(() => {
        const payload = {
            email,
            mobilePhone,
        };
        validate.current = () => {
            setShowValidation(false);
            return new Promise((resolve, reject) => {
                if (!email) {
                    setShowValidation('You must enter your email address');
                    return reject();
                }
                if (!mobilePhone) {
                    setShowValidation('You must enter your phone number');
                    return reject();
                }
                axios
                    .post(`${config.apiRoot}/patient/native-verify-phone-number`, payload)
                    .then((response) => {
                        updateMe(dispatch, '', payload);
                        setIsValid(true);
                        Segment.track('account-activation', {
                            phone_verified: 'success',
                        });
                        resolve();
                    })
                    .catch((err) => {
                        const { data } = err.response;
                        const { nonFieldErrors, email, mobilePhone } = data;

                        if (email) {
                            setShowValidation(email?.join('\n'));
                        } else if (mobilePhone) {
                            setShowValidation(mobilePhone?.join('\n'));
                        } else if (nonFieldErrors) {
                            setShowValidation(nonFieldErrors?.join('\n'));
                        } else {
                            setShowValidation('There was an error processing your request');
                        }
                        Segment.track('account-activation', {
                            phone_verified: 'failed',
                        });

                        reject();
                    });
            });
        };
    }, [mobilePhone, email, validate, setShowValidation, dispatch, setIsValid]);
    return (
        <Container>
            <Label>
                <FieldTitle>Email Address</FieldTitle>
                <Input
                    value={email}
                    editable={!answered}
                    autoCapitalize="none"
                    keyboardType="email-address"
                    returnKeyType="next"
                    textContentType="emailAddress"
                    onChangeText={(e) => setEmail(e)}
                    onSubmitEditing={() => phoneNumberRef.current.focus()}
                />
            </Label>

            <Label>
                <FieldTitle>Phone Number</FieldTitle>
                <Input
                    maxLength={255}
                    autoCompleteType="tel"
                    keyboardType="phone-pad"
                    returnKeyType="go"
                    value={mobilePhone}
                    editable={!answered}
                    ref={phoneNumberRef as any}
                    textContentType="telephoneNumber"
                    onChangeText={(e) => setMobilePhone(e)}
                />
            </Label>

            {!isValid && Boolean(showValidation) && <Instruction>{showValidation}</Instruction>}
        </Container>
    );
};

export default AccountActivation;
