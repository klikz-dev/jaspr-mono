import StoryTab from '../../storytab';
import styles from './index.module.scss';
import { SelectedStory } from '../..';
import { Video } from 'state/types';

export interface ViewProps {
    setSelectedStory: (story: SelectedStory | null) => void;
    setSelectedVideo: (video: Video | null) => void;
    name: string;
    videos: Video[];
    getLabel: (name: string) => string;
}

interface StoriesProps extends Omit<ViewProps, 'name' | 'videos'> {
    selectedStory: SelectedStory;
}

const Stories = ({ setSelectedStory, setSelectedVideo, selectedStory, getLabel }: StoriesProps) => {
    const { name, videos } = selectedStory;

    return (
        <div className={styles.container}>
            <div className={styles.header} onClick={() => setSelectedStory(null)}>
                <span className={styles.headerText}>{name}</span>
            </div>
            <div className={styles.videosContainer}>
                {videos &&
                    videos.map((video) => {
                        return (
                            <StoryTab
                                key={video?.id}
                                video={video}
                                label={getLabel(video?.name)}
                                setSelectedVideo={() => setSelectedVideo(video)}
                            />
                        );
                    })}
            </div>
        </div>
    );
};

export default Stories;
