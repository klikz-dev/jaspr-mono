import React, { useContext, useEffect, useState } from 'react';
import { Modal } from 'react-native';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import { getCommonConcerns } from 'state/actions/contacts';
import TitleMenu from 'components/TitleMenu';
import ContactButtons from '../contactButtons';
import Menu from 'components/Menu';

const Container = Styled.View`
    flex: 1;
    background-color: #2F344F;
`;
const List = Styled.ScrollView``;
// TODO Shadow
const ListItem = Styled.TouchableOpacity`
    flex: 1;
    margin-vertical: 9.5px;
    margin-horizontal: 20px;
    border-radius: 8px;
    background-color: #41476A;
`;
const ConcernText = Styled.Text`
    padding-vertical: 28px;
    padding-horizontal: 18px;
    color: #FFFEFE;
    font-size: 20px;
    letter-spacing: 0.15px;
    line-height: 24px;
`;
const ContentContainer = Styled.ScrollView`
    flex: 1;
    padding: 20px;
    background-color: #2F344F;
`;
const ContentText = Styled.Text`
    color: #FFFEFE;
    font-size: 18px;
    letter-spacing: 0.14px;
    line-height: 21px;
`;

const CommonConcerns = () => {
    const [store, dispatch] = useContext(StoreContext);
    const { contacts } = store;
    const { concerns } = contacts;
    const [selectedContent, setSelectedContent] = useState(null);

    useEffect(() => {
        if (concerns.length === 0) {
            getCommonConcerns(dispatch);
        }
    }, [concerns, dispatch]);

    useEffect(() => {
        addAction(actionNames.JAH_ARRIVE_COMMON_CONCERNS);
    }, []);

    return (
        <Container>
            <TitleMenu label="Common Concerns" />
            <List>
                {concerns.map(({ title, content }) => (
                    <ListItem
                        key={title}
                        onPress={() => {
                            setSelectedContent({ title, content });
                            addAction(actionNames.JAH_OPEN_CONCERN, { extra: title });
                        }}
                    >
                        <ConcernText>{title}</ConcernText>
                    </ListItem>
                ))}
            </List>
            <ContactButtons />
            <Menu selected="contacts" />
            <Modal visible={Boolean(selectedContent)} animationType="fade" transparent={false}>
                <TitleMenu goBack={() => setSelectedContent(null)} label={selectedContent?.title} />
                <ContentContainer>
                    <ContentText>{selectedContent?.content}</ContentText>
                </ContentContainer>
                <ContactButtons />
                <Menu selected="contacts" />
            </Modal>
        </Container>
    );
};

export default CommonConcerns;
