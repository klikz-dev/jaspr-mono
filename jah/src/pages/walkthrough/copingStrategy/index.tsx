import React, { useState } from 'react';
import { Modal } from 'react-native';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import InfoModal from 'components/InfoModal';

const Container = Styled.View`flex: 1;`;
const BackgroundImage = Styled.Image`flex: 1;`;
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

interface CopingStrategyProps {
    title: string;
    image: string;
    category?: { name: string; whyText: string };
}

const CopingStrategy = ({
    title,
    image,
    category = { name: '', whyText: '' },
}: CopingStrategyProps) => {
    const [showInfo, setShowInfo] = useState(false);
    const { name, whyText } = category;

    const showInfoModal = () => {
        addAction(actionNames.JAH_WALKTHROUGH_CLICKED_MORE_INFO, {
            extra: 'Coping Strategy',
        });
        setShowInfo(true);
    };

    return (
        <Container>
            <BackgroundImage source={{ uri: image }} resizeMode="cover" />
            <Bottom>
                <Title>{title}</Title>
                <TouchableOpacity onPress={showInfoModal}>
                    <TheWhy>The why behind this ›</TheWhy>
                </TouchableOpacity>
            </Bottom>
            <Modal visible={showInfo} animationType="fade" transparent={true}>
                <InfoModal title={name} body={whyText} close={() => setShowInfo(false)} />
            </Modal>
        </Container>
    );
};

export default CopingStrategy;
