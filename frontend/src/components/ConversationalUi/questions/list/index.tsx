import { useEffect } from 'react';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './list.module.scss';
import { QuestionProps } from '../../question';

interface ListItemProps {
    setAnswered: (answered: boolean) => void;
    index: number;
    placeholder: string;
    maxLength: number;
    updatedAnswer: string[];
    setAnswer: (answer: string[]) => void;
}

const ListItem = (props: ListItemProps) => {
    const { setAnswered, setAnswer, updatedAnswer, maxLength, placeholder, index } = props;

    const onChange = (value: string): void => {
        if (value !== updatedAnswer[index]) {
            const newList = [...updatedAnswer];
            newList[index] = value;
            setAnswered(false);
            setAnswer(newList);
        }
    };

    return (
        <input
            type="text"
            value={updatedAnswer[index] || ''}
            placeholder={placeholder}
            maxLength={maxLength}
            onChange={(e) => onChange(e.target.value)}
        />
    );
};

type ListQuestionProps = Pick<QuestionProps, 'setAnswered' | 'answerKey' | 'answered'> & {
    rows: number;
    maxLength: number;
    question: string;
};

const ListQuestion = (props: ListQuestionProps) => {
    const { answerKey, answered, rows, question, maxLength, setAnswered } = props;
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<string[]>(
        answerKey,
        Array(rows || 0).fill(''),
        false,
    );

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    return (
        <>
            <div className={styles.instruction}>{question}</div>
            <div className={styles.options}>
                {[...Array(rows)].map((e, i) => (
                    <ListItem
                        key={i}
                        index={i}
                        placeholder={i === 0 ? 'Click here to begin typing' : ''}
                        maxLength={maxLength}
                        setAnswered={setAnswered}
                        updatedAnswer={updatedAnswer}
                        setAnswer={setAnswer}
                    />
                ))}
            </div>
        </>
    );
};

export { ListQuestion };
export default ListQuestion;
