import React, { useContext } from 'react';
import Styled from 'styled-components/native';
import StoreContext from 'state/context/store';
import TitleMenu from 'components/TitleMenu';
import VideoPlayer from 'components/Videos/Player';
import DistressButton from 'components/DistressButton';
import TopContainer from 'components/TopContainer';
import Menu from 'components/Menu/index';
import Item from '../item';

const Container = Styled.View`
    flex: 1;
    background-color: #5C6597;
`;
const Inner = Styled.ScrollView`
    background-color: #41476A
`;
const Labels = Styled.View`
    flex-direction: row;
    flex-wrap: wrap;
`;
const DescriptionContainer = Styled.ScrollView``;
const Description = Styled.Text`
    padding-vertical: 28px;
    color: #FFFEFE;
    font-size: 16px;
    font-weight: 300;
    line-height: 24px;
`;

const WarningSignals = () => {
    const [store] = useContext(StoreContext);
    const { crisisStabilityPlan, media } = store;
    const { isFullScreen } = media;
    const { warningSignals = {} } = media.media;
    const { wsTop } = crisisStabilityPlan;

    const { dash, hls, video, poster } = warningSignals;

    return (
        <Container>
            {!isFullScreen && <TitleMenu label="Warning Signals" />}
            <VideoPlayer
                poster={poster}
                fpm4Transcode={dash}
                hlsPlaylist={hls}
                mp4Transcode={video}
                name="Learn more about warning signals"
            />
            {!isFullScreen && (
                <>
                    <Inner>
                        <TopContainer
                            title="My Top Warning Signals"
                            moreLabel={wsTop?.length ? 'View All My Warning Signals' : undefined}
                            moreLink="/jah-stability-playlist/warning-signals/full"
                            link="/jah-stability-playlist/warning-signals/edit"
                            showPencil
                        >
                            <Labels>
                                {wsTop?.map((strategy) => (
                                    <Item key={strategy} label={strategy} />
                                ))}
                            </Labels>
                            {!Boolean(wsTop?.length) && (
                                <DescriptionContainer>
                                    <Description>
                                        It’s always good to know when you’re heading toward the eye
                                        of the emotional storm. At a minimum, you can prepare so
                                        when it happens, the impact isn’t quite so severe. Even
                                        better is if you can see the storm coming and start heading
                                        in another direction to avoid the crisis altogether. One of
                                        the best ways to prepare is to know your own personal
                                        warning signals - those things that tell you a crisis is
                                        around the corner like certain events, body sensations and
                                        the things you do when you’re not doing well. The whole idea
                                        is to recognize early on when you are going off course and
                                        to have a plan when it happens, so you keep working to
                                        (re)build the life you want for yourself.
                                    </Description>
                                </DescriptionContainer>
                            )}
                        </TopContainer>
                    </Inner>
                    <DistressButton />
                    <Menu selected="stability-playlist" />
                </>
            )}
        </Container>
    );
};

export default WarningSignals;
