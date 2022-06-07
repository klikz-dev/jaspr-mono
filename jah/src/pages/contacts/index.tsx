import React, { useContext, useEffect } from 'react';
import { ImageBackground } from 'react-native';
import { useHistory } from 'lib/router';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import { getCrisisStabilityPlan } from 'state/actions/crisisStabilityPlan';
import Menu from 'components/Menu/index';
import Hamburger from 'components/Hamburger';
import Container from 'components/TopContainer';
import Contact from 'components/Contact';
import backgroundImageSource from 'assets/contactBackground.png';
import { Patient } from 'state/types';

const Contacts = Styled.View`margin-top: auto;`;
const TouchableOpacity = Styled.TouchableOpacity``;
const AddContactText = Styled.Text`color: #fff;`;

const JahContacts = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { crisisStabilityPlan, user } = store;
    const { token } = user as Patient;
    const { supportivePeople } = crisisStabilityPlan;

    useEffect(() => {
        if (token) {
            getCrisisStabilityPlan(dispatch);
        }
    }, [dispatch, token]);

    useEffect(() => {
        addAction(actionNames.JAH_ARRIVE_CONTACTS);
    }, []);

    return (
        <ImageBackground style={{ flex: 1 }} source={backgroundImageSource}>
            <Hamburger />
            <Contacts>
                <Container
                    title="My Supportive People"
                    link="/jah-supportive-people"
                    moreLink="/jah-supportive-people-info"
                    moreLabel="More About Supportive People"
                >
                    {supportivePeople?.slice(0, 2).map(
                        (
                            person, // Only show the first two
                        ) => (
                            <Contact
                                key={person.name}
                                name={person.name || ''}
                                phone={person.phone || ''}
                                text={person.phone || ''}
                            />
                        ),
                    )}
                    {!supportivePeople ||
                        (supportivePeople?.length === 0 && (
                            <TouchableOpacity
                                onPress={() => {
                                    history.push('/jah-supportive-people');
                                }}
                            >
                                <AddContactText>Add a Supportive Person</AddContactText>
                            </TouchableOpacity>
                        ))}
                </Container>
                <Container
                    title="Hotline Contacts"
                    moreLabel="More About Using Hotlines"
                    link="/jah-contacts/hotlines"
                    moreLink="/jah-contacts/hotline-info"
                >
                    <Contact name="National Lifeline" phone="800-273-8255" />
                    <Contact name="National Text Line" text="741741" />
                </Container>
                <Menu selected="contacts" />
            </Contacts>
        </ImageBackground>
    );
};

export default JahContacts;
