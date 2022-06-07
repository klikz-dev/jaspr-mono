import React, { useContext, useEffect, useState } from 'react';
import Styled from 'styled-components/native';
import { CodeField, Cursor, useBlurOnFulfill } from 'react-native-confirmation-code-field';
import axios from 'axios';
import Segment from 'lib/segment';
import StoreContext from 'state/context/store';
import config from 'config';
import styles from './index.module.css';
import { setMe } from 'state/actions/user';
import { QuestionProps } from '../../question';
import { Patient } from 'state/types';

const Container = Styled.View`${styles.container}`;
const Instruction = Styled.Text`${styles.instruction} line-height: 25px;`;
const Label = Styled.View`${styles.label}`;
const Cell = Styled.Text`${styles.cell}`;

type AccountCodeProps = Pick<
    QuestionProps,
    'answered' | 'showValidation' | 'isValid' | 'setIsValid' | 'validate' | 'setShowValidation'
>;

const AccountCode = (props: AccountCodeProps) => {
    const { answered, showValidation, setShowValidation, isValid, setIsValid, validate } = props;
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { email, mobilePhone } = user as Patient;
    const [code, setCode] = useState('');
    const ref = useBlurOnFulfill({ value: code, cellCount: 6 });

    useEffect(() => {
        const payload = {
            email,
            mobilePhone,
            code,
            longLived: true,
        };
        validate.current = () => {
            return new Promise((resolve, reject) => {
                if (!code) {
                    setShowValidation('You must enter your activation code');
                    return reject();
                }
                axios
                    .post(`${config.apiRoot}/patient/native-check-phone-number-code`, payload)
                    .then((response) => {
                        setMe(dispatch, {
                            authenticated: false,
                            userType: '',
                            setupToken: response.data.token,
                            setupUid: response.data.uid,
                            alreadySetUp: response.data.alreadySetUp,
                            setPasswordToken: response.data.setPasswordToken,
                        });
                        Segment.track('account-activation', {
                            activation_code: 'success',
                        });
                        Segment.track('account-code');
                        setIsValid(true);
                        resolve();
                    })
                    .catch((err) => {
                        const { data } = err.response;
                        const { nonFieldErrors, code } = data;

                        if (code) {
                            setShowValidation(code?.join('\n'));
                        } else if (nonFieldErrors) {
                            setShowValidation(nonFieldErrors?.join('\n'));
                        }
                        Segment.track('account-activation', {
                            activation_code: 'failed',
                        });
                        reject();
                    });
            });
        };
    }, [mobilePhone, email, code, validate, setShowValidation, dispatch, setIsValid]);

    return (
        <Container>
            <Label>
                <CodeField
                    ref={ref}
                    value={code}
                    onChangeText={setCode}
                    cellCount={6}
                    rootStyle={{
                        marginLeft: 20,
                        marginRight: 20,
                    }}
                    keyboardType="number-pad"
                    textContentType="oneTimeCode"
                    renderCell={({ index, symbol, isFocused }) => (
                        <Cell
                            key={index}
                            style={
                                isFocused
                                    ? { borderColor: '#000000', lineHeight: 54 }
                                    : { lineHeight: 54 }
                            }
                        >
                            {symbol || (isFocused ? <Cursor /> : null)}
                        </Cell>
                    )}
                />
            </Label>

            {!isValid && Boolean(showValidation) && <Instruction>{showValidation}</Instruction>}
        </Container>
    );
};

export default AccountCode;
