import { AnswerKeyType } from 'components/ConversationalUi/questions';
import React from 'react';
import { AssessmentAnswers } from 'state/types';
import styles from './scale.module.scss';

interface ScaleQuestionProps {
    idx: number;
    min: number;
    max: number;
    step: number;
    minLabel: string;
    maxLabel: string;
    question: string;
    answerKey: AnswerKeyType;
    inProgressAnswers: Partial<AssessmentAnswers>;
    setCurrentAnswers: (answers: Partial<AssessmentAnswers>) => void;
}

const ScaleQuestion = (props: ScaleQuestionProps) => {
    const {
        answerKey,
        inProgressAnswers,
        setCurrentAnswers,
        question,
        min,
        max,
        step,
        minLabel,
        maxLabel,
        idx,
    } = props;
    const options = [];
    for (let i = min; i <= max; i += step) {
        options.push(
            <React.Fragment key={i}>
                <label className={styles.option}>
                    <input
                        type="radio"
                        name={`scale-${idx}`}
                        checked={i === inProgressAnswers[answerKey]}
                        onChange={() =>
                            setCurrentAnswers({
                                ...inProgressAnswers,
                                [answerKey]: i,
                            })
                        }
                        value={inProgressAnswers[answerKey] || ''}
                    />
                    <span className={styles.checkmark} />
                    <span className={styles.value}>{i}</span>
                    {i === min && <div className={styles.leastImportant}>{minLabel}</div>}
                    {i === max && <div className={styles.mostImportant}>{maxLabel}</div>}
                </label>
                <div className={styles.rule} />
            </React.Fragment>,
        );
    }

    return (
        <>
            <div
                className={styles.instruction}
                dangerouslySetInnerHTML={{ __html: question }}
                style={{ paddingTop: props.idx ? '40px' : 0 }}
            />
            <div className={styles.scalebar}>{options.map((option) => option)}</div>
        </>
    );
};

export default ScaleQuestion;
