import React, { useState } from 'react';
import { Modal, Platform } from 'react-native';
import { addAction, actionNames } from 'state/actions/analytics';
import Styled from 'styled-components/native';
import BreatheApp from 'pages/breathe';
import InfoModal from 'components/InfoModal';
import backgroundImageSource from 'pages/breathe/background.png';

const Container = Styled.View`flex: 1;`;
const BackgroundImage = Styled.Image`flex: 1; width: 100%;`;
const Bottom = Styled.View`
    flex: 1;
    width: 100%;
    padding-top: 50px;
    max-height: 225px;
    height: 100%;
    align-items: center;
    background-color: #2F344F;
`;
const Title = Styled.Text`
    color: #ffffff;
    font-size: 36px;
    line-height: 43px;
    text-align: center;
`;
const TouchableOpacity = Styled.TouchableOpacity``;
const TheWhy = Styled.Text`
    margin-top: 10px;
    color: #6CC5D4;
    font-size: 16px;
    font-style: italic;
    font-weight: 300;
    line-height: 19px;
`;

// TODO Don't need the IOS check.  Can just add all the props.  Confirm and refactor everywhere
const StartButton = Styled.TouchableOpacity<{ isIOS: boolean }>`
    align-items: center;
    justify-content: center;
    width: 185px;
    height: 54px;
    margin: auto;
    border-radius: 17px;
    background-color: #5C6597;
    ${({ isIOS }) =>
        isIOS
            ? `
    shadow-color: #000;
    shadow-offset: 2px 4px;
    shadowOpacity: 0.5;
    shadowRadius: 10px;
    `
            : `
    elevation: 7;
    `}
`;
const StartButtonText = Styled.Text`
    color: #FFFEFE;
    font-size: 20px;
    letter-spacing: 0;
    line-height: 24px;
    text-align: center; 
`;

const Breathe = () => {
    const [showBreathe, setShowBreathe] = useState(false);
    const [showInfo, setShowInfo] = useState(false);

    const showInfoModal = () => {
        addAction(actionNames.JAH_WALKTHROUGH_CLICKED_MORE_INFO, { extra: 'Breathe' });
        setShowInfo(true);
    };

    return (
        <Container>
            <BackgroundImage source={backgroundImageSource} resizeMode="cover" />
            <Bottom>
                <Title>Paced Breathing</Title>
                <TouchableOpacity onPress={showInfoModal}>
                    <TheWhy>The why behind this ›</TheWhy>
                </TouchableOpacity>

                <StartButton onPress={() => setShowBreathe(true)} isIOS={Platform.OS === 'ios'}>
                    <StartButtonText>Start</StartButtonText>
                </StartButton>
            </Bottom>
            <Modal visible={showBreathe} animationType="fade" transparent={false}>
                <BreatheApp />
            </Modal>
            <Modal visible={showInfo} animationType="fade" transparent={true}>
                <InfoModal
                    title="Coping Strategies - Body"
                    body="Intense negative emotions can have a big impact on how we feel physically: our muscles tighten, our hearts race, and we might even feel sick to our stomach. These skills help change how you are feeling emotionally and physically. For example, using an exercise like Paced Breathing helps calm your mind and body so you can relax, feel calmer and more at ease."
                    close={() => setShowInfo(false)}
                />
            </Modal>
        </Container>
    );
};

export default Breathe;
