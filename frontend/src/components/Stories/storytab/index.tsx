import { useContext } from 'react';
import { Video } from 'state/types';
import { saveStoryForLater } from 'state/actions/stories';
import StoreContext from 'state/context/store';
import { ReactComponent as Heart } from 'assets/heart.svg';
import { ReactComponent as HeartFilled } from 'assets/heartFilled.svg';
import styles from './index.module.scss';

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
    const saved = videoRating?.saveForLater || false;
    const progress = videoRating?.progress || null;

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
        <div className={styles.container}>
            <div className={styles.row}>
                <div
                    className={styles.name}
                    onClick={() => setSelectedVideo(video)}
                    style={{ width: '190.5px' }}
                >
                    <span
                        className={styles.nameText}
                        style={{
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                            cursor: 'pointer',
                            overflow: 'hidden',
                            lineHeight: '20px',
                        }}
                    >
                        {label} ›
                    </span>
                </div>
                {ratingsFetched && (
                    <div className={styles.save} onClick={save} style={{ cursor: 'pointer' }}>
                        {!saved && <Heart />}
                        {saved && <HeartFilled />}
                    </div>
                )}
            </div>
            <div className={styles.progress}>
                <div className={styles.track} style={{ width: `${progress}%` }} />
            </div>
        </div>
    );
};

export default StoryTab;
