import React from 'react';
import { View } from 'react-native';
import { Alert } from 'react-native';
import * as Linking from 'expo-linking';
import { useHistory } from 'lib/router';
import Sentry from 'lib/sentry';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import { formatPhoneNumber } from 'lib/phoneNumber';
import ContactImageSource from 'assets/contact.png';
import Pencil from 'assets/pencilWhite.svg';

const Container = Styled.View`
    flex-direction: column;
    background-color: rgba(65,71,106,1);
    border-radius: 8px;
    padding: 15px;
    marginVertical: 4px;
    shadow-color: #000;
    shadow-offset: 2px 4px;
    shadowOpacity: 0.5;
    shadowRadius: 10px;
    elevation: 7;
`;

const AvatarImage = Styled.Image`
    width: 36px;
    height: 36px;
    border-radius: 8px;
`;
const EditButton = Styled.TouchableOpacity`
    position: absolute;
    top: 13px;
    right: 15px;
    width: 16px;
    height: 17px;
`;
const Name = Styled.Text`
    flex-shrink: 1;
    padding-left: 16px;
    color: #fffefe;
    font-size: 20px;
    letter-spacing: 0.15px;
`;
const PhoneNumber = Styled.Text`
    flex-shrink: 1;
    padding-left: 16px;
    color: #fffefe;
    font-size: 20px;
    letter-spacing: 0.15px;
`;

const Row = Styled.View`
    flex-direction: row;
    align-items: center;
    margin-vertical:  9px;
`;
const Column = Styled.View`
    flex-direction: column;
`;

const Button = Styled.TouchableOpacity`
    flex: 1;
    height: 39px;
    max-width: 134px;
    margin-horizontal: 18px;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255,254,254,1);
    border-radius: 3px;
`;

const ButtonText = Styled.Text`
    color: rgba(255,254,254,1);
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.14px;
    line-height: 21px;
`;

interface Props {
    name: string;
    phone?: string;
    text?: string;
    type?: 'person' | 'hotline';
    index?: number;
}

const Contact = ({ name, phone, text, type = 'person', index }: Props): React.ReactNode => {
    const history = useHistory();

    return (
        <Container>
            {type === 'person' && (
                <EditButton
                    hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
                    onPress={() => history.push(`/jah-supportive-people/edit/${index}`)}
                >
                    <View pointerEvents="none">
                        <Pencil />
                    </View>
                </EditButton>
            )}

            <Row>
                <Column>
                    <AvatarImage source={ContactImageSource} />
                </Column>
                <Column>
                    <Name numberOfLines={1}>{name}</Name>
                    <PhoneNumber numberOfLines={1}>{formatPhoneNumber(phone || text)}</PhoneNumber>
                </Column>
            </Row>
            <Row style={{ justifyContent: 'center' }}>
                {Boolean(phone) && (
                    <Button
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
                        <ButtonText>Call</ButtonText>
                    </Button>
                )}
                {Boolean(text) && (
                    <Button
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
                        <ButtonText>Text</ButtonText>
                    </Button>
                )}
            </Row>
        </Container>
    );
};

export default Contact;
