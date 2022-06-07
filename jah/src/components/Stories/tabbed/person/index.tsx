import React from 'react';
import { Video } from 'state/types';
import { SelectedStory } from '../..';
import Styled from 'styled-components/native';
import styles from './index.module.css';

const StyledContainer = Styled.View`${styles.person}`;
const Details = Styled.TouchableOpacity``;
const Image = Styled.Image`${styles.profileImage}`;
const Banner = Styled.View`${styles.banner} background-color: rgba(65,70,107,0.8)`;
const Name = Styled.Text`${styles.bannerText}`;

interface PersonProps {
    thumbnail: string;
    name: string;
    videos: Video[];
    setSelectedStory: (story: SelectedStory | null) => void;
}

const Person = (props: PersonProps) => {
    const { thumbnail, name, videos, setSelectedStory } = props;

    return (
        <StyledContainer>
            <Details onPress={() => setSelectedStory({ name, videos })}>
                <Image source={{ uri: thumbnail, cache: 'force-cache' }} />
                <Banner>
                    <Name>{name}</Name>
                </Banner>
            </Details>
        </StyledContainer>
    );
};

export default Person;
