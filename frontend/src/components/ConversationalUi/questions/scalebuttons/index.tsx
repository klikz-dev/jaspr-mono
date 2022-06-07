import { useEffect } from 'react';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

type ScaleButtonsType = Pick<QuestionProps, 'setAnswered' | 'answerKey' | 'answered'> & {
    min: number;
    minLabel: string;
    max: number;
    maxLabel: string;
};

const ScaleButtons = (props: ScaleButtonsType): JSX.Element => {
    const { min, minLabel, max, maxLabel, setAnswered, answerKey, answered } = props;

    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<number | ''>(answerKey, '', true);

    const range = (start: number, end: number) => {
        return new Array(end - start + 1).fill(undefined).map((_, i) => i + start);
    };

    const onChange = (value: number): void => {
        if (value !== updatedAnswer) {
            setAnswered(false);
            setAnswer(value);
        }
    };

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    return (
        <div className={styles.container}>
            <div className={styles.scale}>
                <div className={styles.row}>
                    {range(min, max).map((value) => (
                        <div
                            key={value}
                            className={`${styles.box} ${
                                value === updatedAnswer ? styles.selected : {}
                            } ${max > 5 ? styles.small : styles.large}`}
                            onClick={() => onChange(value)}
                        >
                            {value}
                        </div>
                    ))}
                </div>
                <div className={styles.row}>
                    <span>{minLabel}</span>
                    <span>{maxLabel}</span>
                </div>
            </div>
        </div>
    );
};

export { ScaleButtons };
export default ScaleButtons;
