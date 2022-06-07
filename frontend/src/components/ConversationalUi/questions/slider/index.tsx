import { useEffect } from 'react';
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

type SliderQuestionProps = Pick<QuestionProps, 'answerKey' | 'answered' | 'setAnswered'> & {
    min: number;
    max: number;
    minLabel: string;
    maxLabel: string;
    step?: number;
};

const SliderQuestion = (props: SliderQuestionProps) => {
    const { answerKey, min, max, minLabel, maxLabel, step = 1, answered, setAnswered } = props;
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<number | null>(
        answerKey,
        null,
        true,
    );

    const marks = {
        [min]: <div className={styles.mark} />,
        [max]: <div className={styles.mark} />,
    };

    if (updatedAnswer !== null) {
        marks[updatedAnswer] = {
            // @ts-ignore
            style: {
                color: '#3B6975',
                fontSize: '20px',
                fontWeight: 'bold',
                letterSpacing: 1.5,
                top: -51,
            },
            label: updatedAnswer,
        };
    }

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    return (
        <div className={styles.container}>
            <div className={styles.end}>
                <span className={styles.value}>{min}</span>
                <span className={styles.label}>{minLabel}</span>
            </div>
            <Slider
                min={min}
                max={max}
                step={step}
                defaultValue={0}
                value={updatedAnswer || 0}
                trackStyle={{ backgroundColor: 'rgba(0,0,0,.59)', height: 2 }}
                railStyle={{ backgroundColor: 'rgba(0,0,0,.59)', height: 2 }}
                marks={marks}
                handleStyle={{
                    height: 28,
                    width: 6,
                    backgroundColor: '#4E77A2',
                    borderRadius: 7,
                    marginTop: -13,
                    marginLeft: 0,
                    border: 'none',
                }}
                dotStyle={{
                    width: '8px',
                    height: '8px',
                    borderColor: '#979797',
                    backgroundColor: '#4E77A2',
                    top: '-3px',
                }}
                onChange={(value) => {
                    setAnswer(value);
                    setAnswered(false);
                }}
            />
            <div className={styles.end}>
                <span className={styles.value}>{max}</span>
                <span className={styles.label}>{maxLabel}</span>
            </div>
        </div>
    );
};

export { SliderQuestion };
export default SliderQuestion;
