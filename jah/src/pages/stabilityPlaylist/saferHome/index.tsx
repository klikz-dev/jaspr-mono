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

const ReasonsLive = (): JSX.Element => {
    const [store] = useContext(StoreContext);
    const { crisisStabilityPlan, media } = store;
    const { isFullScreen } = media;
    const { saferHome = {} } = media.media;
    const {
        meansSupportWho,
        strategiesCustom,
        strategiesFirearm,
        strategiesGeneral,
        strategiesMedicine,
        strategiesOther,
        strategiesPlaces,
    } = crisisStabilityPlan;

    const hasContent =
        strategiesCustom?.length ||
        strategiesFirearm?.length ||
        strategiesGeneral?.length ||
        strategiesMedicine?.length ||
        strategiesOther?.length ||
        strategiesPlaces?.length;

    const { dash, hls, video, poster } = saferHome;

    return (
        <Container>
            {!isFullScreen && <TitleMenu label="Making Home Safer" />}
            <VideoPlayer
                poster={poster}
                fpm4Transcode={dash}
                hlsPlaylist={hls}
                mp4Transcode={video}
                name="Learn more about making home safer"
            />
            {!isFullScreen && (
                <>
                    <Inner>
                        <TopContainer
                            title="To Protect Myself I Plan To:"
                            link="/jah-stability-playlist/making-home-safer/full"
                            showPencil
                            moreLabel={hasContent ? 'View Other Steps to Protect Myself' : null}
                            moreLink="/jah-stability-playlist/making-home-safer/edit"
                        >
                            <Labels>
                                {strategiesGeneral?.map((strategy) => (
                                    <Item key={strategy} label={strategy} />
                                ))}
                                {Boolean(meansSupportWho) && (
                                    <Item
                                        label={`I will ask ${meansSupportWho} for help with this plan`}
                                    />
                                )}
                            </Labels>
                            {!hasContent && (
                                <DescriptionContainer>
                                    <Description>
                                        Overwhelming feelings can make it very hard to think
                                        clearly. When this happens, the urge to die can feel like
                                        the only way to escape the pain. The fact is that
                                        overwhelming emotions do pass with time. One important step
                                        you can take for your own safety is to get some distance
                                        between you and the things you might use to harm yourself.
                                        This can give you enough time for your emotions to pass and
                                        for you to take steps to get help. The plan doesn’t have to
                                        be forever, but long enough to give you a chance to get
                                        through dark moments when they come up.. Making your home
                                        safe may be the single most important thing you can do to
                                        save your life.
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
