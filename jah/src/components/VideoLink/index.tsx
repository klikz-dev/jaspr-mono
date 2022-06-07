import React, { useContext, useState } from 'react';
import { Modal } from 'react-native';
import Styled from 'styled-components/native';
import StoreContext from 'state/context/store';
import { rateVideo, saveStoryForLater } from 'state/actions/stories';
import Video from 'components/Videos';

import PlayButton from 'assets/play.png';

const Container = Styled.TouchableOpacity`flex-direction: column; border-radius: 10px; overflow: hidden;  background-color: #41476A;`;
const Row = Styled.View`flex-direction: row;`;
const VideoContainer = Styled.View`background-color: #000; flex-basis: 50%; resizeMode: contain`;
const TextContainer = Styled.View`flex-basis: 50%; padding: 8px; justify-content: center;`;
const Image = Styled.Image`height: 78px; width: 72px; align-self: flex-start; display: flex; margin-left: auto;`;
const PlayButtonImage = Styled.Image`
    position: absolute;
    top: 50%;
    left: 50%;
    width: 40px;
    height: 26px;
    margin-left: -20px;
    margin-top: -13px;
`;
const Title = Styled.Text`
    color: #FFFEFE;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.1px;
`;

const Progress = Styled.View`
    width: 100%;
    height: 6px;
`;
const ProgressTrack = Styled.View`
    height: 6px;
    background-color: #50A7BD;
`;

interface VideoLinkProps {
    id?: number;
    thumbnail: string;
    name: string;
    mp4Transcode?: string;
    hlsPlaylist: string;
    fpm4Transcode: string;
}

const VideoLink = ({ id, thumbnail, name, ...rest }: VideoLinkProps) => {
    const [showVideo, setShowVideo] = useState(false);
    const [store, dispatch] = useContext(StoreContext);
    const { stories } = store;
    const { videoRatings } = stories;
    const videoRating = videoRatings.find((rating) => rating.video === id);

    const rate = (rating: 0 | 1 | 2 | 3 | 4 | 5) => {
        rateVideo(dispatch, videoRating?.id || null, id, rating);
    };

    const save = () => {
        const saveForLater = videoRating ? videoRating.saveForLater : false;
        saveStoryForLater(dispatch, videoRating?.id || null, id, !saveForLater);
    };

    return (
        <Container onPress={() => setShowVideo(true)}>
            <Row>
                <VideoContainer>
                    <Image source={{ uri: thumbnail }} resizeMode="cover" resizeMethod="resize" />
                    <PlayButtonImage source={PlayButton} />
                </VideoContainer>
                <TextContainer>
                    <Title>{name}</Title>
                </TextContainer>
            </Row>
            <Progress>
                <ProgressTrack style={{ width: `${videoRating?.progress || 0}%` }} />
            </Progress>

            <Modal
                visible={Boolean(showVideo)}
                animationType="slide"
                supportedOrientations={['portrait', 'landscape']}
            >
                <>
                    {Boolean(showVideo) && (
                        <Video
                            id={id}
                            name={name}
                            {...rest}
                            poster={thumbnail}
                            object={videoRating}
                            save={save}
                            rate={rate}
                            back={() => setShowVideo(false)}
                        />
                    )}
                </>
            </Modal>
        </Container>
    );
};

export default VideoLink;
