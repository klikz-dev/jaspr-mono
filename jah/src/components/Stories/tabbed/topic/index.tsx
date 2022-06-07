import React from 'react';
import Styled from 'styled-components/native';
import styles from './index.module.css';
import { Video } from 'state/types';
import { SelectedStory } from '../..';

const StyledTopic = Styled.View`${styles.topic}`;
const StyledDetails = Styled.TouchableOpacity`${styles.details}`;
const StyledTitle = Styled.Text`${styles.title}`;

interface TopicProps {
    name: string;
    videos: Video[];
    setSelectedStory: (story: SelectedStory | null) => void;
}

export type ViewProps = TopicProps;

const Topic = ({ name, videos, setSelectedStory }: TopicProps) => {
    return (
        <StyledTopic>
            <StyledDetails onPress={() => setSelectedStory({ name, videos })}>
                <StyledTitle>{name}</StyledTitle>
            </StyledDetails>
        </StyledTopic>
    );
};

export default Topic;
