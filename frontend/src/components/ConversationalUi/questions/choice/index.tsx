import { useEffect } from 'react';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './choice.module.scss';
import { QuestionProps } from '../../question';

const checkBoolean = (value: any): any => {
    if (value === 'true') {
        return true;
    } else if (value === 'false') {
        return false;
    }
    return value;
};

type ChoiceQuestionProps = Pick<QuestionProps, 'uid' | 'answerKey' | 'answered' | 'setAnswered'> & {
    question?: string;
    subtitle?: string;
    multiple?: boolean;
    vertical?: boolean;
    options: { label: string; value: boolean | string }[];
};

// TODO Conditional type for multiple boolean, either array or string answer
const ChoiceQuestion = (props: ChoiceQuestionProps) => {
    const {
        uid,
        question,
        subtitle,
        options,
        answerKey,
        answered,
        setAnswered,
        multiple = false,
        vertical = false,
    } = props;
    const defaultValue: string[] | null = multiple ? [] : null;
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<boolean | string | string[]>(
        answerKey,
        defaultValue,
        true,
    );

    const checkMultiple = (value: string) => {
        if (Array.isArray(updatedAnswer)) {
            if (updatedAnswer.includes(value)) {
                return updatedAnswer.filter((current) => current !== value); // Remove from list
            } else {
                return [...updatedAnswer, value];
            }
        }
    };

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    return (
        <>
            <div className={styles.titles}>
                <div className={styles.instruction}>{question}</div>
                {Boolean(subtitle) && <div className={styles.subtitle}>{subtitle}</div>}
            </div>
            <div className={`${styles.options} ${vertical ? styles.vertical : ''}`}>
                {options.map((option) => (
                    <label key={option.value.toString()} className={styles.option}>
                        <input
                            type={multiple ? 'checkbox' : 'radio'}
                            name={`choice-${uid}-${options.map((option) => option.value).join('')}`}
                            checked={
                                multiple && Array.isArray(updatedAnswer)
                                    ? updatedAnswer.includes(option.value.toString())
                                    : updatedAnswer === option.value
                            }
                            onChange={(e) => {
                                setAnswered(false);
                                setAnswer(
                                    multiple
                                        ? checkMultiple(e.target.value)
                                        : checkBoolean(e.target.value),
                                );
                            }}
                            value={option.value.toString()}
                        />
                        <span className={styles.label}>{option.label}</span>
                    </label>
                ))}
            </div>
        </>
    );
};

export { ChoiceQuestion };
export default ChoiceQuestion;
