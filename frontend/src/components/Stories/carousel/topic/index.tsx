import { useEffect, useRef } from 'react';
import scrollIntoView from 'smooth-scroll-into-view-if-needed';
import StoryTab from '../../storytab';
import { Video } from 'state/types';
import styles from './index.module.scss';

interface TopicProps {
    name: string;
    color: string;
    videos: Video[];
    setSelectedVideo: (video: Video | null) => void;
    open: boolean;
    toggleOpen: (open: boolean) => void;
    getTopicLabel: (name: string) => string;
}

const Topic = ({
    name,
    color = 'rgb(128, 70, 124)',
    videos,
    setSelectedVideo,
    open,
    toggleOpen,
    getTopicLabel,
}: TopicProps): JSX.Element => {
    const containerRef = useRef<HTMLDivElement>(null!);

    useEffect(() => {
        let timeout: number | undefined;
        if (open && containerRef?.current) {
            timeout = window.setTimeout(() => {
                scrollIntoView(containerRef.current, {
                    behavior: 'smooth',
                    block: 'start',
                    scrollMode: 'if-needed',
                });
            }, 500);
        } else if (timeout) {
            window.clearTimeout(timeout);
        }
        return () => window.clearTimeout(timeout);
    }, [open]);

    return (
        <div
            className={`${styles.topic} ${open ? styles.topicOpen : ''}`}
            style={{ backgroundColor: color || 'rgb(128, 70, 124)', cursor: 'pointer' }}
            ref={containerRef}
        >
            <div
                className={`${styles.details} ${open ? styles.detailsClosed : ''}`}
                onClick={() => toggleOpen(!open)}
            >
                {name}
            </div>
            <div className={styles.stories}>
                <div className={styles.storyTitle}>{name}</div>
                {videos &&
                    videos.map((video) => (
                        <StoryTab
                            key={video.name}
                            video={video}
                            label={getTopicLabel(video.name) || ''}
                            setSelectedVideo={setSelectedVideo}
                        />
                    ))}
            </div>
        </div>
    );
};

export default Topic;
