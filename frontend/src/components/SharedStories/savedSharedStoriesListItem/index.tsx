import { useState } from 'react';
import Modal, { Styles } from 'react-modal';
import styles from './index.module.scss';
import zIndexHelper from 'lib/zIndexHelper';
import CrossedPlus from 'components/CrossedPlus';
import Video from 'components/Videos';
import { Video as VideoType } from 'state/types';

interface SavedSharedStoriesListItemProps {
    video: VideoType;
    onRemove?: (video: VideoType) => void;
    setQuestionDisableAudio?: (disable: boolean) => void;
}

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'space-evenly',
        backgroundColor: 'rgba(45, 44, 63, 0.85)',
        zIndex: zIndexHelper('patient.shared-story-item'),
    },
    content: {
        position: 'absolute',
        top: 0,
        bottom: 0,
        right: 0,
        left: 0,
        padding: 0,
        borderRadius: 0,
    },
};

const SavedSharedStoriesListItem = (props: SavedSharedStoriesListItemProps) => {
    const { video, onRemove, setQuestionDisableAudio } = props;
    const [showVideo, setShowVideo] = useState(false);

    const onClickRemove = () => {
        if (onRemove) {
            onRemove(video);
        }
    };

    return (
        <li className={styles.item}>
            {onRemove && <CrossedPlus onClick={onClickRemove} size={24} />}
            <div
                className={styles.name}
                onClick={() => {
                    if (!onRemove) {
                        setShowVideo(true);
                        if (setQuestionDisableAudio) {
                            setQuestionDisableAudio(true);
                        }
                    }
                }}
            >
                {video.name}
            </div>

            <img
                src={video.thumbnail || undefined}
                alt={video.name}
                className={styles.image}
                onClick={() => {
                    if (!onRemove) {
                        if (setQuestionDisableAudio) {
                            setQuestionDisableAudio(true);
                        }

                        setShowVideo(true);
                    }
                }}
            />
            <Modal isOpen={showVideo} style={modalStyle}>
                <Video
                    video={video}
                    type="story"
                    back={() => {
                        if (setQuestionDisableAudio) {
                            setQuestionDisableAudio(false);
                        }

                        setShowVideo(false);
                    }}
                />
            </Modal>
        </li>
    );
};

export default SavedSharedStoriesListItem;
