import { AnswerKeyType } from 'components/ConversationalUi/questions';
import { AssessmentAnswers } from 'state/types';
import styles from './index.module.scss';

interface QuestionListProps {
    action: {
        question: string;
        answerKey: AnswerKeyType;
    };
    assessment: AssessmentAnswers;
}

const QuestionList = ({ action, assessment }: QuestionListProps) => {
    return (
        <div className={styles.questionContainer}>
            <div className={styles.questionList}>
                <div className={styles.row}>
                    <div className={styles.rankHeader}>Rank</div>
                    <div className={styles.question} style={{ textAlign: 'center' }}>
                        {action.question}
                    </div>
                </div>
                {assessment[action.answerKey]?.map((item: string, idx: number) => (
                    <div className={styles.row} key={`${idx}-${item}`}>
                        <div className={styles.rank}>{idx + 1}</div>
                        <div className={styles.answer}>{item}</div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default QuestionList;
