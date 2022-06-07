import React from 'react';
import { SelectedStory } from '../..';
import { Video } from 'state/types';
import Styled from 'styled-components/native';
import StoryTab from '../../storytab';
import styles from './index.module.css';

const Container = Styled.View`${styles.container}`;
const Header = Styled.TouchableOpacity`${styles.header}`;
const HeaderText = Styled.Text`${styles.headerText}`;
const VideosContainer = Styled.ScrollView`${styles.videosContainer}`;
const Close = Styled.TouchableOpacity`
    position: absolute;
    top: 10px;
    right: 20px;
`;
const CloseText = Styled.Text`
    color: #ffffff;
    font-size: 30px;
    font-weight: bold;
`;

export interface StoriesProps {
    setSelectedStory: (story: SelectedStory | null) => void;
    setSelectedVideo: (video: Video | null) => void;
    selectedStory: SelectedStory;
    getLabel: (name: string) => string;
}

const Stories = ({ setSelectedStory, setSelectedVideo, selectedStory, getLabel }: StoriesProps) => {
    const { name, videos } = selectedStory;
    return (
        <Container>
            <Close onPress={() => setSelectedStory(null)}>
                <CloseText>✕</CloseText>
            </Close>
            <Header>
                <HeaderText>{name}</HeaderText>
            </Header>
            <VideosContainer>
                {videos &&
                    videos.map((video) => (
                        <StoryTab
                            key={video.id}
                            video={video}
                            label={getLabel(video.name)}
                            setSelectedVideo={() => setSelectedVideo(video)}
                        />
                    ))}
            </VideosContainer>
        </Container>
    );
};

export default Stories;
