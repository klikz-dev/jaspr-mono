import Section from '../../Components/Section';
import BubbleQuestion from '../../Components/BubbleQuestion';
import TopRankQuestion from '../../Components/TopRank';
import styles from './index.module.scss';
import { AssessmentAnswers } from 'state/types';
import { Questions } from 'components/ConversationalUi/questions';

interface CopingSkillsTabProps {
    answers: Partial<AssessmentAnswers>;
    questions: Questions;
    setAnswers: (
        answers:
            | Partial<AssessmentAnswers>
            | ((answers: Partial<AssessmentAnswers>) => Partial<AssessmentAnswers>),
    ) => void;
    error: string;
}

const CopingSkillsTab = ({ answers, questions, setAnswers, error }: CopingSkillsTabProps) => {
    return (
        <Section
            number="5"
            title="Coping Strategies"
            tooltip="Select a mix of strategies to help cope with intense painful emotions and situation."
        >
            <div className={styles.questions}>
                <div className={styles.error}>{error}</div>

                <BubbleQuestion
                    title="Calm your body chemistry:"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="copingBody"
                    answerKey="copingBody"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Distract:"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="copingDistract"
                    answerKey="copingDistract"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Help someone:"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="copingHelpOthers"
                    answerKey="copingHelpOthers"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Courage:"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="copingCourage"
                    answerKey="copingCourage"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Comfort through 5 senses:"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="copingSenses"
                    answerKey="copingSenses"
                    questions={questions}
                />

                <TopRankQuestion
                    answerKey="copingTop"
                    answers={answers}
                    lists={[
                        'copingBody',
                        'copingDistract',
                        'copingHelpOthers',
                        'copingCourage',
                        'copingSenses',
                        'supportivePeople',
                    ]}
                    dropTitle="COPING STRATEGIES"
                    targetCount={7}
                    setAnswers={setAnswers}
                />
            </div>
        </Section>
    );
};

export default CopingSkillsTab;
