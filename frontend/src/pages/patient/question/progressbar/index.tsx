import { useContext } from 'react';
import { AssignedActivities, AssignedActivity } from 'components/ConversationalUi/questions';
import StoreContext from 'state/context/store';
import styles from './index.module.scss';

interface ProgressBarProps {
    activities: AssignedActivities;
    toggleSummaries: () => void;
}

const ProgressBar = (props: ProgressBarProps) => {
    const [store] = useContext(StoreContext);
    const { assessment } = store;
    const { currentSectionUid } = assessment;
    const { activities, toggleSummaries } = props;

    const calculateProgress = (activity: AssignedActivity) => {
        if (activity.locked || activity.status === 'completed') {
            return 100;
        }
        const currentIndex = activity.questions.findIndex(
            (question) => question.uid === currentSectionUid,
        );
        if (currentIndex === -1) {
            return 0;
        }
        return (currentIndex / activity.questions.length) * 100;
    };

    return (
        <div className={styles.container}>
            <div className={styles.sections}>
                {activities
                    ?.filter((activity) => activity.progressBarLabel)
                    .map((activity) => (
                        <div className={styles.section} key={activity.progressBarLabel}>
                            <div className={styles.title}>{activity.progressBarLabel}</div>
                            <div className={styles.bar}>
                                <span
                                    className={styles.complete}
                                    style={{
                                        width: `${calculateProgress(activity)}%`,
                                    }}
                                />
                            </div>
                        </div>
                    ))}
            </div>
            <div className={styles.summaries} onClick={toggleSummaries}>
                Summaries
            </div>
        </div>
    );
};

export default ProgressBar;
