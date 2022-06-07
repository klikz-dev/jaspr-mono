import React, { useState } from 'react';
import { Alert, Modal } from 'react-native';
import Styled from 'styled-components/native';
import * as Linking from 'expo-linking';
import Sentry from 'lib/sentry';
import { addAction, actionNames } from 'state/actions/analytics';
import InfoModal from 'components/InfoModal';
import IconText from 'assets/textIcon.svg';
import IconPhone from 'assets/phoneIcon.svg';
import iconContact from 'assets/contact.png';

const supportivePersonInfo =
    "Calling a supportive person might seem easy until you’re actually in a crisis. Then our minds start generating all kinds of reasons why it's a bad idea to reach out for help: they're too busy; our problems aren't big or important enough. The list goes on. It helps to remember that they are a supportive person for a reason, and they want us to be okay and stay in this world. You can just say you want to chat, or if you’re in trouble, get super honest and say you need help and support. The important part is to reach out and not suffer alone.";
const nationalLineInfo =
    'Calling a crisis hotline can feel scary and shameful. We know from others who have been in extreme pain that healing often starts when we share our truth with someone else, particularly in really difficult moments. Crisis line workers want to help and are there to listen - whether you just want to chat about your problems, or you feel like you can’t stand another minute of life and want to die.';

const Titles = Styled.View`
    margin: auto;
    align-items: center;
    flex-direction: column;
`;
const Title = Styled.Text`
    color: #FFFFFF;
    font-size: 32px;
    letter-spacing: 0;
    line-height: 38px;
    text-align: center;
    margin-vertical: 20px;
`;
const TouchableOpacity = Styled.TouchableOpacity``;
const TheWhy = Styled.Text`
    color: #6CC5D4;
    font-size: 16px;
    font-style: italic;
    font-weight: 300;
    line-height: 19px;
`;
const ContactButtons = Styled.View`
    flex-direction: row;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: auto;
`;
const ContactButton = Styled.TouchableOpacity`
    margin-horizontal: 24px;
`;
const IconPerson = Styled.Image`width: 137px; height: 137px;`;

interface ContactProps {
    personalContact?: boolean;
    name: string;
    phone?: string;
    text?: string;
}

const Contact = ({ personalContact, name, phone, text }: ContactProps) => {
    const [showInfo, setShowInfo] = useState(false);

    const showInfoModal = () => {
        addAction(actionNames.JAH_WALKTHROUGH_CLICKED_MORE_INFO, {
            extra: personalContact ? 'Personal Contact' : 'Hotline',
        });
        setShowInfo(true);
    };

    return (
        <>
            <Titles>
                {personalContact && <IconPerson source={iconContact} />}
                <Title>{name}</Title>
                <TouchableOpacity onPress={showInfoModal}>
                    <TheWhy>{personalContact ? `What to say ›` : 'The why behind this ›'}</TheWhy>
                </TouchableOpacity>
            </Titles>
            <ContactButtons>
                {Boolean(phone) && (
                    <ContactButton
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
                        <IconPhone width={72} height={72} />
                    </ContactButton>
                )}
                {Boolean(text) && (
                    <ContactButton
                        onPress={() => {
                            Linking.openURL(`sms:${text}`).catch((err) => {
                                Sentry.captureException(err.message);
                                Alert.alert(
                                    'Unable to open',
                                    `We were unable to open your messaging app.  The SMS number is ${text}`,
                                    [{ text: 'OK' }],
                                );
                            });
                            addAction(actionNames.JAH_TEXT_SUPPORTIVE_PERSON);
                        }}
                    >
                        <IconText width={72} height={72} />
                    </ContactButton>
                )}
                <Modal visible={showInfo} animationType="fade" transparent={true}>
                    <InfoModal
                        title={personalContact ? 'Call Supportive Person' : 'Call National Hotline'}
                        body={personalContact ? supportivePersonInfo : nationalLineInfo}
                        close={() => setShowInfo(false)}
                    />
                </Modal>
            </ContactButtons>
        </>
    );
};

export default Contact;
