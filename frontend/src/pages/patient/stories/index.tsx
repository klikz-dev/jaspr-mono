import Menu from 'components/Menu';
import SharedStories from 'components/Stories';
import styles from './index.module.scss';

const Stories = () => {
    return (
        <div className={styles.container}>
            <Menu selectedItem="stories" dark />
            <SharedStories />
        </div>
    );
};

export default Stories;
