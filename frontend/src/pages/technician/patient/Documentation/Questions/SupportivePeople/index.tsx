import ProviderComments from '../../ProviderNotes';
import { AssessmentAnswers, Preferences } from 'state/types';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';

import styles from './index.module.scss';
import { AnswerKeyType } from 'components/ConversationalUi/questions';

interface QuestionSupportivePeopleProps {
    action: {
        answerKey: AnswerKeyType;
    };
    providerComments: ProviderCommentsGetResponse;
    setProviderComments: (providerComments: ProviderCommentsGetResponse) => void;
    assessment: AssessmentAnswers;
    preferences: Preferences;
    currentEncounter: number;
}

const QuestionSupportivePeople = ({
    action,
    assessment,
    providerComments,
    setProviderComments,
    currentEncounter,
    preferences,
}: QuestionSupportivePeopleProps) => {
    return (
        <div className={styles.questionSupportivePeople}>
            <div className={styles.question}>Supportive People</div>
            <div className={styles.contacts}>
                {(assessment[action.answerKey] || []).map(
                    (supportivePerson: { name: string; phone: string }) => (
                        <div
                            className={styles.contact}
                            key={`${supportivePerson.name}-${supportivePerson.phone}`}
                        >
                            {supportivePerson.name}: {supportivePerson.phone}
                        </div>
                    ),
                )}
                <div className={styles.contact}>24/7 National Hotline: Call 1-800-273-8255</div>
                <div className={styles.contact}>24/7 National Text Line: Text 741741</div>
            </div>
            <ProviderComments
                providerComments={providerComments}
                answerKey={action.answerKey}
                indent
                setProviderComments={setProviderComments}
                currentEncounter={currentEncounter}
                enabled={preferences.providerNotes}
            />
        </div>
    );
};

export default QuestionSupportivePeople;
