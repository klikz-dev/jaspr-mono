import React, { useEffect, useRef, useState } from 'react';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

type TextQuestionProps = Pick<QuestionProps, 'answered' | 'answerKey' | 'setAnswered'> & {
    label: string;
    maxLength?: number;
};

const TextQuestion = (props: TextQuestionProps) => {
    const { answered, answerKey, label, maxLength, setAnswered } = props;
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<string>(answerKey, '', false);
    const inputRef = useRef<HTMLTextAreaElement>(null!);
    const measureRef = useRef<HTMLDivElement>(null!);
    const [rows, setRows] = useState(1);

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    const onChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const { value } = e.target;
        setAnswer(value);
        setAnswered(false);
        setRows(measureRef?.current?.offsetHeight / 25);
    };

    //const value = answers[answerKey] || '';
    const atLimit = updatedAnswer.length >= (maxLength | Infinity);
    // Show the character limit if we're in the last ~15% of the remaining characters.
    const showLimit = maxLength ? Math.floor(maxLength - maxLength * 0.15) : Infinity;

    return (
        <div className={styles.container}>
            <div className={styles.label}>{label}</div>
            <div className={styles.measure} ref={measureRef}>
                {updatedAnswer}
            </div>
            <textarea
                rows={rows > 2 ? rows : 2}
                placeholder="Type your response here"
                maxLength={maxLength}
                onChange={(e) => {
                    onChange(e);
                }}
                value={updatedAnswer}
                ref={inputRef}
            />

            {updatedAnswer.length >= showLimit && (
                <div
                    className={`${styles.charLimit} ${
                        atLimit ? styles.atLimit : styles.belowLimit
                    }`}
                >
                    {updatedAnswer.length}/{maxLength} characters {atLimit && '(at limit)'}
                </div>
            )}
        </div>
    );
};

export { TextQuestion };
export default TextQuestion;
