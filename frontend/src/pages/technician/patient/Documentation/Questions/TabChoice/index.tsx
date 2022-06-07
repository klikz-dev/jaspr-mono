import { AnswerKeyType } from 'components/ConversationalUi/questions';
import { AssessmentAnswers, Preferences } from 'state/types';
import ProviderComments from '../../ProviderNotes';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';
import styles from './index.module.scss';

interface QuestionTabChoiceProps {
    action: {
        groups: {
            label: string;
            options: {
                label: string;
                value: string;
            }[];
            answerKey: AnswerKeyType;
        }[];
    };
    assessment: AssessmentAnswers;
    question: { providerLabel?: string };
    providerComments: ProviderCommentsGetResponse;
    setProviderComments: (providerComments: ProviderCommentsGetResponse) => void;
    preferences: Preferences;
    currentEncounter: number;
}

const QuestionTabChoice = ({
    action,
    assessment,
    question,
    providerComments,
    setProviderComments,
    currentEncounter,
    preferences,
}: QuestionTabChoiceProps) => {
    return (
        <div className={styles.questionTabChoice}>
            <div className={styles.question}>{question.providerLabel}</div>
            {action?.groups.some((group) => group.answerKey === 'strategiesFirearm') && (
                <div>{assessment['strategiesGeneral']?.join(', ')}</div>
            )}
            <div className={styles.lists}>
                {action?.groups.map((group) => (
                    <div key={group.label} className={styles.list}>
                        <div className={styles.listHeader}>
                            <strong>{group.label}</strong>
                            {(assessment[group.answerKey] || []).map((answer: string) => (
                                <div key={answer}>{answer}</div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            <ProviderComments
                providerComments={providerComments}
                // @ts-ignore // TODO This isn't right
                answerKey={action.answerKey}
                indent
                setProviderComments={setProviderComments}
                currentEncounter={currentEncounter}
                enabled={preferences.providerNotes}
            />
        </div>
    );
};

export default QuestionTabChoice;
