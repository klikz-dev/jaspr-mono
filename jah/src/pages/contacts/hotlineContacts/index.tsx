import React, { useEffect } from 'react';
import { useHistory } from 'lib/router';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import TitleMenu from 'components/TitleMenu';
import Menu from 'components/Menu';
import ContactEdit from 'components/ContactEdit';

const Container = Styled.View`
    flex: 1;
    background-color: #2F344F;
`;
const List = Styled.ScrollView``;
const ContactContainer = Styled.View`
    margin-horizontal: 22px;
    margin-vertical: 10px;
    shadow-color: #000;
    shadow-offset: 2px 4px;
    shadowOpacity: 0.5;
    shadowRadius: 10px;
    elevation: 7;
`;

const MoreButton = Styled.TouchableOpacity`
    height: 56px;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    background-color: #171A27;
`;
const MoreText = Styled.Text`
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

const SupportivePeopleSharedStories = () => {
    const history = useHistory();

    useEffect(() => {
        addAction(actionNames.JAH_ARRIVE_PEOPLE);
    }, []);

    return (
        <Container>
            <TitleMenu label="Hotline Contacts" />
            <List>
                <ContactContainer>
                    <ContactEdit name="National Lifeline" phone="8002738255" type="hotline" />
                </ContactContainer>
                <ContactContainer>
                    <ContactEdit name="National Text Line" text="741741" type="hotline" />
                </ContactContainer>
            </List>

            <MoreButton onPress={() => history.push('/jah-supportive-people-info')}>
                <MoreText>More About Supportive People</MoreText>
                <RightPointer>›</RightPointer>
            </MoreButton>
            <Menu selected="contacts" />
        </Container>
    );
};

export default SupportivePeopleSharedStories;
