import { AssessmentAnswers } from 'state/types';

import styles from './index.module.scss';

interface RankedReasonsLivingDyingProps {
    answers: Partial<AssessmentAnswers>;
}

const RankedReasonsLivingDying = ({ answers }: RankedReasonsLivingDyingProps) => {
    return (
        <div className={styles.reasonsTable}>
            <div className={styles.reasonsTableRow}>
                <div className={styles.tableLabel}>Rank</div>
                <div className={styles.tableLabelMedium}>Reasons For Living</div>
                <div className={styles.tableLabel}>Rank</div>
                <div className={styles.tableLabelMedium}>Reasons For Dying</div>
            </div>
            {Array(5)
                .fill(0)
                .map((_, i) => (
                    <div className={styles.reasonsTableRow} key={i}>
                        <div className={styles.boldItem}>{i + 1}</div>
                        <div className={styles.reasonsAnswer}>
                            {(answers['reasonsLive'] || [])[i] || ''}
                        </div>
                        <div className={styles.emptyItem} />
                        <div className={styles.boldItem}>{i + 1}</div>
                        <div className={styles.reasonsAnswer}>
                            {(answers['reasonsDie'] || [])[i] || ''}
                        </div>
                        <div className={styles.emptyItem} />
                    </div>
                ))}
        </div>
    );
};

export default RankedReasonsLivingDying;
