import React, { useContext, useEffect, useRef, useState } from 'react';
import Styled from 'styled-components/native';
import { LinearGradient } from 'expo-linear-gradient';
import { Modal, SafeAreaView } from 'react-native';
import { Video } from 'expo-av';
import StoreContext from 'state/context/store';
import ReplayIcon from 'assets/replay.svg';
import tempImage from './home.gif';
import { UIDType } from '../../questions';

type SlideshowProps = {
    currentQuestion: boolean;
    slides: {
        text: string;
        imageUrl: string;
    }[];
    next: (goTo?: UIDType) => void;
};

const InlineContainer = Styled.View`
    align-items: center;
    flex-direction: row;
    justify-content: space-around;
    width: 100%;
    height: 176px;
    margin-vertical: 20px;
    background-color: rgba(117, 121, 140, 0.21)
`;
const ReplayImage = Styled.Image`
    height: 126px;
    width: 72px;
`;
const ReplayColumn = Styled.View`
    flex-direction: column;
    align-items: center;
    justify-content: center;
`;
const ReplayText = Styled.Text`
    color: #595959;
    font-size: 19px;
    letter-spacing: -0.24px;
    line-height: 24px;
`;
const Description = Styled.Text`
    color: #595959;
    font-size: 20px;
    letter-spacing: -0.25px;
    line-height: 25px;
    margin-horizontal: 42px;
    
`;
const ImageContainer = Styled.View`
    flex: 1;
    margin-vertical: 10px;
`;
const Controls = Styled.View`
    flex-direction: row;
    height: 64px;
    flex-shrink: 0;
    justify-content: space-between;
    background-color: #FFFEFE;
    border-top-color: #D4D1D1;
    border-top-width: 10px;
`;
const Button = Styled.TouchableOpacity`
    justify-content: center;
    margin-horizontal: 42px;
`;
const ButtonText = Styled.Text`
    color: #8F98CC;
    font-size: 24px;
    letter-spacing: 0;
    line-height: 31px;
`;
const TouchableOpacity = Styled.TouchableOpacity``;

const Render = ({ slides, currentQuestion, next }: SlideshowProps) => {
    const [store] = useContext(StoreContext);
    const { media } = store;
    const { mediaUrl } = media.media;
    const videoEl = useRef<Video>();
    const [index, setIndex] = useState(0);
    const [showSlides, setShowSlides] = useState(false);
    const [initialized, setInitialized] = useState(false);
    const currentSlide = slides[index];
    const { text } = currentSlide;

    const nextSlide = () => {
        if (index < slides.length - 1) {
            setIndex(index + 1);
        } else {
            setShowSlides(false);
            setIndex(0);
        }
    };

    const prevSlide = () => {
        if (index > 0) {
            setIndex(index - 1);
        }
    };

    useEffect(() => {
        // Fix for https://github.com/facebook/react-native/issues/20394 and https://github.com/facebook/react-native/issues/19345
        // Related info: https://github.com/facebook/react-native/issues/10471
        const timer = setImmediate(() => {
            setShowSlides(true);
            setInitialized(true);
        });
        return () => clearImmediate(timer);
    }, []);

    useEffect(() => {
        if (initialized && currentQuestion && !showSlides) {
            next();
        }
    }, [currentQuestion, showSlides, next, initialized]);

    return (
        <>
            <InlineContainer>
                <ReplayColumn>
                    <ReplayImage source={tempImage} resizeMode="contain" />
                </ReplayColumn>
                <TouchableOpacity onPress={() => setShowSlides(true)}>
                    <ReplayColumn>
                        <ReplayIcon />
                        <ReplayText>Replay tutorial</ReplayText>
                    </ReplayColumn>
                </TouchableOpacity>
            </InlineContainer>
            <Modal visible={showSlides}>
                <LinearGradient style={{ flex: 1 }} colors={['#eeeef6', '#eeeef6']}>
                    <SafeAreaView
                        style={{
                            marginTop: 'auto',
                            marginBottom: 'auto',
                            minHeight: 150,
                            justifyContent: 'center',
                        }}
                    >
                        <Description>{text}</Description>
                    </SafeAreaView>
                    <ImageContainer key={currentSlide.imageUrl}>
                        <Video
                            source={{ uri: `${mediaUrl}${currentSlide.imageUrl}` }}
                            ref={videoEl}
                            rate={1.0}
                            isMuted={true}
                            resizeMode={Video.RESIZE_MODE_CONTAIN}
                            style={{ height: '100%', width: '100%', marginHorizontal: 'auto' }}
                            shouldPlay
                            isLooping
                        />
                    </ImageContainer>
                </LinearGradient>
                <Controls>
                    {index !== 0 && (
                        <Button onPress={prevSlide}>
                            <ButtonText>‹ Back</ButtonText>
                        </Button>
                    )}

                    <Button onPress={nextSlide} style={{ marginLeft: 'auto' }}>
                        <ButtonText>{index === slides.length - 1 ? 'Done' : 'Next'} ›</ButtonText>
                    </Button>
                </Controls>
            </Modal>
        </>
    );
};

export default Render;
