import { AnswerKeyType } from 'components/ConversationalUi/questions';
import { AssessmentAnswers } from 'state/types';
import styles from './index.module.scss';

interface QuestionButtonsProps {
    action: {
        answerKey: AnswerKeyType;
    };
    assessment: AssessmentAnswers;
    question: { providerLabel?: string };
}

const QuestionButtons = ({ action, assessment, question }: QuestionButtonsProps) => {
    const checkBoolean = (value: any): any => {
        if (value === true) {
            return 'YES';
        }
        if (value === false) {
            return 'NO';
        }
        return value;
    };
    return (
        <div className={styles.questionButtons}>
            <div className={styles.question}>{question?.providerLabel}</div>
            <div className={styles.answer}>{checkBoolean(assessment[action.answerKey])}</div>
        </div>
    );
};

export default QuestionButtons;
