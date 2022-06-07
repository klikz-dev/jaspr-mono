import { Video } from 'state/types';
import { SelectedStory } from '../..';
import styles from './index.module.scss';

interface TopicProps {
    name: string;
    videos: Video[];
    setSelectedStory: (story: SelectedStory | null) => void;
}

const Topic = ({ name, videos, setSelectedStory }: TopicProps) => {
    return (
        <div className={styles.topic}>
            <div className={styles.details} onClick={() => setSelectedStory({ name, videos })}>
                <span className={styles.title}>{name}</span>
            </div>
        </div>
    );
};

export default Topic;
