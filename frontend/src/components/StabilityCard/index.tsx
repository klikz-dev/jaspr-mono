import logo from 'assets/logo.png';
import styles from './index.module.scss';
import { AssessmentAnswers } from 'state/types';

type StabilityCardProps = {
    empty?: boolean;
    provider?: boolean;
    patient?: {
        lastName?: string;
        firstName?: string;
        dateOfBirth?: string;
        mrn?: string;
        ssid?: string;
        lastLoggedInAt?: string;
    };
    answers: AssessmentAnswers;
};

const StabilityCard = ({ empty = false, answers = {} }: StabilityCardProps) => {
    const { copingTop = [], reasonsLive = [], wsTop = [] } = answers;

    return (
        <div className={styles.container}>
            <div className={styles.card}>
                <div className={styles.column}>
                    <div className={styles.header}>My Stability Plan</div>
                    <div className={styles.sectionHeader}>Coping Strategies</div>
                    <div className={styles.section}>
                        <ul>
                            {!empty && (
                                <li>
                                    Limit access to means to keep myself safe (see Takeaway Kit)
                                </li>
                            )}
                            {!empty &&
                                Array.isArray(copingTop) &&
                                copingTop.map((cope) => <li key={cope}>{cope}</li>)}
                            <li>Watch Jaspr videos</li>
                            {!empty && (
                                <li>24/7 National Hotline, call 1-800-273-8255, text 741741</li>
                            )}
                        </ul>
                    </div>
                    <img src={logo} alt="Jaspr" className={styles.logo} />
                </div>
                <div className={styles.column}>
                    <div className={styles.header}></div>
                    <div className={styles.sectionHeader}>Reasons for Living</div>
                    <div className={styles.section}>
                        <ol>
                            {!empty &&
                                (reasonsLive || []).map((reason) => <li key={reason}>{reason}</li>)}
                        </ol>
                    </div>
                    <div className={styles.sectionHeader}>When to Use My Plan</div>
                    {!empty && (
                        <div className={styles.section}>
                            I commit to using my plan when I experience any of the following warning
                            signs:
                            <ul>
                                {Array.isArray(wsTop) &&
                                    wsTop.map((sign) => <li key={sign}>{sign}</li>)}
                            </ul>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export { StabilityCard };
export default StabilityCard;
