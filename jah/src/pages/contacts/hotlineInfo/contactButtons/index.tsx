import React from 'react';
import * as Linking from 'expo-linking';
import { Alert } from 'react-native';
import Sentry from 'lib/sentry';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import TextIcon from 'assets/textIconDark.svg';
import PhoneIcon from 'assets/phoneIconDark.svg';

const ContactContainer = Styled.View`
    height: 56px;
    flex-direction: row;
    align-items: center;
    background-color: #171A27;
    
`;
const Text = Styled.Text`
    color: #FFFEFE;
    font-size: 16px;
    margin-left: 30px;
    margin-right: auto;
`;
const ContactButton = Styled.TouchableOpacity`
    margin-right: 20px;
`;

const ContactButtons = () => {
    return (
        <ContactContainer>
            <Text>National Hotlines</Text>
            <ContactButton
                onPress={() => {
                    const phone = '+1-800-273-8255';
                    Linking.openURL(`tel://${phone}`).catch((err) => {
                        Sentry.captureException(err.message);
                        Alert.alert(
                            'Unable to open',
                            `We were unable to open your dialer.  The phone number is ${phone}`,
                            [{ text: 'OK' }],
                        );
                    });
                    addAction(actionNames.JAH_CALL_HOTLINE);
                }}
            >
                <PhoneIcon width={40} height={40} />
            </ContactButton>
            <ContactButton
                onPress={() => {
                    const sms = '741741';
                    Linking.openURL(`sms:${sms}`).catch((err) => {
                        Sentry.captureException(err.message);
                        Alert.alert(
                            'Unable to open',
                            `We were unable to open your messaging app.  The SMS number is ${sms}`,
                            [{ text: 'OK' }],
                        );
                    });
                    addAction(actionNames.JAH_TEXT_HOTLINE);
                }}
            >
                <TextIcon width={40} height={40} />
            </ContactButton>
        </ContactContainer>
    );
};

export default ContactButtons;
