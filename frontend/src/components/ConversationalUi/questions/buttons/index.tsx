import { useContext } from 'react';
import { useHistory } from 'lib/router';
import { completeTour } from 'state/actions/user';
import { actionNames, addAction } from 'state/actions/analytics';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import StoreContext from 'state/context/store';
import Button from 'components/Button';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

interface ButtonType {
    label: string;
    selected?: boolean;
    analyticsAction?: keyof typeof actionNames;
    action?: string;
    params?: string;
    path?: string;
    goto?: string[];
}

export type ButtonProps = Pick<
    QuestionProps,
    'answered' | 'setAnswered' | 'next' | 'isValid' | 'validate' | 'setShowValidation' | 'answerKey'
> & {
    orientation?: 'vertical' | 'horizontal';
    submissionInProgress: boolean;
    setSubmissionInProgress: (submissionInProgress: boolean) => void;
    buttons: ButtonType[];
    validation?: boolean;
};

const Buttons = (props: ButtonProps) => {
    const history = useHistory();
    const {
        answered,
        buttons,
        setAnswered,
        next,
        isValid,
        validation,
        validate,
        setShowValidation,
        answerKey,
        orientation,
        submissionInProgress,
        setSubmissionInProgress,
    } = props;
    const [, dispatch] = useContext(StoreContext);
    const [, updatedAnswer, , saveAnswer] = useQuestion<string>(answerKey, '', true);

    const onClick = (button: ButtonType) => {
        const handleValidation = () => {
            if (answerKey) {
                saveAnswer(button.label);
            }
            setAnswered(Boolean(button.label));

            if (button.analyticsAction) {
                addAction(actionNames[button.analyticsAction]);
            }

            if (button.action === 'navigate') {
                if (button.params === '?completeTour=true') {
                    // TODO This is a hack.  It doesn't really belong in this component
                    completeTour(dispatch);
                }
                history.push({ pathname: button.path, search: button.params || '' });
            } else {
                next(button.goto);
            }
        };
        setShowValidation(false);
        if (validate?.current) {
            setSubmissionInProgress(true);
            validate
                .current()
                .then(handleValidation)
                .catch((err) => {})
                .finally(() => setSubmissionInProgress(false));
        } else {
            if (!validation || isValid) {
                handleValidation();
            } else {
                setShowValidation(true);
            }
        }
    };

    const buttonShouldBeHidden = (button: ButtonType) => {
        return !(
            (answered && button.label === 'Done') ||
            (answered && answerKey && updatedAnswer !== button.label) ||
            (answered && button.selected === false)
        );
    };

    return (
        <div className={styles.container}>
            <div
                className={`${styles.buttons} ${Boolean(answered) ? styles.selected : {}} ${
                    orientation === 'horizontal' ? styles.row : styles.column
                }`}
            >
                {buttons.filter(buttonShouldBeHidden).map((button) => (
                    <Button
                        dark
                        key={button.label}
                        onClick={() => onClick(button)}
                        disabled={submissionInProgress || answered}
                    >
                        {button.label}
                    </Button>
                ))}
            </div>
        </div>
    );
};

export { Buttons };
export default Buttons;
