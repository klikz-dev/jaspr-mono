import React, { useContext, useEffect } from 'react';
import Styled from 'styled-components/native';
import { useHistory } from 'lib/router';
import StoreContext from 'state/context/store';
import { getSkills } from 'state/actions/skills';
import { getStoriesVideos, getVideoRatings } from 'state/actions/stories';
import TitleMenu from 'components/TitleMenu';
import Menu from 'components/Menu';
import VideoLink from 'components/VideoLink';

const Container = Styled.View`
    flex: 1;
    background-color: #2F344F;
`;
const List = Styled.ScrollView``;
const VideoContainer = Styled.View`
    margin-vertical: 5px;
    margin-horizontal: 21px;
`;

const SkillContainer = Styled.TouchableOpacity`flex-direction: row; border-radius: 10px; overflow: hidden;  background-color: #41476A;`;
const SkillImageContainer = Styled.View`background-color: #000; flex-basis: 50%; resizeMode: contain`;
const TextContainer = Styled.View`flex-basis: 50%; padding: 8px; justify-content: center;`;
const Image = Styled.Image`height: 78px; width: 72px; align-self: flex-start; display: flex; margin-left: auto;`;
const Title = Styled.Text`
    color: #FFFEFE;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.1px;
`;

const Favorites = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { stories, skills } = store;
    const { videos, videoRatings } = stories;
    const { storiesFetched, ratingsFetched } = stories;

    // TODO Be smart about when to fetch
    useEffect(() => {
        if (!storiesFetched) {
            getStoriesVideos(dispatch);
        }

        if (!ratingsFetched) {
            getVideoRatings(dispatch);
        }

        if (skills.length === 0) {
            getSkills(dispatch);
        }
    }, [storiesFetched, ratingsFetched, skills.length, dispatch]);

    return (
        <Container>
            <TitleMenu label="My Favorites" />
            <List>
                {videoRatings
                    .filter((videoRating) => videoRating.saveForLater)
                    .map((videoRating) => {
                        return (
                            <VideoContainer key={videoRating.id}>
                                <VideoLink
                                    {...videos.find((video) => video.id === videoRating.video)}
                                />
                            </VideoContainer>
                        );
                    })}
                {skills
                    .filter((skill) => skill.saveForLater)
                    .filter((skill) => skill.video)
                    .map((skill) => (
                        <VideoContainer key={skill.id}>
                            <VideoLink
                                {...skill.video}
                                thumbnail={skill.thumbnailImage || skill.video.thumbnail}
                            />
                        </VideoContainer>
                    ))}
                {skills
                    .filter((skill) => skill.targetUrl)
                    .map((skill) => (
                        <VideoContainer key={skill.id}>
                            <SkillContainer onPress={() => history.push(skill.targetUrl)}>
                                <SkillImageContainer>
                                    <Image
                                        source={{ uri: skill.thumbnailImage }}
                                        resizeMode="cover"
                                        resizeMethod="resize"
                                    />
                                </SkillImageContainer>
                                <TextContainer>
                                    <Title>{skill.name}</Title>
                                </TextContainer>
                            </SkillContainer>
                        </VideoContainer>
                    ))}
            </List>
            <Menu selected="home" />
        </Container>
    );
};

export default Favorites;
