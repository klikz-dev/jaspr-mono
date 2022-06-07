import Section from '../../Components/Section';
import BubbleQuestion from '../../Components/BubbleQuestion';
import HelpfulPersonQuestion from './HelpfulPersonQuestion';
import styles from './index.module.scss';

import { AssessmentAnswers } from 'state/types';
import { Questions } from 'components/ConversationalUi/questions';

interface MakeHomeSaferTabProps {
    answers: Partial<AssessmentAnswers>;
    questions: Questions;
    setAnswers: (
        answers: AssessmentAnswers | ((answers: AssessmentAnswers) => AssessmentAnswers),
    ) => void;
}

const MakeHomeSaferTab = ({ answers, questions, setAnswers }: MakeHomeSaferTabProps) => {
    return (
        <Section
            number="1"
            title="Immediate steps to Make Home Safer"
            tooltip="Limiting access to dangerous objects can save your life. How can you secure or remove means of potentially harming yourself?"
        >
            <div className={styles.questions}>
                <BubbleQuestion
                    title="To protect myself I plan to:"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="strategiesGeneral"
                    answerKey="strategiesGeneral"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Firearm"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="additionalStrategies"
                    answerKey="strategiesFirearm"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Medicine"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="additionalStrategies"
                    answerKey="strategiesMedicine"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Dangerous Places"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="additionalStrategies"
                    answerKey="strategiesPlaces"
                    questions={questions}
                />

                <BubbleQuestion
                    title="Other Hazards"
                    answers={answers}
                    setAnswers={setAnswers}
                    uid="additionalStrategies"
                    answerKey="strategiesOther"
                    questions={questions}
                    allowCustom
                />

                <HelpfulPersonQuestion answers={answers} setAnswers={setAnswers} />
            </div>
        </Section>
    );
};

export default MakeHomeSaferTab;
