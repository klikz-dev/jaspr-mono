import { AnswerKeyType } from 'components/ConversationalUi/questions';
import { AssessmentAnswers, Preferences } from 'state/types';
import ProviderComments from '../../ProviderNotes';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';
import styles from './index.module.scss';

interface QuestionTextProps {
    action: {
        answerKey: AnswerKeyType;
    };
    question: { providerLabel?: string };
    actionIndex: number;
    providerComments: ProviderCommentsGetResponse;
    setProviderComments: (providerComments: ProviderCommentsGetResponse) => void;
    assessment: AssessmentAnswers;
    preferences: Preferences;
    currentEncounter: number;
}

const QuestionText = ({
    action,
    actionIndex,
    assessment,
    question,
    providerComments,
    setProviderComments,
    currentEncounter,
    preferences,
}: QuestionTextProps) => {
    return (
        <>
            {actionIndex === 0 && <div className={styles.question}>{question?.providerLabel}</div>}
            <div className={styles.questionText}>
                <div className={styles.answer}>
                    Describe: <span>{assessment[action.answerKey]}</span>
                </div>
                <ProviderComments
                    providerComments={providerComments}
                    answerKey={action.answerKey}
                    setProviderComments={setProviderComments}
                    currentEncounter={currentEncounter}
                    enabled={preferences.providerNotes}
                />
            </div>
        </>
    );
};

export default QuestionText;
