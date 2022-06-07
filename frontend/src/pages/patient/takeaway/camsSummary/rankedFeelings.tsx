import { AssessmentAnswers } from 'state/types';
import styles from './index.module.scss';

type Props = {
    answers: Partial<AssessmentAnswers>;
};

const RankedFeelings = ({ answers }: Props) => {
    const numToFeeling = {
        1: ['Psychological pain', answers?.mostPainful || '', answers?.ratePsych || ''],
        2: ['Stress', answers?.mostStress || '', answers?.rateStress || ''],
        3: ['Agitation', answers?.causesAgitation || '', answers?.rateAgitation || ''],
        4: ['Hopelessness', answers?.mostHopeless || '', answers?.rateHopeless || ''],
        5: ['Self hate', answers?.mostHate || '', answers?.rateSelfHate || ''],
    };
    const questionsHaveBeenRanked = Boolean(answers.rankFeelings);

    const rankedFeelings = (answers.rankFeelings || '1,2,3,4,5')
        .split(',')
        // @ts-ignore
        .map((rank) => numToFeeling[rank]);

    return (
        <div className={styles.ratingTable}>
            <div className={styles.ratingTableRow}>
                <div className={styles.tableLabel}>{questionsHaveBeenRanked && <>Rank</>}</div>
                <div className={styles.tableLabel}>Item</div>
                <div className={styles.tableLabel}>Response</div>
                <div className={styles.tableLabel}>
                    <span>Rating </span>
                    <span>(1-5)</span>
                </div>
            </div>
            <div className={styles.divider} />
            {rankedFeelings.map((feelingArray, index) => (
                <div className={styles.ratingTableRow} key={index}>
                    <div className={styles.boldItem}>
                        {questionsHaveBeenRanked && <>{index + 1}</>}
                    </div>
                    <div className={styles.boldItem}>{feelingArray[0]}</div>
                    <div className={styles.italicsItemQuotes}>{feelingArray[1]}</div>
                    <div className={styles.item}>{feelingArray[2]}</div>
                    <div className={styles.emptyItem} />
                </div>
            ))}
        </div>
    );
};

export default RankedFeelings;
