import { AnswerKeyType } from 'components/ConversationalUi/questions';
import { AssessmentAnswers, Preferences } from 'state/types';
import ProviderComments from '../../ProviderNotes';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';
import styles from './index.module.scss';

interface QuestionCounterProps {
    action: {
        answerKey: AnswerKeyType;
        answerKeyCount: AnswerKeyType;
        answerKeyUnit: AnswerKeyType;
        multiple?: boolean;
    };
    providerComments: ProviderCommentsGetResponse;
    setProviderComments: (providerComments: ProviderCommentsGetResponse) => void;
    assessment: AssessmentAnswers;
    question: { providerLabel?: string };
    preferences: Preferences;
    currentEncounter: number;
}

const QuestionCounter = ({
    action,
    assessment,
    question,
    providerComments,
    setProviderComments,
    currentEncounter,
    preferences,
}: QuestionCounterProps) => {
    return (
        <div className={styles.questionCounter}>
            <div className={styles.question}>{question.providerLabel}</div>
            <div className={styles.answer}>
                {assessment[action.answerKeyCount]}{' '}
                {!isNaN(assessment[action.answerKeyCount]) && assessment[action.answerKeyUnit]
                    ? 'times per'
                    : ''}{' '}
                {assessment[action.answerKeyUnit]}
            </div>
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

export default QuestionCounter;
