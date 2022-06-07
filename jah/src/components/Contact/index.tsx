import React from 'react';
import { Alert } from 'react-native';
import * as Linking from 'expo-linking';
import Sentry from 'lib/sentry';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import { formatPhoneNumber } from 'lib/phoneNumber';
import ContactImageSource from 'assets/contact.png';
import PhoneImageSource from 'assets/phoneIcon.svg';
import TextImageSource from 'assets/textIcon.svg';

const Container = Styled.View`
    flex-direction: row;
    background-color: #5C6597;
    border-radius: 10px;
    padding: 10px;
    align-items: center;
    marginVertical: 4px;
`;
const TouchableOpacity = Styled.TouchableOpacity``;
const Image = Styled.Image`
    width: 36px;
    height: 36px;
    border-radius: 18px;
`;
const Column = Styled.View`
    flex-direction: column;
`;
const Name = Styled.Text`
    flex-shrink: 1;
    padding-left: 16px;
    color: #fffefe;
    font-size: 18px;
    letter-spacing: 0.12px;
`;
const Number = Styled.Text`
    flex-shrink: 1;
    padding-left: 16px;
    color: rgba(255,254,254,1);
    font-size: 12px;
    letter-spacing: 0.09px;
`;
const Options = Styled.View`flex-direction: row; margin-left: auto;`;

const smallImage = {
    width: 36,
    height: 36,
    borderRadius: 18,
    marginLeft: 10,
};

interface ContactProps {
    name: string;
    phone?: string;
    text?: string;
}

const Contact = ({ name, phone, text }: ContactProps) => {
    return (
        <Container>
            <Image source={ContactImageSource} />
            <Column>
                <Name numberOfLines={1}>{name}</Name>
                <Number numberOfLines={1}>{formatPhoneNumber(phone || text)}</Number>
            </Column>
            <Options>
                {Boolean(phone) && (
                    <TouchableOpacity
                        onPress={() => {
                            Linking.openURL(`tel://${phone}`).catch((err) => {
                                Sentry.captureException(err.message);
                                Alert.alert(
                                    'Unable to open',
                                    `We were unable to open your dialer.  The phone number is ${phone}`,
                                    [{ text: 'OK' }],
                                );
                            });
                            addAction(actionNames.JAH_CALL_SUPPORTIVE_PERSON);
                        }}
                    >
                        <PhoneImageSource style={smallImage} />
                    </TouchableOpacity>
                )}
                {Boolean(text) && (
                    <TouchableOpacity
                        onPress={() => {
                            Linking.openURL(`sms:${text}`).catch((err) => {
                                Sentry.captureException(err.message);
                                Alert.alert(
                                    'Unable to open',
                                    `We were unable to open your messaging app.  The sms number is ${text}`,
                                    [{ text: 'OK' }],
                                );
                            });
                            addAction(actionNames.JAH_TEXT_SUPPORTIVE_PERSON);
                        }}
                    >
                        <TextImageSource style={smallImage} />
                    </TouchableOpacity>
                )}
            </Options>
        </Container>
    );
};

export default Contact;
