import React, { useContext, useEffect } from 'react';
import { ImageBackground, Platform } from 'react-native';
import Styled from 'styled-components/native';
import ListContainer from 'components/ListContainer';
import Menu from 'components/Menu/index';
import Hamburger from 'components/Hamburger';
import { getCrisisStabilityPlan } from 'state/actions/crisisStabilityPlan';
import StoreContext from 'state/context/store';
import backgroundImageSource from 'assets/stabilityPlanBackground.png';
import HeartSource from 'assets/heartplus.png';
import { useHistory } from 'lib/router';

const Container = Styled.View`margin-top: auto;`;

const DistressContainer = Styled.TouchableOpacity<{ isIOS: boolean }>`
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    background-color:#FFFAD6;
    height: 80px;
    border-radius: 8px;
    margin: 20px;
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

const DistressText = Styled.Text`color: #47546B; font-size: 22px; font-weight: 500;`;
const HeartImage = Styled.Image`width: 38px; height: 35.5px;`;

const StabilityPlaylist = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { token } = user;

    useEffect(() => {
        if (token) {
            getCrisisStabilityPlan(dispatch);
        }
    }, [dispatch, token]);

    return (
        <>
            <ImageBackground
                style={{ flex: 1, marginTop: 'auto' }}
                source={backgroundImageSource}
                resizeMode="cover"
            >
                <Hamburger />
                <Container>
                    <DistressContainer
                        onPress={() => history.push('/jah-walkthrough')}
                        isIOS={Platform.OS === 'ios'}
                    >
                        <DistressText>Distress Survival Guide</DistressText>
                        <HeartImage source={HeartSource} />
                    </DistressContainer>
                </Container>
            </ImageBackground>
            <ListContainer
                noRoundedCorners
                items={[
                    {
                        label: 'Warning Signals',
                        link: '/jah-stability-playlist/warning-signals',
                    },
                    {
                        label: 'Making Home Safer',
                        link: '/jah-stability-playlist/making-home-safer',
                    },
                    {
                        label: 'Reasons For Living',
                        link: '/jah-stability-playlist/reasons-for-living',
                    },
                    {
                        label: 'Coping Strategies',
                        link: '/jah-stability-playlist/coping-strategies',
                    },
                ]}
            />
            <Menu selected="stability-playlist" />
        </>
    );
};

export default StabilityPlaylist;
