import React, { useContext } from 'react';
import Styled from 'styled-components/native';
import TitleMenu from 'components/TitleMenu';
import ContactButtons from '../contactButtons';
import VideoPlayer from 'components/Videos/Player';
import StoreContext from 'state/context/store';

import Menu from 'components/Menu';

const Container = Styled.View`
    flex: 1;
    background-color: #2F344F;
`;
const Content = Styled.ScrollView``;
const Text = Styled.Text`
    padding: 28px;
    color: #FFFEFE;
    font-size: 16px;
    font-weight: 300;
    line-height: 24px;
`;

const WhatToExpect = () => {
    const [store] = useContext(StoreContext);
    const { media } = store.media;
    const { crisisLinesExpect } = media;
    const { hls, dash, poster, video } = crisisLinesExpect;

    return (
        <Container>
            <TitleMenu label="What to Expect" />
            <VideoPlayer
                poster={poster}
                fpm4Transcode={dash}
                hlsPlaylist={hls}
                mp4Transcode={video}
                name="National Lifeline: What to Expect"
            />
            <Content>
                <Text>
                    After introducing themselves, the first thing the crisis line volunteer may ask
                    you is your name. You don’t have to give it if you don’t want to. Next, they
                    will ask something like, “What’s going on for you today?” At this point, you
                    control the conversation, including what to say and how much detail to provide.
                    Their job then is to listen and offer support. If you are in crisis, they will
                    ask if you have a safety plan for what to do in situations like the one you are
                    in. If you do, they’ll help you figure out how best to use it. When callers
                    don’t have a safety plan, they will help create one. Their goal in these
                    situations is to think with you about how to stay safe for the next couple of
                    hours and days, and to figure out when it’s a good idea to call the crisis line
                    back.
                </Text>
            </Content>
            <ContactButtons />
            <Menu selected="contacts" />
        </Container>
    );
};

export default WhatToExpect;
