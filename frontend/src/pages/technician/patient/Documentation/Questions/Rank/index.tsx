import { AnswerKeyType } from 'components/ConversationalUi/questions';
import { AssessmentAnswers, Preferences } from 'state/types';
import ProviderComments from '../../ProviderNotes';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';
import styles from './index.module.scss';

interface QuestionRankProps {
    action: {
        answerKey: AnswerKeyType;
        options: {
            question: string;
            answerKey: AnswerKeyType;
            title?: string;
            subtitle?: string;
        }[];
    };
    providerComments: ProviderCommentsGetResponse;
    setProviderComments: (providerComments: ProviderCommentsGetResponse) => void;
    assessment: AssessmentAnswers;
    preferences: Preferences;
    currentEncounter: number;
}

const QuestionRank = ({
    action,
    assessment,
    providerComments,
    setProviderComments,
    currentEncounter,
    preferences,
}: QuestionRankProps) => {
    const count = action.options.length;
    const order: number[] = (assessment[action.answerKey] || '1,2,3,4,5')
        .split(',')
        .map((str: string) => parseInt(str, 10) - 1);
    const options = action.options;

    return (
        <div className={styles.questionRank}>
            <div className={styles.header}>
                <div className={styles.rankHeader}>Rank</div>
                <div className={styles.itemHeader}>Item</div>
                <div className={styles.responseHeader}>Response</div>
                <div className={styles.ratingHeader}>
                    Rating
                    <br />
                    (1-{count})
                </div>
            </div>

            {order.map((index: number, rank: number) => {
                const [rateAnswerKey, describeAnswerKey] = options?.[index]?.answerKey.split('|');

                return (
                    <div className={styles.row} key={rank}>
                        <div className={styles.rank}>{rank + 1}</div>
                        <div className={styles.item}>{options[index]?.question}</div>
                        <div className={styles.response}>
                            {assessment[describeAnswerKey] || '[-]'}
                        </div>
                        <div className={styles.rating}>{assessment[rateAnswerKey] || '[-]'}</div>
                        <ProviderComments
                            providerComments={providerComments}
                            answerKey={describeAnswerKey}
                            setProviderComments={setProviderComments}
                            currentEncounter={currentEncounter}
                            enabled={preferences.providerNotes}
                            indent
                        />
                    </div>
                );
            })}
        </div>
    );
};

export default QuestionRank;
