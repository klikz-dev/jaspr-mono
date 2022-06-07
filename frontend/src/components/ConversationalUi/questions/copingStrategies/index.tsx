import React, { useEffect, useRef, useState } from 'react';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';
import { CopingStrategyType } from '../../questions';

// TODO Deduplicate this with meansCustom
type AddCustomStrategyProps = Pick<QuestionProps, 'setAnswered'> & {
    setAnswer: (answer: string[]) => void;
    updatedAnswer: string[];
};

const AddCustomStrategy = (props: AddCustomStrategyProps) => {
    const { setAnswered, updatedAnswer, setAnswer } = props;
    const [isEditing, setIsEditing] = useState(false);
    const [strategy, setStrategy] = useState('');
    const inputRef = useRef<HTMLInputElement>(null);
    const measureRef = useRef<HTMLDivElement>(null);
    const saveStrategy = () => {
        if (strategy !== '' && !updatedAnswer.includes(strategy)) {
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
            setAnswered(false);
        }
    };

    const calculateWidth = () => {
        const width = measureRef?.current?.clientWidth;
        if (width && width > 110) {
            return width + 30; // 15 px padding on each side
        }
        return 127; // Minimum width
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
        <div className={styles.addCustomButton} onClick={() => setIsEditing(true)}>
            &#xff0b;
        </div>
    );
};

type CopingStrategiesQuestionProps = Pick<
    QuestionProps,
    | 'answerKey'
    | 'setAnswered'
    | 'answered'
    | 'questions'
    | 'setIsValid'
    | 'showValidation'
    | 'showValidation'
    | 'isValid'
    | 'setShowValidation'
    | 'currentAnswers'
    | 'validate'
> & {
    choices: string[];
};

const CopingStrategiesQuestion = (props: CopingStrategiesQuestionProps): JSX.Element => {
    const {
        answerKey,
        setAnswered,
        answered,
        choices,
        questions,
        setIsValid,
        showValidation,
        isValid,
        setShowValidation,
        currentAnswers,
        validate,
    } = props;
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<string[]>(answerKey, [], false);

    const togglePreset = (value: string) => {
        if (updatedAnswer.includes(value)) {
            setAnswer(updatedAnswer.filter((answer) => answer !== value));
        } else {
            setAnswer([...updatedAnswer, value]);
        }
        setAnswered(false);
    };

    const removeCustom = (value: string) => {
        setAnswer(updatedAnswer.filter((answer) => answer !== value));
        setAnswered(false);
    };

    useEffect(() => {
        const copingAnswerKeys = questions
            .filter((question) =>
                question?.actions?.some(
                    (action: CopingStrategyType): action is CopingStrategyType =>
                        action.answerKey !== answerKey && action.type === 'coping-strategy',
                ),
            )
            .map((question) =>
                question.actions.filter((action) => action.type === 'coping-strategy'),
            )
            .flat()
            .map((action: CopingStrategyType) => action.answerKey);

        const allCopingAnswers = copingAnswerKeys
            .map((answerKey) => currentAnswers[answerKey])
            .flat()
            .filter((answer) => answer);

        validate.current = () =>
            new Promise((resolve, reject) => {
                const valid = !updatedAnswer.some((answer) => allCopingAnswers.includes(answer));
                setIsValid(valid);
                setShowValidation(
                    !valid
                        ? "You've already used one of your choices on a previous answer.  You may only submit a coping strategy once"
                        : false,
                );
                if (valid) {
                    setShowValidation(!valid);
                    resolve(valid);
                } else {
                    reject();
                }
            });
    }, [
        questions,
        setIsValid,
        setShowValidation,
        validate,
        currentAnswers,
        answerKey,
        updatedAnswer,
    ]);

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    return (
        <div className={styles.container}>
            {choices.map((choice) => {
                const selected = updatedAnswer.includes(choice);
                return (
                    <div
                        key={choice}
                        className={`${styles.choice} ${selected ? styles.selected : ''}`}
                        onClick={() => togglePreset(choice)}
                    >
                        {choice}
                    </div>
                );
            })}
            {updatedAnswer
                .filter((answer) => !choices.includes(answer))
                .map((choice) => (
                    <div
                        key={choice}
                        className={`${styles.choice} ${styles.selected} ${styles.custom}`}
                    >
                        {choice}
                        <span onClick={() => removeCustom(choice)}>✕</span>
                    </div>
                ))}
            <AddCustomStrategy {...props} updatedAnswer={updatedAnswer} setAnswer={setAnswer} />
            {!isValid && showValidation && (
                <div className={styles.instruction}>{showValidation}</div>
            )}
        </div>
    );
};

export { CopingStrategiesQuestion };
export default CopingStrategiesQuestion;
