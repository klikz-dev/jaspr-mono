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

const CopingStrategies = (): JSX.Element => {
    const [store] = useContext(StoreContext);
    const { crisisStabilityPlan, media } = store;
    const { copingTop } = crisisStabilityPlan;
    const { isFullScreen } = media;
    const { copingStrategies = {} } = media.media;
    const { dash, hls, video, poster } = copingStrategies;

    return (
        <Container>
            {!isFullScreen && <TitleMenu label="Coping Strategies" />}
            <VideoPlayer
                poster={poster}
                fpm4Transcode={dash}
                hlsPlaylist={hls}
                mp4Transcode={video}
                name="Learn more about coping strategies"
            />
            {!isFullScreen && (
                <>
                    <Inner>
                        <TopContainer
                            title="My Top Coping Strategies"
                            moreLabel={
                                copingTop?.length ? 'View All My Coping Strategies' : undefined
                            }
                            moreLink="/jah-stability-playlist/coping-strategies/full"
                            link="/jah-stability-playlist/coping-strategies/edit"
                            showPencil
                        >
                            <Labels>
                                {copingTop?.map((strategy) => (
                                    <Item key={strategy} label={strategy} />
                                ))}
                            </Labels>
                            {!Boolean(copingTop?.length) && (
                                <DescriptionContainer>
                                    <Description>
                                        There is no better time to have distress survival skills at
                                        the ready than when you're overwhelmed. There are lots of
                                        different ways to get through tough times - skills to help
                                        you distract so you can take your mind off of your problems
                                        for a period of time; to help you feel more comfortable and
                                        relaxed in the moment; help you see more clearly; and help
                                        you get through intense negative emotions.The idea is to
                                        explore different ways to get through really difficult
                                        moments. Learn from people with lived experience about
                                        coping strategies they found most useful and how they used
                                        them.
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

export default CopingStrategies;
