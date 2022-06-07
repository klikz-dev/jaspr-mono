import ProviderComments from '../../ProviderNotes';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';
import { AssessmentAnswers, Preferences } from 'state/types';

import styles from './index.module.scss';
import { AnswerKeyType } from 'components/ConversationalUi/questions';

interface QuestionSliderProps {
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

const QuestionSlider = ({
    action,
    assessment,
    question,
    providerComments,
    setProviderComments,
    currentEncounter,
    preferences,
}: QuestionSliderProps) => {
    return (
        <div className={styles.questionSlider}>
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

export default QuestionSlider;
