import StabilityCard from 'components/StabilityCard';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';
import { AssessmentAnswers } from 'state/types';

type StabilityCardQuestionProps = Pick<QuestionProps, 'answered'> & {
    empty?: boolean;
    answers: AssessmentAnswers;
};

const StabilityCardQuestion = (props: StabilityCardQuestionProps) => {
    const { answered, empty = false, answers } = props;

    return (
        <div className={styles.container} style={{ display: !answered ? 'flex' : 'none' }}>
            <StabilityCard empty={empty} answers={answers} />
        </div>
    );
};

export { StabilityCardQuestion };
export default StabilityCardQuestion;
