import React, { useContext, useEffect, useState, useRef } from 'react';
import { TextInput } from 'react-native';
import Styled from 'styled-components/native';
import { useRouteMatch } from 'lib/router';
import { saveCrisisStabilityPlan } from 'state/actions/crisisStabilityPlan';
import { addAction, actionNames } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import TitleMenu from 'components/TitleMenu';
import Menu from 'components/Menu';
import { useHistory } from 'lib/router';
import Button from 'components/Button';
// import Heart from 'assets/heart.svg';
// import HeartFilled from 'assets/heartFilled.svg';

const Container = Styled.View`
    flex: 1;
    flex-shrink: 0;
    background-color: #2F344F;
`;
const Title = Styled.Text`
    margin-top: 20px;
    margin-bottom: 14px;
    align-self: center;
    color: rgba(255,254,254,1);
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.14px;
    line-height: 21px;
`;
const Form = Styled.ScrollView`
    flex: 1;
    flex-shrink: 0;
    flex-direction: column;
`;
const FormHeader = Styled.View`
    padding-horizontal: 32px;
    padding-vertical: 8px;
    border-bottom-width: 1px;
    border-top-width: 1px;
    border-color: rgba(140,140,140,1);
`;
const FormHeaderText = Styled.Text`
    color: rgba(255,254,254,0.81);
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.14px;
    line-height: 21px;
`;
const FormInput = Styled.TextInput`
    padding-horizontal: 32px;
    padding-vertical: 18px;
    color: rgba(255,254,254,0.81);
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.14px;
    line-height: 21px;
`;
const HR = Styled.View`
    border-bottom-width: 1px;
    border-color: rgba(140,140,140,1);
`;
/* const GuideRow = Styled.TouchableOpacity`
    flex-direction: row;
    align-items: center;
    justify-content: center;
    margin-vertical: 28px;
    margin-bottom: 10px;
`;
const GuideText = Styled.Text`
    margin-left: 18px;
    color: rgba(255,254,254,1);
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.14px;
    line-height: 21px;
`; 
*/

const DeleteContact = Styled.TouchableOpacity`
    margin-top: auto;
    margin-left: auto;
    margin-right: auto;
`;
const DeleteContactText = Styled.Text`
    color: rgba(255,254,254,1);
    font-size: 16px;
    letter-spacing: 0.12px;
    line-height: 19px;
    text-decoration: underline;
`;
// TODO Refactor More Button into it's own component
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

const SupportivePeopleEditContact = (): JSX.Element => {
    const history = useHistory();
    const match = useRouteMatch<{ contactId?: string }>();
    const contactIndex = match.params?.contactId ? parseInt(match.params.contactId, 10) : null;

    const [store, dispatch] = useContext(StoreContext);
    const { crisisStabilityPlan } = store;
    const { supportivePeople = [] } = crisisStabilityPlan;
    const phoneNumberRef = useRef<typeof FormInput>(null!);
    const [editedContact, setEditedContact] = useState({
        name: contactIndex !== null ? supportivePeople[contactIndex].name : '',
        phone: contactIndex !== null ? supportivePeople[contactIndex].phone : '',
    });

    // const ToggleGuideContent = () => {};

    const saveContact = () => {
        const newSupportivePeople = [...(supportivePeople || [])];

        if (contactIndex !== null && newSupportivePeople.length >= contactIndex + 1) {
            newSupportivePeople[contactIndex] = editedContact;
            addAction(actionNames.JAH_CONTACT_EDITED);
        } else {
            newSupportivePeople.push(editedContact);
            addAction(actionNames.JAH_CONTACT_MODIFIED);
        }

        saveCrisisStabilityPlan(dispatch, { supportivePeople: newSupportivePeople });
        history.goBack();
    };

    const deleteContact = () => {
        if (contactIndex !== null) {
            const newSupportivePeople = [...(supportivePeople || [])];
            newSupportivePeople.splice(contactIndex, 1);
            saveCrisisStabilityPlan(dispatch, { supportivePeople: newSupportivePeople });
            addAction(actionNames.JAH_CONTACT_DELETED);
        }
        history.goBack();
    };

    useEffect(() => {
        addAction(actionNames.JAH_ARRIVE_CONTACT_EDIT);
    }, []);

    useEffect(() => {
        setEditedContact({
            name: contactIndex !== null ? supportivePeople[contactIndex].name : '',
            phone: contactIndex !== null ? supportivePeople[contactIndex].phone : '',
        });
    }, [supportivePeople, contactIndex]);

    return (
        <Container>
            <TitleMenu label="My Supportive People" />
            <Title>Edit Contact</Title>
            <Form
                contentContainerStyle={{
                    flexGrow: 1,
                    paddingBottom: 36,
                }}
            >
                <FormHeader>
                    <FormHeaderText>Name</FormHeaderText>
                </FormHeader>
                <FormInput
                    returnKeyType="next"
                    textContentType="name"
                    // @ts-ignore
                    onSubmitEditing={() => phoneNumberRef.current?.focus()}
                    value={editedContact.name}
                    onChangeText={(value) => setEditedContact({ ...editedContact, name: value })}
                />
                <FormHeader>
                    <FormHeaderText>Number</FormHeaderText>
                </FormHeader>
                <FormInput
                    // @ts-ignore TODO refs on styled components
                    ref={phoneNumberRef}
                    autoCompleteType="tel"
                    keyboardType="phone-pad"
                    textContentType="telephoneNumber"
                    returnKeyType="done"
                    value={editedContact.phone}
                    onChangeText={(value) => setEditedContact({ ...editedContact, phone: value })}
                />
                <HR />
                {/*
                <GuideRow onPress={ToggleGuideContent}>
                    {saved ? (
                        <HeartFilled width={32} height={30} />
                    ) : (
                        <Heart width={32} height={30} />
                    )}
                    <GuideText>Add to Distress Survival Guide</GuideText>
                </GuideRow>
                */}
                <Button
                    onClick={saveContact}
                    label="Save Contact"
                    style={{
                        marginLeft: 22,
                        marginRight: 22,
                        marginTop: 40,
                        marginBottom: 25,
                    }}
                />

                <DeleteContact onPress={deleteContact}>
                    <DeleteContactText>Delete Contact</DeleteContactText>
                </DeleteContact>
            </Form>
            <MoreButton onPress={() => history.push('/jah-supportive-people-info')}>
                <MoreText>More About Supportive People</MoreText>
                <RightPointer>›</RightPointer>
            </MoreButton>
            <Menu selected="contacts" />
        </Container>
    );
};

export default SupportivePeopleEditContact;
