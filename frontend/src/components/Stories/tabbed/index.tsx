import Modal, { Styles } from 'react-modal';
import zIndexHelper from 'lib/zIndexHelper';
import styles from './index.module.scss';
import Person from './person';
import Topic from './topic';
import Stories from './stories';
import Video from 'components/Videos';
import { Video as VideoType, VideoRating } from 'state/types';
import { SelectedStory } from '..';

const modalStyle: Styles = {
    overlay: {
        zIndex: zIndexHelper('patient.story-video'),
    },
    content: {
        position: 'absolute',
        display: 'flex',
        alignSelf: 'center',
        border: 'none',
        borderRadius: 0,
        padding: 0,
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
    },
};

interface Props {
    selectedVideo: VideoType | null;
    setTab: (tab: 'person' | 'topic') => void;
    topics: {
        name: string;
        labelColor: string;
        videos: VideoType[];
    }[];
    people: {
        name: string;
        labelColor: string;
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
    selectedStory?: SelectedStory | null;
    setSelectedStory: (story: SelectedStory | null) => void;
}

const TabbedStories = ({
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
        <div style={{ flex: 1, backgroundColor: 'white' }}>
            <div className={styles.tabs}>
                <div
                    className={styles.tab}
                    onClick={() => {
                        setTab('person');
                        setOpenThumbnail(null);
                        setSelectedStory(null);
                    }}
                    style={{
                        cursor: 'pointer',
                        color: tab === 'person' ? '#000' : '#fff',
                        backgroundColor: tab === 'person' ? '#fff' : '#e5e5e5',
                    }}
                >
                    <span className={styles.tabText}>By Person</span>
                </div>
                <div
                    className={styles.tab}
                    onClick={() => {
                        setTab('topic');
                        setOpenThumbnail(null);
                        setSelectedStory(null);
                    }}
                    style={{
                        cursor: 'pointer',
                        color: tab === 'topic' ? '#000' : '#fff',
                        backgroundColor: tab === 'topic' ? '#fff' : '#e5e5e5',
                    }}
                >
                    <span className={styles.tabText}>By Topic</span>
                </div>
            </div>
            {!Boolean(selectedStory) && (
                <div className={styles.container}>
                    {tab === 'person' && (
                        <div>
                            <div className={styles.carousel}>
                                {people.map((person) => (
                                    <Person
                                        key={person.name}
                                        {...person}
                                        videos={person.videos}
                                        setSelectedStory={setSelectedStory}
                                    />
                                ))}
                            </div>
                        </div>
                    )}
                    {tab === 'topic' && (
                        <div>
                            <div className={styles.carousel}>
                                {topics.map((topic) => (
                                    <Topic
                                        key={topic.name}
                                        {...topic}
                                        setSelectedStory={setSelectedStory}
                                    />
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
            {selectedStory !== null && selectedStory !== undefined && (
                <Stories
                    setSelectedStory={setSelectedStory}
                    selectedStory={selectedStory}
                    setSelectedVideo={setSelectedVideo}
                    getLabel={tab === 'person' ? getPersonLabel : getTopicLabel}
                />
            )}
            <Modal isOpen={Boolean(selectedVideo)} style={modalStyle}>
                {selectedVideo && (
                    <Video video={selectedVideo} type="story" back={() => setSelectedVideo(null)} />
                )}
            </Modal>
        </div>
    );
};

export default TabbedStories;
