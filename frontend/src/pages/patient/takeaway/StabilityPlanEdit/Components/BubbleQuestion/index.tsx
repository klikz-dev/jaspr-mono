import { AnswerKeyType, Questions, UIDType } from 'components/ConversationalUi/questions';
import React from 'react';
import { AssessmentAnswers } from 'state/types';
import CustomStrategy from './CustomStrategy';
import styles from './index.module.scss';

interface BubbleQuestionProps {
    title: string;
    answers: Partial<AssessmentAnswers>;
    setAnswers: (answers: Partial<AssessmentAnswers>) => void;
    uid: UIDType;
    answerKey: AnswerKeyType;
    questions: Questions;
    allowCustom?: boolean;
}

const BubbleQuestion = ({
    title,
    answers,
    setAnswers,
    uid,
    answerKey,
    questions,
    allowCustom = false,
}: BubbleQuestionProps) => {
    const question = questions
        .find((question) => question.uid === uid)
        ?.actions.map((action) => {
            if ('groups' in action) {
                return action.groups.flat();
            }
            return action;
        })
        .flat()
        .find((action) => 'answerKey' in action && action.answerKey === answerKey);

    let options: { value: string | boolean; label: string; sublabel?: string }[] = [];
    if (question && 'choices' in question) {
        options = question.choices.map((choice) => ({ value: choice, label: choice }));
    } else if (question && 'options' in question && question) {
        // @ts-ignore Types not appropriately filtered
        options = question.options.map((option) => ({ value: option.value, label: option.label }));
    }

    const questionAnswers: string[] = answers[answerKey] || [];

    const toggleOption = ({ target }: React.ChangeEvent<HTMLInputElement>) => {
        const { checked, value } = target;
        if (checked) {
            setAnswers({ ...answers, [answerKey]: [...(answers[answerKey] || []), value] });
        } else {
            setAnswers({
                ...answers,
                [answerKey]: (answers[answerKey] || []).filter(
                    (answer: string) => answer !== value,
                ),
            });
        }
    };

    const addOption = (options: string[]) => {
        setAnswers({ ...answers, [answerKey]: options });
    };

    return (
        <div className={styles.container}>
            <div className={styles.title}>{title}</div>
            <div className={styles.bubbles}>
                {options.map((option) => (
                    <label
                        className={`${styles.label} ${
                            questionAnswers.includes(option.value.toString()) ? styles.checked : ''
                        }`}
                        key={`${answerKey}-default-${answerKey}${option.value.toString()}`}
                    >
                        {option?.label || option}
                        <input
                            className={styles.checkbox}
                            type="checkbox"
                            onChange={toggleOption}
                            checked={questionAnswers.includes(option.value.toString())}
                            value={option.value.toString()}
                        />
                    </label>
                ))}
                {questionAnswers
                    .filter((answer) => !options.map((option) => option.value).includes(answer))
                    .map((option) => (
                        <label
                            className={`${styles.label} ${styles.checked}`}
                            key={`${answerKey}-custom-${option}`}
                        >
                            {option}
                            <input
                                className={styles.checkbox}
                                type="checkbox"
                                onChange={toggleOption}
                                checked={questionAnswers.includes(option)}
                                value={option}
                            />
                        </label>
                    ))}
                {(allowCustom ||
                    (question && 'allowCustom' in question && question.allowCustom)) && (
                    <CustomStrategy setAnswer={addOption} answer={questionAnswers} />
                )}
            </div>
        </div>
    );
};

export default BubbleQuestion;
