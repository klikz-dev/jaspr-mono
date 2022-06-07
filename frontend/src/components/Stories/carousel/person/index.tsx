import { useEffect, useRef } from 'react';
import scrollIntoView from 'smooth-scroll-into-view-if-needed';
import { Video } from 'state/types';
import StoryTab from '../../storytab';
import styles from './index.module.scss';

interface PersonProps {
    name: string;
    color: string;
    thumbnail: string;
    videos: Video[];
    setSelectedVideo: (video: Video | null) => void;
    open: boolean;
    toggleOpen: (open: boolean) => void;
    getPersonLabel: (name: string) => string;
}

const Person = ({
    name,
    color = 'rgb(128, 70, 124)',
    thumbnail,
    videos,
    setSelectedVideo,
    open,
    toggleOpen,
    getPersonLabel,
}: PersonProps) => {
    const containerRef = useRef<HTMLDivElement>(null!);
    // After expanding the stories, scroll the stories into view if it is offscreen
    // Timeouts should match the transition time for the container
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
            className={`${styles.person} ${open ? styles.personOpen : ''}`}
            style={{ backgroundColor: color || 'rgb(128, 70, 124)', cursor: 'pointer' }}
            ref={containerRef}
        >
            <div className={styles.details} onClick={() => toggleOpen(!open)}>
                <img className={styles.detailImage} src={thumbnail} alt={name} />
                <div className={styles.banner}>{name}</div>
            </div>
            <div className={styles.stories}>
                {videos?.map((video) => (
                    <StoryTab
                        key={video.name}
                        video={video}
                        label={getPersonLabel(video.name) || ''}
                        setSelectedVideo={setSelectedVideo}
                    />
                ))}
            </div>
        </div>
    );
};

export default Person;
