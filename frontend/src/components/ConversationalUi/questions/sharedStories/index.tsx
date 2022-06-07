import styles from './index.module.scss';
import Stories from 'components/Stories';

const SharedStoriesQuestion = () => {
    return (
        <div className={styles.container}>
            <Stories tabbed />
        </div>
    );
};

export { SharedStoriesQuestion };
export default SharedStoriesQuestion;
