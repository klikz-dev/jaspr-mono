import React, { useContext, useEffect } from 'react';
import { Alert } from 'react-native';
import Styled from 'styled-components/native';
import * as Linking from 'expo-linking';
import Sentry from 'lib/sentry';
import { addAction, actionNames } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import LifelinePhoneSource from 'assets/phoneIcon.svg';
import LifelineTextSource from 'assets/textIcon.svg';
import ContactImageSource from 'assets/contact.png';
import { getCrisisStabilityPlan } from 'state/actions/crisisStabilityPlan';

const Container = Styled.View`flex-direction: row;`;
const ContactContainer = Styled.TouchableOpacity`flex-basis: 33.33%; align-items: center;`;
const Image = Styled.Image`width: 72px; height: 72px;`;
const Name = Styled.Text`margin-top: 7px; text-align: center; color: #ECF0F3; line-height: 15px; font-size: 12px; letter-spacing: 0.09px;`;

const SupportiveContacts = (): JSX.Element => {
    const [store, dispatch] = useContext(StoreContext);
    const { crisisStabilityPlan, user } = store;
    const { supportivePeople = [] } = crisisStabilityPlan;
    const { token } = user;

    useEffect(() => {
        if (token) {
            getCrisisStabilityPlan(dispatch);
        }
    }, [dispatch, token]);

    return (
        <Container>
            <ContactContainer
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
                <LifelinePhoneSource width={72} height={72} />
                <Name>National{'\n'}Lifeline</Name>
            </ContactContainer>
            <ContactContainer
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
                <LifelineTextSource width={72} height={72} />
                <Name>National{'\n'}Lifeline</Name>
            </ContactContainer>
            {Boolean(supportivePeople?.length) && (
                <ContactContainer
                    onPress={() => {
                        Linking.openURL(`tel://${supportivePeople[0].phone}`).catch((err) => {
                            Sentry.captureException(err.message);
                            Alert.alert(
                                'Unable to open',
                                `We were unable to open your dialer.  The phone number is ${supportivePeople[0].phone}`,
                                [{ text: 'OK' }],
                            );
                        });
                        addAction(actionNames.JAH_CALL_SUPPORTIVE_PERSON);
                    }}
                >
                    <Image source={ContactImageSource} />
                    <Name>{supportivePeople[0].name}</Name>
                </ContactContainer>
            )}
        </Container>
    );
};

export default SupportiveContacts;
