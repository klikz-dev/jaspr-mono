import React, { useContext, useEffect, useState } from 'react';
// TODO Clipboard is deprecated from react-native, import from react-native-community/Clipboard
import { Modal, Clipboard } from 'react-native';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import { getConversationStarters } from 'state/actions/contacts';
import TitleMenu from 'components/TitleMenu';
import Menu from 'components/Menu';
import InfoModal from 'components/InfoModal';
import copyImage from 'assets/copy.png';
import checkImage from 'assets/check.png';

const Container = Styled.View`
    flex: 1;
    background-color: #2F344F;
`;
const List = Styled.ScrollView``;
const ListItem = Styled.View`
    width: 100%;
    flex-direction: row;
    align-items: center;
    padding-vertical: 9.5px;
    padding-horizontal: 10px;
    border-bottom-width: 1px;
    border-bottom-color: #41476A;
`;
const TouchableWithoutFeedback = Styled.TouchableWithoutFeedback`
    flex-direction: row;
`;
const Starter = Styled.View<{ selected: boolean }>`
    flex: 1;
    padding-vertical: 19px;
    padding-horizontal: 16px;
    border-radius: 7px;
    background-color: ${({ selected }) => (selected ? '#F9F9F9' : '#41476A')};
`;
const StarterText = Styled.Text<{ selected: boolean }>`
    color:  ${({ selected }) => (selected ? '#2F3350' : '#FFFEFE')};
    font-size: 16px;
    letter-spacing: 0.21px;
    line-height: 19px;
`;
const CopyImage = Styled.Image`
    height: 33px;
    width: 28px;
    margin-horizontal: 17px;
`;

const WhyButton = Styled.TouchableOpacity`
    height: 56px;
    flex-direction: row;
    align-items: center;
    background-color: #171A27;
`;
const WhyText = Styled.Text`
    color: #FFFEFE;
    font-size: 16px;
    margin-left: 30px;
    margin-right: auto;
`;
const RightPointer = Styled.Text`
    font-size: 35px;
    color: #fff;
    margin-right: 20px;
    line-height: 35px;
`;

const CheckContainer = Styled.View`
    margin: auto;
    height: 200px;
    width: 200px;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background-color: rgba(30,30,30,0.75);
`;
const CheckImage = Styled.Image`
    height: 48px;
    width: 74.5px;
`;
const CheckText = Styled.Text`
    color: #FFFEFE;
    font-size: 20px;
    letter-spacing: 0.15px;
    line-height: 28px;
    text-align: center;
`;

const ConversationStarters = () => {
    const [selectedStarter, setSelectedStarter] = useState<string | null>(null);
    const [showInfo, setShowInfo] = useState(false);
    const [store, dispatch] = useContext(StoreContext);
    const { contacts } = store;
    const { starters } = contacts;

    useEffect(() => {
        if (starters.length === 0) {
            getConversationStarters(dispatch);
        }
    }, [starters, dispatch]);

    // TODO syncronize fading out modal with unselecting highlight
    useEffect(() => {
        const timeout = setTimeout(() => setSelectedStarter(null), 1000);
        if (selectedStarter) {
            Clipboard.setString(selectedStarter);
            addAction(actionNames.JAH_USER_COPY, {
                extra: selectedStarter,
            });
        }

        return () => clearTimeout(timeout);
    }, [selectedStarter]);

    useEffect(() => {
        addAction(actionNames.JAH_ARRIVE_CONVO_STARTERS);
    }, []);

    return (
        <Container>
            <TitleMenu label="Conversation Starters" />
            <List>
                {starters.map((starter) => (
                    <TouchableWithoutFeedback
                        key={starter}
                        onPress={() => setSelectedStarter(starter)}
                    >
                        <ListItem>
                            <Starter selected={starter === selectedStarter}>
                                <StarterText selected={starter === selectedStarter}>
                                    {starter}
                                </StarterText>
                            </Starter>
                            <CopyImage source={copyImage} />
                        </ListItem>
                    </TouchableWithoutFeedback>
                ))}
            </List>
            <WhyButton onPress={() => setShowInfo(true)}>
                <WhyText>Why Conversation Starters?</WhyText>
                <RightPointer>›</RightPointer>
            </WhyButton>
            <Menu selected="contacts" />
            <Modal visible={Boolean(selectedStarter)} animationType="fade" transparent>
                <CheckContainer>
                    <CheckImage source={checkImage} />
                    <CheckText>Text Copied to Clipboard</CheckText>
                </CheckContainer>
            </Modal>
            <Modal visible={showInfo} animationType="fade" transparent>
                <InfoModal
                    close={() => setShowInfo(false)}
                    title="Conversation Starters"
                    body={`It may be hard to ask for help or believe that someone can help you. 

Isolating away from your supportive people (like family or friends) may increase physical and mental health problems because it can lead to long-term "fight-or-flight" stress or changes in your body's natural cycles that negatively affect the your immune system. 

Talking with the supportive people in your life is a reminder that you are not alone and that you have people who care about you and your wellbeing. It also helps stimulate your brain and reverse the negative effects isolation has on your mind and body.`}
                />
            </Modal>
        </Container>
    );
};

export default ConversationStarters;
