import React from 'react';
import { Modal } from 'react-native';
import Styled from 'styled-components/native';
import styles from './index.module.scss';
import Person from './person';
import Topic from './topic';
import Stories from './stories';
import Video from 'components/Videos';
import { Video as VideoType, VideoRating } from 'state/types';
import { SelectedStory } from '..';

const ScrollContainer = Styled.View`flex: 1; background-color: #2F3251;`;
const StyledContainer = Styled.ScrollView`${styles.container} background-color: #2F3251;`;
const StyledTabs = Styled.View`${styles.tabs}`;
const StyledTab = Styled.TouchableOpacity<{ active: boolean }>`
    ${styles.tab}
    
    background-color: ${({ active }) => (active ? '#2F3251' : '#5C6499')}
`;
const StyledTabText = Styled.Text<{ active: boolean }>`${styles.tabText}
    color: ${({ active }) => (active ? '#ffffff' : '#2F3251')}
`;
const StyledCarouselContainer = Styled.View``;
const StyledCarousel = Styled.View`${styles.carousel}`;

interface Props {
    selectedVideo: VideoType | null;
    setTab: (tab: 'person' | 'topic') => void;
    topics: {
        name: string;
        color: string;
        videos: VideoType[];
    }[];
    people: {
        name: string;
        color: string;
        videos: VideoType[];
        thumbnail: string;
    }[];
    tab: 'person' | 'topic';
    setSelectedVideo: (video: VideoType | null) => void;
    getTopicLabel: (name: string) => string;
    getPersonLabel: (name: string) => string;
    setOpenThumbnail: (thumbnail: string | null) => void;
    save: () => void;
    rate: (rating: 0 | 1 | 2 | 3 | 4 | 5) => void;
    videoRating?: VideoRating;
    selectedStory: SelectedStory;
    setSelectedStory: (story: SelectedStory | null) => void;
}

const Render = ({
    selectedVideo,
    videoRating,
    save,
    rate,
    setSelectedVideo,
    setTab,
    setOpenThumbnail,
    setSelectedStory,
    tab,
    topics,
    people,
    selectedStory,
    getTopicLabel,
    getPersonLabel,
}: Props) => {
    return (
        <ScrollContainer>
            <StyledTabs>
                <StyledTab
                    onPress={() => {
                        setTab('person');
                        setOpenThumbnail(null);
                        setSelectedStory(null);
                    }}
                    active={tab === 'person'}
                >
                    <StyledTabText active={tab === 'person'}>By Person</StyledTabText>
                </StyledTab>
                <StyledTab
                    onPress={() => {
                        setTab('topic');
                        setOpenThumbnail(null);
                        setSelectedStory(null);
                    }}
                    active={tab === 'topic'}
                >
                    <StyledTabText active={tab === 'topic'}>By Topic</StyledTabText>
                </StyledTab>
            </StyledTabs>
            {!Boolean(selectedStory) && (
                <StyledContainer>
                    {tab === 'person' && (
                        <StyledCarouselContainer>
                            <StyledCarousel>
                                {people.map((person) => (
                                    <Person
                                        key={person.name}
                                        {...person}
                                        videos={person.videos}
                                        setSelectedStory={setSelectedStory}
                                    />
                                ))}
                            </StyledCarousel>
                        </StyledCarouselContainer>
                    )}
                    {tab === 'topic' && (
                        <StyledCarouselContainer>
                            <StyledCarousel>
                                {topics.map((topic) => (
                                    <Topic
                                        key={topic.name}
                                        {...topic}
                                        setSelectedStory={setSelectedStory}
                                        videos={topic.videos}
                                    />
                                ))}
                            </StyledCarousel>
                        </StyledCarouselContainer>
                    )}
                </StyledContainer>
            )}
            {Boolean(selectedStory) && selectedStory !== null && (
                <Stories
                    setSelectedStory={setSelectedStory}
                    selectedStory={selectedStory}
                    setSelectedVideo={setSelectedVideo}
                    getLabel={tab === 'person' ? getPersonLabel : getTopicLabel}
                />
            )}
            <Modal
                visible={Boolean(selectedVideo)}
                animationType="slide"
                presentationStyle="fullScreen"
                statusBarTranslucent
                supportedOrientations={['portrait', 'landscape']}
            >
                {Boolean(selectedVideo) && selectedVideo !== null && (
                    <Video
                        {...selectedVideo}
                        name={selectedVideo.name}
                        object={videoRating}
                        save={save}
                        rate={rate}
                        back={() => setSelectedVideo(null)}
                    />
                )}
            </Modal>
        </ScrollContainer>
    );
};

export default Render;
