import React, { useState } from 'react';
import { Modal } from 'react-native';
import Styled from 'styled-components/native';
import { addAction, actionNames } from 'state/actions/analytics';
import InfoModal from 'components/InfoModal';
import VideoPlayer from 'components/Videos/Player';
import { Video as VideoType } from 'state/types';

const sharedStoryInfo =
    'During our darkest of moments of despair, knowing that there are other people who get it, who have survived their own pain, can be powerful and comforting. It can touch you in a way that no one else can. Hearing how people have struggled, then changed their lives helps to not feel so alone. It can give hope for the future and give ideas of how to get through some of the hardest times of your life.';
const videoInfo =
    "There is no better time to have crisis survival skills at the ready than when you're in a crisis. Explore the many different ways to get through really difficult moments with distraction activities, watching soothing videos and hearing comforting sounds. Learn from people with lived experience how to change intense negative emotions you want to change, and how to take better control of your mind and painful thoughts.";

const Container = Styled.View`
    position: relative;
    flex: 1;
    background-color: #2F344F;
    padding-top: 80px;
`;
const Title = Styled.Text`
    width: 100%;
    color: #FFFFFF;
    font-size: 32px;
    letter-spacing: 0;
    line-height: 38px;
    text-align: center;
    margin-vertical: 20px;
`;
const Description = Styled.ScrollView`
    flex: 1;
`;
const DescriptionText = Styled.Text`
    color: #F8F8F8;
    font-size: 16px;
    letter-spacing: 0;
    line-height: 24px;
    padding-horizontal: 26px;
`;
const TouchableOpacity = Styled.TouchableOpacity``;
const TheWhy = Styled.Text`
    margin-top: 10px;
    color: #6CC5D4;
    font-size: 16px;
    font-style: italic;
    font-weight: 300;
    line-height: 19px;
    text-align: center;
`;

type VideoProps = {
    sharedStory?: boolean;
    showDescription?: boolean;
    description: string;
    name: string;
} & VideoType;

const Video = ({
    sharedStory = false,
    showDescription = false,
    description,
    name,
    ...video
}: VideoProps) => {
    const [showInfo, setShowInfo] = useState(false);

    const showInfoModal = () => {
        addAction(actionNames.JAH_WALKTHROUGH_CLICKED_MORE_INFO, {
            extra: sharedStory ? 'Shared Story Video' : 'Comfort & Skill Video',
        });
        setShowInfo(true);
    };

    return (
        <Container>
            <VideoPlayer {...video} />
            <Title>{name}</Title>
            <Description>
                {showDescription && <DescriptionText>{description}</DescriptionText>}
                {!showDescription && (
                    <TouchableOpacity onPress={showInfoModal}>
                        <TheWhy>The why behind this ›</TheWhy>
                    </TouchableOpacity>
                )}
            </Description>
            <Modal visible={showInfo} animationType="fade" transparent={true}>
                <InfoModal
                    title={sharedStory ? 'Shared Story Video' : 'Comfort & Skill Video'}
                    body={sharedStory ? sharedStoryInfo : videoInfo}
                    close={() => setShowInfo(false)}
                />
            </Modal>
        </Container>
    );
};

export default Video;
