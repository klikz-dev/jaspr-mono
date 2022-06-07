import React, { useContext, useEffect } from 'react';
import { Platform } from 'react-native';
import { useHistory } from 'lib/router';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import TitleMenu from 'components/TitleMenu';
import Menu from 'components/Menu';
import ContactEdit from 'components/ContactEdit';
import CirclePlusSVG from 'assets/circlePlus.svg';

const Container = Styled.View`
    flex: 1;
    background-color: #2F344F;
`;
const List = Styled.ScrollView``;
const ContactContainer = Styled.View<{ isIOS: boolean }>`
    margin-horizontal: 22px;
    margin-vertical: 10px;
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
const AddButton = Styled.TouchableOpacity`
    height: 40px;
    flex-direction: row;
    margin-vertical: 17px;
    margin-bottom: auto;
    padding-left: 39px;
    align-items: center;
`;
const AddText = Styled.Text`
    margin-horizontal: 22px;
    color: rgba(201,207,216,1);
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.14px;
    line-height: 21px;
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
    const [store] = useContext(StoreContext);
    const { crisisStabilityPlan } = store;
    const { supportivePeople = [] } = crisisStabilityPlan;

    useEffect(() => {
        addAction(actionNames.JAH_ARRIVE_PEOPLE);
    }, []);

    return (
        <Container>
            <TitleMenu label="My Supportive People" />
            <List>
                {supportivePeople?.map(({ name, phone }, index) => (
                    <ContactContainer key={`${name}-${phone}`} isIOS={Platform.OS === 'ios'}>
                        <ContactEdit name={name} phone={phone} text={phone} index={index} />
                    </ContactContainer>
                ))}
                <AddButton onPress={() => history.push('/jah-supportive-people/edit')}>
                    <CirclePlusSVG />
                    <AddText>Add New</AddText>
                </AddButton>
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
