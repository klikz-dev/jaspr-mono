import styles from './index.module.scss';
import SavedSharedStoriesListItem from '../savedSharedStoriesListItem';
import SavedSharedStoriesListItemAdd from '../savedSharedStoriesListItemAdd';

import { Video } from 'state/types';

interface SavedSharedStoriesListProps {
    videos: Video[];
    onAdd?: () => void;
    onRemove?: (video: Video) => void;
    setQuestionDisableAudio?: (disable: boolean) => void;
}

const SavedSharedStoriesList = (props: SavedSharedStoriesListProps) => {
    const { videos, onAdd, onRemove, setQuestionDisableAudio } = props;
    return (
        <ul className={styles.list}>
            {videos.map((video) => (
                <SavedSharedStoriesListItem
                    video={video}
                    onRemove={onRemove}
                    key={video.id}
                    setQuestionDisableAudio={setQuestionDisableAudio}
                />
            ))}
            {onAdd && <SavedSharedStoriesListItemAdd onAdd={onAdd} />}
        </ul>
    );
};

export default SavedSharedStoriesList;
