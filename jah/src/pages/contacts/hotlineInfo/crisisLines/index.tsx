import React, { useContext } from 'react';
import { Platform } from 'react-native';
import Styled from 'styled-components/native';
import { useHistory } from 'lib/router';
import StoreContext from 'state/context/store';
import TitleMenu from 'components/TitleMenu';
import Menu from 'components/Menu';
import VideoLink from 'components/VideoLink';

const Container = Styled.View`
    flex: 1;
    background-color: #2F344F;
`;
const List = Styled.ScrollView``;

const MoreButton = Styled.TouchableOpacity`
    height: 56px;
    flex-direction: row;
    align-items: center;
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

const VideoContainer = Styled.View<{ isIOS: boolean }>`
    margin-vertical: 5px;
    margin-horizontal: 21px;
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

const HotlineInfoCrisisLines = () => {
    const history = useHistory();
    const [store] = useContext(StoreContext);
    const { media } = store.media;
    const { crisisLines } = media;
    const { hls, dash, poster, video } = crisisLines;

    return (
        <Container>
            <TitleMenu label="Crisis Line Shared Story" />
            <List>
                <VideoContainer isIOS={Platform.OS === 'ios'}>
                    <VideoLink
                        thumbnail={poster}
                        mp4Transcode={video}
                        hlsPlaylist={hls}
                        fpm4Transcode={dash}
                        name="Riley - Crisis Lines"
                    />
                </VideoContainer>
            </List>
            <MoreButton onPress={() => history.push('/jah-contacts/hotline-info')}>
                <MoreText>National Hotlines</MoreText>
                <RightPointer>›</RightPointer>
            </MoreButton>
            <Menu selected="contacts" />
        </Container>
    );
};

export default HotlineInfoCrisisLines;
