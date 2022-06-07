import ProviderComments from '../../ProviderNotes';
import { AssessmentAnswers, Preferences } from 'state/types';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';

import styles from './index.module.scss';
import { AnswerKeyType } from 'components/ConversationalUi/questions';

interface QuestionRankTopProps {
    action: {
        answerKey: AnswerKeyType;
        lists: AnswerKeyType[];
        labels?: string[];
    };
    question: { providerLabel?: string };
    providerComments: ProviderCommentsGetResponse;
    setProviderComments: (providerComments: ProviderCommentsGetResponse) => void;
    assessment: AssessmentAnswers;
    preferences: Preferences;
    currentEncounter: number;
}

const QuestionRankTop = ({
    action,
    assessment,
    question,
    providerComments,
    setProviderComments,
    currentEncounter,
    preferences,
}: QuestionRankTopProps) => {
    return (
        <div className={styles.questionRankTop}>
            <div className={styles.question}>{question?.providerLabel}</div>
            <div className={styles.lists}>
                {action?.lists.map((list, listIdx) => {
                    if (action?.labels?.[listIdx] === '*hide*') {
                        return null;
                    }
                    return (
                        <div key={list} className={styles.list}>
                            <div className={styles.listHeader}>
                                <strong>{action?.labels?.[listIdx] || list}</strong>
                                {(assessment[list] || []).map(
                                    (answer: string | { name: string; phone: string }) => {
                                        if (typeof answer !== 'string' && 'name' in answer) {
                                            return (
                                                <div key={`${answer.name} ${answer.phone}`}>
                                                    {answer.name}: {answer.phone}
                                                </div>
                                            );
                                        }
                                        return <div key={answer}>{answer}</div>;
                                    },
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>

            <ProviderComments
                providerComments={providerComments}
                answerKey={action.answerKey}
                setProviderComments={setProviderComments}
                currentEncounter={currentEncounter}
                enabled={preferences.providerNotes}
                indent
            />
        </div>
    );
};

export default QuestionRankTop;
