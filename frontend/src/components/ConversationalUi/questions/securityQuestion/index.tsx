import { useContext, useEffect, useState } from 'react';
import StoreContext from 'state/context/store';
import { saveSecurityQuestion } from 'state/actions/user';
import Dropdown from 'components/Select';
import { QuestionProps } from '../../question';
import styles from './index.module.scss';
import { Patient } from 'state/types';

type SetSecurityQuestionProps = Pick<
    QuestionProps,
    | 'currentQuestion'
    | 'answered'
    | 'validate'
    | 'isValid'
    | 'showValidation'
    | 'setShowValidation'
    | 'setIsValid'
>;

const SetSecurityQuestion = (props: SetSecurityQuestionProps) => {
    const {
        currentQuestion,
        answered,
        validate,
        isValid,
        showValidation,
        setShowValidation,
        setIsValid,
    } = props;
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { securityQuestion: currentSecurityQuestion } = user as Patient;

    const [securityQuestion, setSecurityQuestion] = useState<{
        value: string;
        label: string;
    }>({ label: '', value: '' });
    const [securityAnswer, setSecurityAnswer] = useState('');

    useEffect(() => {
        validate.current = () =>
            new Promise((resolve, reject) => {
                const valid = Boolean(securityQuestion.value) && Boolean(securityAnswer);
                setIsValid(valid);
                setShowValidation(!valid);
                if (valid) {
                    setShowValidation(!valid);
                    resolve(valid);
                } else {
                    reject();
                }
            });
    }, [securityAnswer, securityQuestion.value, setIsValid, setShowValidation, validate]);

    useEffect(() => {
        const save = () => {
            saveSecurityQuestion(
                dispatch,
                currentSecurityQuestion?.id ? currentSecurityQuestion.id : null,
                securityQuestion.value,
                securityAnswer,
            );
        };
        if (answered && securityQuestion.value && securityAnswer) {
            save();
        }
    }, [answered, currentSecurityQuestion, securityQuestion, securityAnswer, dispatch]);

    return (
        <>
            {!currentQuestion && (
                <div className={styles.completeMessage}>Security question complete</div>
            )}
            {currentQuestion && (
                <div className={styles.container}>
                    <Dropdown
                        placeholder="Select a question"
                        onChange={(value: { label: string; value: string }) => {
                            setSecurityQuestion(value);
                            setShowValidation(false);
                        }}
                        mode="light"
                        value={securityQuestion}
                        options={[
                            {
                                label: 'In what city were you born?',
                                value: 'In what city were you born?',
                            },
                            {
                                label: 'What was the name of your first elementary school?',
                                value: 'What was the name of your first elementary school?',
                            },
                            {
                                label: 'What is the first name of the first person you ever dated?',
                                value: 'What is the first name of the first person you ever dated?',
                            },
                            {
                                label: "What is your mother's maiden name?",
                                value: "What is your mother's maiden name?",
                            },
                            {
                                label: 'What is the name of your favorite pet?',
                                value: 'What is the name of your favorite pet?',
                            },
                        ]}
                    />

                    <input
                        className={styles.answer}
                        type="text"
                        placeholder="Type your answer here"
                        maxLength={255}
                        value={securityAnswer}
                        onChange={(e) => {
                            const { value } = e.target;
                            setSecurityAnswer(value);
                            setShowValidation(false);
                        }}
                    />

                    {!isValid && showValidation && (
                        <div className={styles.instruction}>
                            Please select a security question and provide an answer.
                        </div>
                    )}
                </div>
            )}
        </>
    );
};

export { SetSecurityQuestion };
export default SetSecurityQuestion;
