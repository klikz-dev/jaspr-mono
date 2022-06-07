import { useState } from 'react';
import Modal, { Styles } from 'react-modal';
import Video from 'components/Videos';
import { Video as VideoType } from 'state/types';
import styles from '../index.module.scss';

interface VideoTileProps {
    video: VideoType;
    name?: string;
    thumbnailSrc?: string | null;
    thumbnailAlt?: string;
    setQuestionDisableAudio?: (disableAudio: boolean) => void;
}

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'space-evenly',
        backgroundColor: 'rgba(45, 44, 63, 0.85)',
    },
    content: {
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        position: 'static',
        display: 'flex',
        alignSelf: 'center',
        backgroundColor: 'transparent',
        border: 'none',
        borderRadius: '5px',
        padding: 0,
        height: '100%',
        overflow: 'hidden',
    },
};

const VideoTile = (props: VideoTileProps) => {
    const { video, name, thumbnailSrc, thumbnailAlt, setQuestionDisableAudio = () => {} } = props;
    const [showVideo, setShowVideo] = useState(false);

    const src = thumbnailSrc || video.thumbnail;

    const openVideo = () => {
        setQuestionDisableAudio(true);
        setShowVideo(true);
    };

    return (
        <div className={`${styles.favorite} ${styles.showPointer}`}>
            <div className={styles.favoriteInner}>
                <img
                    src={src || undefined}
                    alt={thumbnailAlt || video.name}
                    onClick={openVideo}
                    className={styles.favoriteImage}
                    style={{ width: '100%', objectFit: 'cover' }}
                />
                <div className={`${styles.name} ${styles.nameText}`} onClick={openVideo}>
                    {name || video.name}
                </div>
            </div>
            {video && (
                <Modal isOpen={showVideo} style={modalStyle}>
                    <Video
                        video={video}
                        type="story"
                        back={() => {
                            setQuestionDisableAudio(false);
                            setShowVideo(false);
                        }}
                    />
                </Modal>
            )}
        </div>
    );
};

export default VideoTile;
