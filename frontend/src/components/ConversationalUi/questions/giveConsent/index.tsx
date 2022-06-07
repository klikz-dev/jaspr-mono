import { useEffect, useState } from 'react';
import Modal, { Styles } from 'react-modal';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import zIndexHelper from 'lib/zIndexHelper';
import Segment, { AnalyticNames } from 'lib/segment';
import JahSignup from './jahSignup';
import { QuestionProps } from '../../question';
import styles from './index.module.scss';

const fullScreenModalStyle: Styles = {
    overlay: {
        backgroundColor: 'rgba(255,255,255,1)',
        zIndex: zIndexHelper('patient.jah-signup'),
    },
    content: {
        display: 'flex',
        flexDirection: 'column',
        border: 'none',
        backgroundColor: 'transparent',
        padding: 0,
        height: '100%',
        width: '100%',
        overflow: 'hidden',
    },
};

const checkBoolean = (value: any): any => {
    if (value === 'true') {
        return true;
    } else if (value === 'false') {
        return false;
    }
    return value;
};

interface Option {
    value: string | boolean;
    label: string;
    sublable: string;
}

type GiveConsentQuestionProps = Pick<QuestionProps, 'uid' | 'answerKey' | 'answered' | 'next'> & {
    options: Option[];
};

const GiveConsentQuestion = ({
    uid,
    options,
    answerKey,
    answered,
    next,
}: GiveConsentQuestionProps) => {
    const defaultValue: null = null;
    const [, updatedAnswer, , saveAnswer] = useQuestion(answerKey, defaultValue, true);
    const [showJahSignup, setShowJahSignup] = useState(false);

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    return (
        <>
            <div className={`${styles.options}`}>
                {options.map((option) => (
                    <label key={option.value.toString()} className={styles.option}>
                        <input
                            type="radio"
                            name={`give-consent-${uid}-${options
                                .map((option) => option.value)
                                .join('')}`}
                            checked={updatedAnswer === option.value}
                            onChange={(e) => {
                                const answer = checkBoolean(e.target.value);
                                saveAnswer(answer);
                                if (answer === false) {
                                    Segment.track(AnalyticNames.JAH_SIGNUP_CONSENT, {
                                        consented: false,
                                    });
                                    next();
                                } else {
                                    Segment.track(AnalyticNames.JAH_SIGNUP_CONSENT, {
                                        consented: true,
                                    });
                                    setShowJahSignup(true);
                                }
                            }}
                            value={option.value.toString()}
                        />
                        <span className={styles.label}>
                            {option.label}
                            {Boolean(option.sublable) ? '\n\n' : ''}
                            <span className={styles.sublable}>{option.sublable}</span>
                        </span>
                    </label>
                ))}
            </div>
            <Modal isOpen={showJahSignup} style={fullScreenModalStyle}>
                <JahSignup
                    close={() => {
                        setShowJahSignup(false);
                        next();
                    }}
                />
            </Modal>
        </>
    );
};

export { GiveConsentQuestion };
export default GiveConsentQuestion;
