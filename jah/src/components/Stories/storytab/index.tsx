import React, { useContext } from 'react';
import { Video } from 'state/types';
import { saveStoryForLater } from 'state/actions/stories';
import StoreContext from 'state/context/store';
import Heart from 'assets/heart.svg';
import HeartFilled from 'assets/heartFilled.svg';
import Styled from 'styled-components/native';
import styles from './index.module.css';

const Container = Styled.View`${styles.container}`;
const Row = Styled.View`${styles.row}`;
const Name = Styled.TouchableOpacity`${styles.name}`;
const NameText = Styled.Text`${styles.nameText}`;
const Save = Styled.TouchableOpacity`${styles.save}`;
const Progress = Styled.View`${styles.progress}`;
const Track = Styled.View<{ progress: number | null }>`${styles.track} width: ${({ progress }) =>
    progress ? `${progress}%` : '0'}`;

interface StoryTabProps {
    label: string;
    setSelectedVideo: (video: Video | null) => void;
    video: Video;
}

const StoryTab = (props: StoryTabProps) => {
    const { label, setSelectedVideo, video } = props;
    const [store, dispatch] = useContext(StoreContext);
    const { stories } = store;
    const { ratingsFetched, videoRatings } = stories;

    const videoRating = videoRatings.find((rating) => rating.video === video?.id);
    const progress = videoRating?.progress || null;
    const saved = videoRating?.saveForLater || undefined;

    const save = (): void => {
        if (videoRating) {
            saveStoryForLater(
                dispatch,
                videoRating.id || null,
                video.id,
                !videoRating.saveForLater,
            );
        } else {
            saveStoryForLater(dispatch, null, video.id, true);
        }
    };

    return (
        <Container>
            <Row>
                <Name onPress={() => setSelectedVideo(null)}>
                    <NameText numberOfLines={1}>{label} ›</NameText>
                </Name>
                {ratingsFetched && (
                    <Save onPress={save}>
                        {!saved && <Heart />}
                        {saved && <HeartFilled />}
                    </Save>
                )}
            </Row>
            <Progress>
                <Track progress={progress} />
            </Progress>
        </Container>
    );
};

export default StoryTab;
