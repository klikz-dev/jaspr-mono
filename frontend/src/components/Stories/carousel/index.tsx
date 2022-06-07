import Modal, { Styles } from 'react-modal';
import { useLocation, useHistory } from 'react-router-dom';
import zIndexHelper from 'lib/zIndexHelper';
import styles from './index.module.scss';
import Topic from './topic';
import Person from './person';
import { Video as VideoType, VideoRating } from 'state/types';
import Video from 'components/Videos';
import Button from 'components/Button';

const modalStyle: Styles = {
    overlay: {
        zIndex: zIndexHelper('patient.story-video'),
    },
    content: {
        position: 'absolute',
        display: 'flex',
        alignSelf: 'center',
        backgroundColor: 'transparent',
        border: 'none',
        borderRadius: 0,
        padding: 0,
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
    },
};

interface CarouselStoriesProps {
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
    selectedVideo: VideoType | null;
    setSelectedVideo: (video: VideoType | null) => void;
    getTopicLabel: (name: string) => string;
    getPersonLabel: (name: string) => string;
    openThumbnail: string | null;
    setOpenThumbnail: (thumbnail: string | null) => void;
    save: () => void;
    rate: (rating: 0 | 1 | 2 | 3 | 4 | 5) => void;
    videoRating?: VideoRating;
}

const CarouselStories = ({
    topics,
    people,
    selectedVideo,
    setSelectedVideo,
    openThumbnail,
    setOpenThumbnail,
    getTopicLabel,
    getPersonLabel,
    save,
    videoRating,
    rate,
}: CarouselStoriesProps) => {
    const location = useLocation<{ from?: string }>();
    const history = useHistory();
    const goBack = () => {
        if (location.state?.from) {
            history.replace(location.state.from);
        } else {
            history.goBack();
        }
    };
    return (
        <div
            className={styles.container}
            style={{ background: 'linear-gradient(90deg, #383c58 0%, #343245 100%)' }}
        >
            <div className={styles.inner} style={{ overflowX: 'hidden' }}>
                <div
                    className={`${styles.titleControls} ${location.state?.from ? styles.back : ''}`}
                >
                    {location.state?.from && (
                        <Button variant="tertiary" dark onClick={goBack}>
                            Back
                        </Button>
                    )}
                    <h2 className={`typography--h4 ${styles.title}`}>Shared Stories</h2>
                </div>
                <div className={styles.carouselContainer}>
                    <span className={styles.header}>Search by topic</span>
                    <div className={styles.carousel}>
                        {topics.map((topic) => (
                            <Topic
                                key={topic.name}
                                name={topic.name}
                                color={topic.labelColor}
                                videos={topic.videos}
                                setSelectedVideo={setSelectedVideo}
                                getTopicLabel={getTopicLabel}
                                open={topic.name === openThumbnail}
                                toggleOpen={(open: Boolean) =>
                                    setOpenThumbnail(open ? topic.name : null)
                                }
                            />
                        ))}
                    </div>
                </div>
                <div className={styles.carouselContainer}>
                    <span className={styles.header}>Search by Person</span>
                    <div className={styles.carousel}>
                        {people.map((person) => (
                            <Person
                                key={person.name}
                                name={person.name}
                                color={person.labelColor}
                                thumbnail={person.thumbnail}
                                videos={person.videos}
                                setSelectedVideo={setSelectedVideo}
                                getPersonLabel={getPersonLabel}
                                open={person.name === openThumbnail}
                                toggleOpen={(open: Boolean) =>
                                    setOpenThumbnail(open ? person.name : null)
                                }
                            />
                        ))}
                    </div>
                </div>
            </div>
            <Modal isOpen={Boolean(selectedVideo)} style={modalStyle}>
                {selectedVideo && (
                    <Video video={selectedVideo} type="story" back={() => setSelectedVideo(null)} />
                )}
            </Modal>
        </div>
    );
};

export default CarouselStories;
