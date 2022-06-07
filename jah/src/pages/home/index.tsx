import React, { useContext, useEffect } from 'react';
import { ImageBackground } from 'react-native';
import { useHistory } from 'lib/router';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import { getCrisisStabilityPlan } from 'state/actions/crisisStabilityPlan';
import StoreContext from 'state/context/store';
import Menu from 'components/Menu/index';
import Hamburger from 'components/Hamburger';
import Container from 'components/TopContainer';
import Favorites from 'components/Favorites';
import TopShadow from 'components/TopShadow';
import SupportiveContacts from 'components/SupportiveContacts';
import HeartSource from 'assets/heartplus.png';
import backgroundImageSource from 'assets/homeImage.png';

const Home = Styled.View`
    position: relative;
    background-color: #2F344F;
    padding-top: 15px;
`;
const View = Styled.View``;
const StabilityShortcut = Styled.TouchableOpacity`
    margin-top: auto;
    background-color: #F5EAD6;
    width: 65px;
    height: 50px;
    margin-left: auto;
    margin-right: 15px;
    align-items: center;
    justify-content: center;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
`;
const Image = Styled.Image`width: 38px; height: 35.5px;`;

const JahHome = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { token } = user;

    const gotoWalkthrough = () => {
        addAction(actionNames.JAH_WALKTHROUGH_START, { screen: 'home' });
        history.push('/jah-walkthrough');
    };

    useEffect(() => {
        if (token) {
            getCrisisStabilityPlan(dispatch);
        }
    }, [dispatch, token]);

    return (
        <>
            <ImageBackground style={{ flex: 1 }} source={backgroundImageSource}>
                <Hamburger />
                <StabilityShortcut onPress={gotoWalkthrough}>
                    <Image source={HeartSource} />
                </StabilityShortcut>
            </ImageBackground>

            <Home>
                <TopShadow />
                <Container title="My Favorites" link="/jah-favorites">
                    <View>
                        <Favorites />
                    </View>
                </Container>
                <Container title="My Supportive Contacts" link="/jah-contacts">
                    <View>
                        <SupportiveContacts />
                    </View>
                </Container>
                <Menu selected="home" />
            </Home>
        </>
    );
};

export default JahHome;
