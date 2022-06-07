import React, { useContext, useState } from 'react';
import { Modal } from 'react-native';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import InfoModal from 'components/InfoModal';

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
const SectionContainer = Styled.View`
    flex: 1;
    
    border-radius: 8px;
    background-color: #41476A;
    margin-horizontal: 20px;
    margin-vertical: 7.5px;
    padding-horizontal: 15px;
    padding-vertical: 24px;
    
`;
const TitleText = Styled.Text`
    color: #FFFEFE;
    font-size: 20px;
    letter-spacing: 0.15px;
    line-height: 24px;
    width :100%;
`;
const BoldTitleText = Styled.Text`
    font-weight: bold;
`;
const Items = Styled.View`
    align-items: flex-start;
    flex-wrap: wrap;
`;
const ItemContainer = Styled.View`
    align-items: flex-start;
    flex-shrink: 1;
    margin-vertical: 5px;
    padding-horizontal: 14px;
    padding-vertical: 5px;
    border-radius: 8px;
    background-color: #5C6597;
`;
const ItemText = Styled.Text`
    color: #FFFEFE;
    font-size: 18px;
    letter-spacing: 0.14px;
    line-height: 23px;
`;

const LethalMeans = () => {
    const [store] = useContext(StoreContext);
    const [showInfo, setShowInfo] = useState(false);
    const { crisisStabilityPlan } = store;
    const {
        meansSupportWho,
        strategiesCustom,
        strategiesFirearm,
        strategiesGeneral,
        strategiesMedicine,
        strategiesPlaces,
    } = crisisStabilityPlan;

    const showInfoModal = () => {
        addAction(actionNames.JAH_WALKTHROUGH_CLICKED_MORE_INFO, {
            extra: 'Lethal Means',
        });
        setShowInfo(true);
    };

    return (
        <Container>
            <Top>
                <Title>My Steps to Make Home Safer</Title>
                <TouchableOpacity onPress={showInfoModal}>
                    <TheWhy>The why behind this ›</TheWhy>
                </TouchableOpacity>
            </Top>
            <ScrollView>
                {Boolean(meansSupportWho) && (
                    <SectionContainer>
                        <TitleText>
                            Ask <BoldTitleText>{meansSupportWho}</BoldTitleText> for help with these
                            steps
                        </TitleText>
                    </SectionContainer>
                )}
                {Boolean(strategiesGeneral?.length) && (
                    <SectionContainer>
                        <TitleText>General</TitleText>
                        <Items>
                            {strategiesGeneral?.map((strategy) => (
                                <ItemContainer key={strategy}>
                                    <ItemText>{strategy}</ItemText>
                                </ItemContainer>
                            ))}
                        </Items>
                    </SectionContainer>
                )}
                {Boolean(strategiesMedicine?.length) && (
                    <SectionContainer>
                        <TitleText>Medicine</TitleText>
                        <Items>
                            {strategiesMedicine?.map((strategy) => (
                                <ItemContainer key={strategy}>
                                    <ItemText>{strategy}</ItemText>
                                </ItemContainer>
                            ))}
                        </Items>
                    </SectionContainer>
                )}
                {Boolean(strategiesFirearm?.length) && (
                    <SectionContainer>
                        <TitleText>Firearm</TitleText>
                        <Items>
                            {strategiesFirearm?.map((strategy) => (
                                <ItemContainer key={strategy}>
                                    <ItemText>{strategy}</ItemText>
                                </ItemContainer>
                            ))}
                        </Items>
                    </SectionContainer>
                )}
                {Boolean(strategiesPlaces?.length) && (
                    <SectionContainer>
                        <TitleText>Places</TitleText>
                        <Items>
                            {strategiesPlaces?.map((strategy) => (
                                <ItemContainer key={strategy}>
                                    <ItemText>{strategy}</ItemText>
                                </ItemContainer>
                            ))}
                        </Items>
                    </SectionContainer>
                )}
                {Boolean(strategiesCustom?.length) && (
                    <SectionContainer>
                        <TitleText>Custom Strategies</TitleText>
                        <Items>
                            {strategiesCustom?.map((strategy) => (
                                <ItemContainer key={strategy}>
                                    <ItemText>{strategy}</ItemText>
                                </ItemContainer>
                            ))}
                        </Items>
                    </SectionContainer>
                )}
            </ScrollView>
            <Modal visible={showInfo} animationType="fade" transparent={true}>
                <InfoModal
                    title="My Steps to Make Home Safer"
                    body="In moments of extreme distress, it's hard to think clearly. Our emotions take over and the urge to die feels like the only way out. We know from people who have survived these feelings that these dark moments pass with time. An important way to ride them out involves keeping yourself safe and out of harm's way. That means keeping distance between you and the things you might use to harm yourself. Making your home safe may be the single most important thing you can do to save your life."
                    close={() => setShowInfo(false)}
                />
            </Modal>
        </Container>
    );
};

export default LethalMeans;
