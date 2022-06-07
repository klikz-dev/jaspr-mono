import React, { useEffect, useState } from 'react';
import { Linking, Modal, SafeAreaView } from 'react-native';
import Styled from 'styled-components/native';
import { useHistory } from 'lib/router';
import Checkbox from 'components/Checkbox';
import Button from 'components/Button';
import { QuestionProps } from '../../question';
import Segment from 'lib/segment';

const CloseButton = Styled.TouchableOpacity`
    margin: 17px;
    margin-left: auto;
`;
const CloseText = Styled.Text`
    color: #000;
    font-weight: bold;
    font-size: 20px;
`;
const PolicyScroll = Styled.ScrollView``;
const HeaderText = Styled.Text`
    margin-top: 20px;
    font-weight: bold;
    font-size: 20px;
    line-height: 25px;
    letter-spacing: -0.25px;
`;
const ParagraphText = Styled.Text`
    font-size: 20px;
    line-height: 25px
`;
const LinkText = Styled.Text`
    font-size: 20px;
    color: rgba(23, 155, 176, 1);
`;
const AcceptContainer = Styled.View`
    margin-top: 53px;
    margin-bottom: 41px;
    margin-left: 10px;
`;
const Buttons = Styled.View`
    flex-direction: row;
    align-items: center;
    justify-content: space-around;
`;
const CancelButton = Styled.TouchableOpacity``;
const CancelButtonText = Styled.Text`
    color: rgba(23, 155, 176, 1);
    font-size: 20px;
`;

type PrivacyPolicyProps = Pick<QuestionProps, 'currentQuestion' | 'next'>;

const PrivacyPolicy = ({ next, currentQuestion }: PrivacyPolicyProps) => {
    const history = useHistory();
    const [visible, setVisible] = useState(false);
    const [accepted, setAccepted] = useState(false);

    const close = () => {
        history.replace('/');
    };

    const goToPrivacyPolicy = () => {
        Linking.openURL('https://jasprhealth.com/privacy-policy/');
    };

    const accept = () => {
        if (accepted) {
            Segment.track('patient accepted privacy policy in JAH');
            next();
        }
    };

    useEffect(() => {
        setVisible(currentQuestion);
    }, [currentQuestion]);

    return (
        <SafeAreaView>
            <Modal visible={visible} animationType="slide" transparent={false}>
                <CloseButton hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }} onPress={close}>
                    <CloseText>⨉</CloseText>
                </CloseButton>
                <PolicyScroll contentContainerStyle={{ padding: 24, paddingTop: 0 }}>
                    <ParagraphText>
                        Jaspr Health is committed to the highest level of confidentiality with your
                        personal and medical information, and actively enforces the Health Insurance
                        Portability and Accountability Act (HIPAA) regulations. Our employees are
                        held to high standards in accessing and maintaining confidential information
                        as outlined in our corporate and departmental policies and procedures.
                    </ParagraphText>
                    <HeaderText>Access to records</HeaderText>
                    <ParagraphText>
                        You have the right to obtain and inspect a copy of your personal information
                        that we or our business associates maintain. Please send requests to
                        support@jasprhealth.com.
                    </ParagraphText>
                    <HeaderText>Use of measurement data</HeaderText>
                    <ParagraphText>
                        Jaspr Health collects and analyzes claim information to perform utilization
                        management, case management and other clinical activities. The data is used
                        to identify areas of improvement for the care and service members receive.
                    </ParagraphText>
                    <ParagraphText
                        style={{
                            marginTop: 20,
                        }}
                    >
                        Read our full policy:{' '}
                        <LinkText onPress={goToPrivacyPolicy}>Privacy Policy</LinkText>
                    </ParagraphText>
                    <AcceptContainer>
                        <Checkbox
                            checked={accepted}
                            onChange={(value) => setAccepted(value)}
                            label="I accept the Jaspr Health Privacy Policy"
                            labelStyle={{ fontSize: 22, lineHeight: 24, marginLeft: 30 }}
                        />
                    </AcceptContainer>
                    <Buttons>
                        <CancelButton onPress={close}>
                            <CancelButtonText>Cancel</CancelButtonText>
                        </CancelButton>
                        <Button disabled={!accepted} onClick={accept} label="Continue"></Button>
                    </Buttons>
                </PolicyScroll>
            </Modal>
        </SafeAreaView>
    );
};

export default PrivacyPolicy;
