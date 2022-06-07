import { useContext } from 'react';
import Button from 'components/Button';
import StoreContext from 'state/context/store';
import { lockActivity } from 'state/actions/assessment';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

type AssessmentLockQuestionProps = Pick<QuestionProps, 'setAnswered' | 'answered' | 'next'>;

const AssessmentLockQuestion = ({ next }: AssessmentLockQuestionProps): JSX.Element => {
    const [store, dispatch] = useContext(StoreContext);
    const { assessment } = store;

    const outro = assessment?.activities.find((activity) => activity.type === 'outro');

    const done = () => {
        lockActivity(dispatch, outro);
    };

    return (
        <div className={styles.buttons}>
            <Button onClick={done} dark>
                I'm done
            </Button>
        </div>
    );
};

export { AssessmentLockQuestion };
export default AssessmentLockQuestion;
