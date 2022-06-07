import ProviderComments from '../../ProviderNotes';
import { AssessmentAnswers, Preferences } from 'state/types';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';

import styles from './index.module.scss';
import { AnswerKeyType } from 'components/ConversationalUi/questions';

interface QuestionScaleButtonsProps {
    action: {
        answerKey: AnswerKeyType;
    };
    question: { providerLabel?: string };
    providerComments: ProviderCommentsGetResponse;
    setProviderComments: (providerComments: ProviderCommentsGetResponse) => void;
    assessment: AssessmentAnswers;
    preferences: Preferences;
    currentEncounter: number;
}

const QuestionScaleButtons = ({
    action,
    assessment,
    question,
    providerComments,
    setProviderComments,
    currentEncounter,
    preferences,
}: QuestionScaleButtonsProps) => {
    return (
        <div className={styles.questionScaleButtons}>
            <div className={styles.question}>{question.providerLabel}</div>
            <div className={styles.answer}>{assessment[action.answerKey]}</div>
            <ProviderComments
                providerComments={providerComments}
                answerKey={action.answerKey}
                setProviderComments={setProviderComments}
                currentEncounter={currentEncounter}
                enabled={preferences.providerNotes}
            />
        </div>
    );
};

export default QuestionScaleButtons;
