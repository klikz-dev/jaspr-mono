import React, { useEffect } from 'react';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

type PersonProps = Pick<QuestionProps, 'setAnswered'> & {
    personIndex: number;
    name: string;
    phone: string;
    setAnswer: (answer: { phone: string; name: string }[]) => void;
    updatedAnswer: { phone: string; name: string }[];
};

const Person = (props: PersonProps) => {
    const { personIndex, name, phone, setAnswered, setAnswer, updatedAnswer } = props;

    const setName = (name: string): void => {
        const updatedAnswers = [...updatedAnswer];
        updatedAnswers[personIndex].name = name;
        setAnswer(updatedAnswers);
        setAnswered(false);
    };

    const setPhone = (phone: string): void => {
        const updatedAnswers = [...updatedAnswer];
        updatedAnswers[personIndex].phone = phone;
        setAnswer(updatedAnswers);
        setAnswered(false);
    };

    const remove = (): void => {
        const updatedAnswers = [...updatedAnswer];
        updatedAnswers.splice(personIndex, 1);
        setAnswer(updatedAnswers);
        setAnswered(false);
    };

    return (
        <div className={styles.row}>
            <div className={styles.person}>
                <input
                    value={name}
                    placeholder="Type name here"
                    onChange={(e) => setName(e.target.value)}
                    maxLength={45}
                />
                <input
                    value={phone}
                    placeholder="Type number here"
                    onChange={(e) => setPhone(e.target.value)}
                    maxLength={21}
                />
            </div>
            <div className={styles.close} onClick={remove}>
                &times;
            </div>
        </div>
    );
};

type SupportivePeopleQuestionProps = Pick<QuestionProps, 'answered' | 'answerKey' | 'setAnswered'>;

const SupportivePeopleQuestion = (props: SupportivePeopleQuestionProps) => {
    const { answered, answerKey, setAnswered } = props;
    const defaultValue = [{ phone: '', name: '' }];
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<{ phone: string; name: string }[]>(
        answerKey,
        defaultValue,
        false,
    );

    const addPerson = () => {
        setAnswer([...updatedAnswer, { phone: '', name: '' }]);
        setAnswered(false);
    };

    useEffect(() => {
        if (answered) {
            // TODO Can't save if phone and name are empty.  Will need to filter out
            saveAnswer();
        }
    }, [answered, saveAnswer, updatedAnswer]);

    return (
        <div className={styles.container}>
            <div className={`${styles.row} ${styles.header}`}>
                <span>Name</span>
                <span>Phone Number</span>
            </div>
            {updatedAnswer.map((person, personIndex) => (
                <Person
                    key={`person-${personIndex}`}
                    {...props}
                    {...person}
                    personIndex={personIndex}
                    updatedAnswer={updatedAnswer}
                    setAnswer={setAnswer}
                />
            ))}

            <div className={styles.addButton} onClick={addPerson}>
                Add another
            </div>
        </div>
    );
};

export { SupportivePeopleQuestion };
export default SupportivePeopleQuestion;
