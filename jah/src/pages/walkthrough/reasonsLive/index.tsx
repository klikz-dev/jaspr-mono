import React, { useContext, useState } from 'react';
import { Modal } from 'react-native';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import InfoModal from 'components/InfoModal';
import StoreContext from 'state/context/store';

const Container = Styled.View`flex: 1;`;
const Top = Styled.View`
    flex: 1;
    width: 100%;
    padding-top: 50px;
    max-height: 225px;
    height: 100%;
    align-items: center;
    background-color: #2F344F;
`;
const Title = Styled.Text`
    padding-horizontal: 32px;
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
const ScrollView = Styled.ScrollView`flex: 1;`;
const ReasonContainer = Styled.View`
    border-radius: 8px;
    background-color: #41476A;
    margin-horizontal: 20px;
    margin-vertical: 7.5px;
    padding-horizontal: 15px;
    padding-vertical: 24px;
`;
const ReasonText = Styled.Text`
    color: #FFFEFE;
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.14px;
    line-height: 21px;
`;

const ReasonsLive = () => {
    const [store] = useContext(StoreContext);
    const [showInfo, setShowInfo] = useState(false);
    const { crisisStabilityPlan } = store;
    const { reasonsLive } = crisisStabilityPlan;

    const showInfoModal = () => {
        addAction(actionNames.JAH_WALKTHROUGH_CLICKED_MORE_INFO, {
            extra: 'Reasons to Live',
        });
        setShowInfo(true);
    };

    return (
        <Container>
            <Top>
                <Title>My Reasons for Living</Title>
                <TouchableOpacity onPress={showInfoModal}>
                    <TheWhy>The why behind this ›</TheWhy>
                </TouchableOpacity>
            </Top>
            <ScrollView>
                {(reasonsLive || []).map((reason) => (
                    <ReasonContainer key={reason}>
                        <ReasonText>{reason}</ReasonText>
                    </ReasonContainer>
                ))}
            </ScrollView>
            <Modal visible={showInfo} animationType="fade" transparent={true}>
                <InfoModal
                    title="My Reasons for Living"
                    body="When we’re in a hopeless, dark space, it can be hard to see anything but our pain and life can feel impossible. Remembering your Reasons for Living, even if it seems very small, can help to change your focus just enough to get through the moment and take the next step in build a life you want to live."
                    close={() => setShowInfo(false)}
                />
            </Modal>
        </Container>
    );
};

export default ReasonsLive;
