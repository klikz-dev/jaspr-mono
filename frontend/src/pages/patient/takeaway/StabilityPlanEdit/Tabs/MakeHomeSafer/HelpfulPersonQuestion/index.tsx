import React from 'react';
import styles from './index.module.scss';
import { AssessmentAnswers } from 'state/types';

interface HelpfulPersonQuestionProps {
    answers: Partial<AssessmentAnswers>;
    setAnswers: (
        answers: AssessmentAnswers | ((answers: AssessmentAnswers) => AssessmentAnswers),
    ) => void;
}

const HelpfulPersonQuestion = ({ answers, setAnswers }: HelpfulPersonQuestionProps) => {
    const { meansSupportYesNo, meansSupportWho = '' } = answers;

    const meansSupportToggle = ({ target }: React.ChangeEvent<HTMLInputElement>) => {
        const { value, checked } = target;
        if ((value === 'true' && !checked) || (value === 'false' && !checked)) {
            setAnswers((answers) => ({ ...answers, meansSupportYesNo: null }));
        } else if (value === 'true' && checked) {
            setAnswers((answers) => ({ ...answers, meansSupportYesNo: true }));
        } else if (value === 'false' && checked) {
            setAnswers((answers) => ({ ...answers, meansSupportYesNo: false }));
        }
    };

    const changeMeansSupportWho = ({ target }: React.ChangeEvent<HTMLInputElement>) => {
        const { value } = target;
        setAnswers((answers) => ({ ...answers, meansSupportWho: value }));
    };

    return (
        <div className={styles.container}>
            <div className={styles.row}>
                <div className={styles.question}>
                    In your situation, can someone help you take these steps
                </div>
                <div className={styles.yesno}>
                    <label
                        className={`${styles.label} ${styles.yes} ${
                            meansSupportYesNo === true ? styles.checked : ''
                        }`}
                    >
                        Yes
                        <input
                            className={styles.checkbox}
                            type="checkbox"
                            onChange={meansSupportToggle}
                            checked={meansSupportYesNo === true}
                            value="true"
                        />
                    </label>
                    <label
                        className={`${styles.label} ${styles.no} ${
                            meansSupportYesNo === false ? styles.checked : ''
                        }`}
                    >
                        No
                        <input
                            className={styles.checkbox}
                            type="checkbox"
                            onChange={meansSupportToggle}
                            checked={meansSupportYesNo === false} // Not null
                            value="false"
                        />
                    </label>
                </div>
            </div>
            <div className={styles.row}>
                <div className={`${styles.question} ${styles.whoQuestion}`}>Who?</div>
                <input
                    className={styles.who}
                    value={meansSupportWho ? meansSupportWho : ''}
                    onChange={changeMeansSupportWho}
                    placeholder="Type your response here"
                />
            </div>
        </div>
    );
};

export default HelpfulPersonQuestion;
