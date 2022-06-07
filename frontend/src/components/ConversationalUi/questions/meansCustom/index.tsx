import React, { useContext, useEffect, useRef, useState } from 'react';
import StoreContext from 'state/context/store';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

type AddCustomStrategyProps = Pick<QuestionProps, 'setAnswered'> & {
    setAnswer: (answer: string[]) => void;
    updatedAnswer: string[];
};

const AddCustomStrategy = (props: AddCustomStrategyProps) => {
    const { setAnswered, setAnswer, updatedAnswer } = props;

    const [isEditing, setIsEditing] = useState(false);
    const [strategy, setStrategy] = useState('');
    const inputRef = useRef<HTMLInputElement>(null!);
    const measureRef = useRef<HTMLDivElement>(null!);

    const saveStrategy = () => {
        if (strategy !== '') {
            setAnswer([...updatedAnswer, strategy]);
        }
        setIsEditing(false);
        setStrategy('');
    };

    useEffect(() => {
        if (isEditing && inputRef && inputRef.current) {
            inputRef.current.focus();
        }
    }, [inputRef, isEditing]);

    const onEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
        // TODO Update deprecated keyCode
        if (e.keyCode === 13) {
            // Enter key
            saveStrategy();
        }
    };

    const calculateWidth = () => {
        const width = measureRef?.current?.clientWidth;
        if (width > 110) {
            return width + 30; // 15 px padding on each side
        }
        return 127;
    };

    if (isEditing) {
        return (
            <>
                <div className={styles.measure} ref={measureRef}>
                    {strategy}
                </div>{' '}
                {/* Hidden div used for measuring text length */}
                <input
                    type="text"
                    ref={inputRef}
                    autoFocus // for mobile safari
                    value={strategy}
                    onChange={(e) => {
                        setAnswered(false);
                        setStrategy(e.target.value);
                    }}
                    className={styles.input}
                    onKeyDown={onEnter}
                    onBlur={saveStrategy}
                    maxLength={10000}
                    style={{ width: calculateWidth() }}
                />
            </>
        );
    }
    return (
        <div className={styles.addButton} onClick={() => setIsEditing(true)}>
            Add&nbsp;custom
        </div>
    );
};

type MeansCustomQuestionProps = Pick<QuestionProps, 'answerKey' | 'answered' | 'setAnswered'> & {
    reviewKeys: { answerKey: string; label: string }[];
};

const MeansCustomQuestion = (props: MeansCustomQuestionProps) => {
    const { answerKey, reviewKeys, answered, setAnswered } = props;
    const [store] = useContext(StoreContext);
    const { assessment } = store;
    const { answers } = assessment;

    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<string[]>(answerKey, [], false);

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    return (
        <div className={styles.container}>
            <div className={styles.title}>
                To protect myself now, I can reduce assess to ways to harm myself. I plan to:
            </div>
            {reviewKeys.map((reviewKey) => {
                const answerList: string[] = answers[reviewKey.answerKey] || [];
                if (!answerList.length) return null;
                return (
                    <React.Fragment key={`section-${reviewKey.label}`}>
                        <h6>{reviewKey.label}:</h6>
                        <ul>
                            {answerList.map((answer) => (
                                <li key={`answer-${reviewKey.label}-${answer}`}>{answer}</li>
                            ))}
                        </ul>
                    </React.Fragment>
                );
            })}
            <h6>My Additional Ideas</h6>
            <div className={styles.customStrategies}>
                {updatedAnswer.map((answer) => (
                    <div key={answer} className={styles.customStrategy}>
                        {answer}
                        <span
                            onClick={() => {
                                setAnswered(false);
                                setAnswer(updatedAnswer.filter((value) => value !== answer));
                            }}
                        >
                            ✕
                        </span>
                    </div>
                ))}
                <AddCustomStrategy {...props} updatedAnswer={updatedAnswer} setAnswer={setAnswer} />
            </div>
        </div>
    );
};

export { MeansCustomQuestion };
export default MeansCustomQuestion;
