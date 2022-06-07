import Section from '../../Components/Section';
import BubbleQuestion from '../../Components/BubbleQuestion';
import TopRankQuestion from '../../Components/TopRank';
import styles from './index.module.scss';
import { AssessmentAnswers } from 'state/types';
import { Questions } from 'components/ConversationalUi/questions';
interface WarningSignsTabProps {
    answers: Partial<AssessmentAnswers>;
    questions: Questions;
    setAnswers: (
        answers:
            | Partial<AssessmentAnswers>
            | ((answers: Partial<AssessmentAnswers>) => Partial<AssessmentAnswers>),
    ) => void;
    error: string;
}

const WarningSignsTab = ({ answers, questions, setAnswers, error }: WarningSignsTabProps) => {
    return (
        <Section
            number="4"
            title="Recognize Warning Signs"
            tooltip="What cues signal that you are in danger of a suicide emergency? Or that it’s time to put your plan in action?"
        >
            <div className={styles.questions}>
                <div className={styles.error}>{error}</div>
                <BubbleQuestion
                    title="Stressors &amp; Situations"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="warningStressors"
                    answerKey="wsStressors"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Internal Signals"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="warningThoughts"
                    answerKey="wsThoughts"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Sensations or Emotions"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="warningFeelings"
                    answerKey="wsFeelings"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Actions"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="warningActions"
                    answerKey="wsActions"
                    questions={questions}
                />

                <TopRankQuestion
                    answerKey="wsTop"
                    answers={answers}
                    lists={['wsStressors', 'wsThoughts', 'wsFeelings', 'wsActions']}
                    dropTitle="TOP WARNING SIGNS"
                    targetCount={3}
                    setAnswers={setAnswers}
                />
            </div>
        </Section>
    );
};

export default WarningSignsTab;
