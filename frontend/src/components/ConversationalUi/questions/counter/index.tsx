import { useEffect } from 'react';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './counter.module.scss';
import { QuestionProps } from '../../question';
import { AnswerKeyType } from '../../questions';

const retrieveNumberInputValue = (value: string | number | null) => {
    if (value === null) return '';
    // @ts-ignore // TODO Review inputs
    const progressInt = parseInt(value, 10);
    if (!Number.isNaN(progressInt)) return progressInt;
    return '';
};

type CounterQuestionProps = Pick<QuestionProps, 'answered' | 'setAnswered'> & {
    answerKeyCount: AnswerKeyType;
    answerKeyUnit: string;
    options: { value: string; label: string }[];
};

const CounterQuestion = (props: CounterQuestionProps) => {
    const { answerKeyCount, answerKeyUnit, options, answered, setAnswered } = props;
    const [, updatedAnswerKeyUnit, setAnswerKeyUnit, saveAnswerKeyUnit] = useQuestion<string>(
        answerKeyUnit,
        '',
        false,
    );
    const [, updatedAnswerKeyCount, setAnswerKeyCount, saveAnswerKeyCount] = useQuestion<number>(
        answerKeyCount,
        null,
        false,
    );

    const times = retrieveNumberInputValue(updatedAnswerKeyCount);

    useEffect(() => {
        if (answered) {
            saveAnswerKeyUnit();
            saveAnswerKeyCount();
        }
    }, [answered, saveAnswerKeyUnit, saveAnswerKeyCount]);

    return (
        <>
            <div className={styles.counter}>
                <div className={styles.timesSection}>
                    <input
                        type="number"
                        pattern="[0-9]*"
                        placeholder="ENTER #"
                        onChange={(e) => {
                            const intValue = parseInt(e.target.value, 10);
                            const updateValue = Number.isNaN(intValue) ? null : intValue;
                            setAnswerKeyCount(updateValue);
                            setAnswered(false);
                        }}
                        value={times}
                    />
                    <span className={styles.times}>time{times === 1 ? '' : 's'} per</span>
                </div>
                <div className={styles.options}>
                    {options.map((option, idx) => (
                        <label key={option.value} className={styles.option}>
                            <input
                                type="radio"
                                name={`counter-choice-${idx}`}
                                checked={updatedAnswerKeyUnit === option.value}
                                onChange={(e) => {
                                    setAnswered(false);
                                    setAnswerKeyUnit(e.target.value);
                                }}
                                value={option.value}
                            />
                            <span className={styles.label}>{option.label}</span>
                        </label>
                    ))}
                </div>
            </div>
        </>
    );
};

export { CounterQuestion };
export default CounterQuestion;
