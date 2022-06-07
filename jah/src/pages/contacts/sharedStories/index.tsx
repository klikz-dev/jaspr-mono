import React, { useContext, useEffect } from 'react';
import { Platform } from 'react-native';
import Styled from 'styled-components/native';
import { useHistory } from 'lib/router';
import { addAction, actionNames } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import { getStoriesVideos, getVideoRatings } from 'state/actions/stories';
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

const SupportivePeopleSharedStories = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { stories } = store;
    const { storiesFetched, ratingsFetched } = stories;
    const { videos } = stories;

    useEffect(() => {
        if (!storiesFetched) {
            getStoriesVideos(dispatch);
        }
        if (!ratingsFetched) {
            getVideoRatings(dispatch);
        }
    }, [dispatch, storiesFetched, ratingsFetched]);

    useEffect(() => {
        addAction(actionNames.JAH_ARRIVE_SS_SUPPORTIVE_PEOPLE);
    }, []);

    return (
        <Container>
            <TitleMenu label="Shared Stories: Supportive People" />
            <List>
                {videos
                    .filter((video) => video?.tags.includes('Supportive People'))
                    .map((video) => (
                        <VideoContainer key={video.id} isIOS={Platform.OS === 'ios'}>
                            <VideoLink {...video} />
                        </VideoContainer>
                    ))}
            </List>
            <MoreButton onPress={() => history.push('/jah-supportive-people')}>
                <MoreText>My Supportive People</MoreText>
                <RightPointer>›</RightPointer>
            </MoreButton>
            <Menu selected="contacts" />
        </Container>
    );
};

export default SupportivePeopleSharedStories;
