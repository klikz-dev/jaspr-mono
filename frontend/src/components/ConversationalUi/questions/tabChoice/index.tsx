import { useEffect, useState } from 'react';
import { useQuestion } from 'components/ConversationalUi/hooks/useQuestion';
import styles from './index.module.scss';
import { QuestionProps } from '../../question';

interface Option {
    value: string;
    label: string;
}

type GroupProps = Pick<QuestionProps, 'setAnswered' | 'uid' | 'answered' | 'answerKey'> & {
    display: boolean;
    options: Option[];
};

const Group = (props: GroupProps) => {
    const { answerKey, setAnswered, uid, options, answered, display } = props;
    const [, updatedAnswer, setAnswer, saveAnswer] = useQuestion<string[]>(answerKey, [], false);

    const checkOption = (option: string) => {
        let updatedAnswers = null;
        if (updatedAnswer.includes(option)) {
            updatedAnswers = updatedAnswer.filter((current) => current !== option); // Remove from list
        } else {
            updatedAnswers = [...updatedAnswer, option];
        }
        setAnswer(updatedAnswers);
        setAnswered(false);
    };

    useEffect(() => {
        if (answered) {
            saveAnswer();
        }
    }, [answered, saveAnswer]);

    return (
        <div className={styles.optionsContainer} style={{ display: display ? 'flex' : 'none' }}>
            {options.map((option) => (
                <div
                    key={`${uid}-tab-${option.value}`}
                    className={`${styles.option} ${
                        updatedAnswer.includes(option.value) ? styles.active : ''
                    }`}
                    onClick={() => {
                        checkOption(option.value);
                    }}
                >
                    {option.label}
                </div>
            ))}
        </div>
    );
};

type TabChoiceQuestionProps = Pick<QuestionProps, 'uid' | 'setAnswered' | 'answered'> & {
    groups: {
        label: string;
        options: Option[];
        answerKey: string;
    }[];
};

const TabChoiceQuestion = (props: TabChoiceQuestionProps) => {
    const { uid, setAnswered, groups, answered } = props;
    const [currentTab, setCurrentTab] = useState(groups[0].label);
    return (
        <div className={styles.container}>
            <div className={styles.tabs}>
                {groups.map((group) => (
                    <div
                        key={`${uid}-group-${group.label}`}
                        className={`${styles.tab} ${
                            currentTab === group.label ? styles.active : ''
                        }`}
                        onClick={() => setCurrentTab(group.label)}
                    >
                        {group.label}
                    </div>
                ))}
            </div>
            {groups.map((group) => (
                <Group
                    key={`${uid}-tab-${group.label}`}
                    uid={uid}
                    options={group.options}
                    answerKey={group.answerKey}
                    setAnswered={setAnswered}
                    answered={answered}
                    display={group.label === currentTab}
                />
            ))}
        </div>
    );
};

export { TabChoiceQuestion };
export default TabChoiceQuestion;
