import { Video } from 'state/types';
import { SelectedStory } from '../..';
import styles from './index.module.scss';

interface PersonProps {
    thumbnail: string;
    name: string;
    videos: Video[];
    setSelectedStory: (story: SelectedStory | null) => void;
}

const Person = (props: PersonProps) => {
    const { thumbnail, name, videos, setSelectedStory } = props;

    return (
        <div className={styles.person}>
            <div className={styles.details} onClick={() => setSelectedStory({ name, videos })}>
                <img
                    className={styles.profileImage}
                    src={thumbnail}
                    alt={name}
                    style={{ height: '100%' }}
                />
                <div className={styles.banner}>
                    <span className={styles.bannerText}>{name}</span>
                </div>
            </div>
        </div>
    );
};

export default Person;
