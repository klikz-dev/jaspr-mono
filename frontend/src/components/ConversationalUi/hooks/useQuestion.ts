import { useContext, useEffect, useState } from 'react';
import Segment, { AnalyticNames } from 'lib/segment';
import StoreContext from 'state/context/store';
import { AnswerContext } from '../context';

/** The useEffect hook manages an assessment answer
 * @param answerKey The string used as a key for the specified answer
 * @param defaultAnswer The object the answer will be initialized to if no answer is currently set
 * @param analytics Set to true to send the answer to segment in addition to the API
 * @return [Answer, Answer, (answer: Answer) => void, (answer?: Answer) => void]
 */
export const useQuestion = <Answer>(
    answerKey: string,
    defaultAnswer: Answer,
    analytics?: boolean,
): [Answer, Answer, (answer: Answer) => void, (answer?: Answer) => void] => {
    const [store] = useContext(StoreContext);
    const { updateAnswers } = useContext(AnswerContext);
    const { assessment } = store;
    const { answers } = assessment;
    const answer: Answer = answers[answerKey];
    const [updatedAnswer, setUpdatedAnswer] = useState<Answer>(answer || defaultAnswer);
    const [isDirty, setIsDirty] = useState(false);

    useEffect(() => {
        if (answer !== null && answer !== undefined) {
            setIsDirty(false);
            setUpdatedAnswer(answer);
        }
    }, [answer]);

    const setAnswer = (value: Answer): void => {
        setIsDirty(true);
        setUpdatedAnswer(value);
    };

    const sendToSegment = (newAnswer: Answer): void => {
        Segment.track(AnalyticNames.ASSESSMENT_QUESTION_ANSWERED, {
            answerKey,
            answer: analytics ? newAnswer : 'answered',
        });
    };

    const processAnswer = (): Answer => {
        if (answerKey === 'supportivePeople' && Array.isArray(updatedAnswer)) {
            // @ts-ignore // TODO Figure out how to fix type issue
            return updatedAnswer.filter((person) => person.name || person.phone);
        }
        if (Array.isArray(updatedAnswer)) {
            // @ts-ignore // TODO Figure out how to fix type issue
            return updatedAnswer.filter((a) => a !== null && a !== '' && a !== undefined);
        }
        return updatedAnswer;
    };

    const saveAnswer = (newAnswer?: Answer): void => {
        if (newAnswer !== undefined) {
            setUpdatedAnswer(newAnswer);
            updateAnswers((answers) => ({ ...answers, ...{ [answerKey]: newAnswer } }));
            setIsDirty(false);
            sendToSegment(newAnswer);
        } else if (isDirty) {
            setIsDirty(false);
            const answerCopy = processAnswer();
            setUpdatedAnswer(answerCopy);
            updateAnswers((answers) => ({ ...answers, ...{ [answerKey]: answerCopy } }));
            sendToSegment(answerCopy);
        }
    };

    return [answer, updatedAnswer, setAnswer, saveAnswer];
};

export default useQuestion;
