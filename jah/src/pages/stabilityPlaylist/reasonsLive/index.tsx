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
    font-size: 18px;
    letter-spacing: 0.14px;
    line-height: 21px;
`;

const ReasonsLive = (): JSX.Element => {
    const [store] = useContext(StoreContext);
    const { crisisStabilityPlan, media } = store;
    const { isFullScreen } = media;
    const { reasonsLive: reasonsLiveMedia = {} } = media.media;
    const { reasonsLive } = crisisStabilityPlan;
    const { dash, hls, video, poster } = reasonsLiveMedia;

    return (
        <Container>
            {!isFullScreen && <TitleMenu label="Reasons for Living" />}
            <VideoPlayer
                poster={poster}
                fpm4Transcode={dash}
                hlsPlaylist={hls}
                mp4Transcode={video}
                name="Learn more about reasons for living"
            />
            {!isFullScreen && (
                <>
                    <Inner>
                        <TopContainer
                            title="My Reasons for Living"
                            link="/jah-stability-playlist/reasons-for-living/edit"
                            showPencil
                        >
                            <Labels>
                                {reasonsLive?.map((strategy) => (
                                    <Item key={strategy} label={strategy} />
                                ))}
                            </Labels>
                            {!Boolean(reasonsLive?.length) && (
                                <DescriptionContainer>
                                    <Description>
                                        Finding the most important things in your life that makes
                                        you want to keep going, even in your darkest moments, can
                                        make the difference between life and death. Reasons for
                                        Living can be things like your family, friends, pets,
                                        spirituality or even just wanting to see spring flowers
                                        bloom. For some people, they’re easy to find. For others,
                                        finding even one can feel impossible and may require help
                                        and support to find one. When you do find something, even if
                                        it seems small, it can be the seed that will get you through
                                        the moment and help you grow a life that you want to live.
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

export default ReasonsLive;
