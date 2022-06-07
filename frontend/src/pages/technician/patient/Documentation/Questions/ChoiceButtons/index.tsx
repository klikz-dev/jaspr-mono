import { AnswerKeyType } from 'components/ConversationalUi/questions';
import { AssessmentAnswers } from 'state/types';
import styles from './index.module.scss';

interface QuestionChoiceProps {
    action: {
        answerKey: AnswerKeyType;
        multiple?: boolean;
    };
    assessment: AssessmentAnswers;
    question: { providerLabel?: string };
}

const QuestionChoice = ({ action, assessment, question }: QuestionChoiceProps) => {
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
        <div className={styles.questionChoice}>
            <div className={styles.question}>{question.providerLabel}</div>
            <div className={styles.answer}>
                {!action.multiple && checkBoolean(assessment[action.answerKey])}
                {action.multiple && assessment[action.answerKey]?.join(', ')}
            </div>
        </div>
    );
};

export default QuestionChoice;
