import React from 'react';
import { useHistory } from 'lib/router';
import styles from './index.module.scss';
import { AssessmentAnswers } from 'state/types';
import { Questions } from 'components/ConversationalUi/questions';
import Pencil from 'assets/icons/Pencil';

interface StabilityPlanProps {
    edit?: boolean;
    answers: AssessmentAnswers;
    questions?: Questions;
}

const StabilityPlan = ({ edit = false, answers, questions = [] }: StabilityPlanProps) => {
    const history = useHistory();

    return (
        <div className={styles.stabilityPlanList}>
            <div className={styles.stabilityPlanListItem}>
                <div className={styles.stabilityPlanListItemNumber}>
                    <div>1</div>
                </div>
                <div className={styles.stabilityPlanListItemContent}>
                    <div className={styles.contentHeader}>
                        Immediate Steps To Take
                        {edit && (
                            <div
                                className={styles.editButton}
                                onClick={() => history.push('/takeaway/stability-plan/safer')}
                            >
                                <span className={styles.editLabel}>Edit</span>
                                <Pencil color="#000000" height={13} />
                            </div>
                        )}
                    </div>
                    <div className={styles.textBlock}>To protect myself I plan to:</div>
                    <ul className={styles.bulletedList}>
                        {(answers.strategiesGeneral || []).map((strategy, idx) => (
                            <li key={`${strategy}-${idx}`}>
                                <span className={styles.textBlock}>{strategy}</span>
                            </li>
                        ))}
                    </ul>
                    {['Firearm', 'Medicine', 'Places', 'Other', 'Custom'].map(
                        (strategyCategory) => {
                            const strategies: string[] =
                                answers[`strategies${strategyCategory}`] || [];
                            if (!strategies.length) return null;
                            return (
                                <React.Fragment key={strategyCategory}>
                                    <div className={styles.textBlock}>{strategyCategory}:</div>
                                    <ul className={styles.bulletedList}>
                                        {(answers[`strategies${strategyCategory}`] || []).map(
                                            (strategy: string, idx: number) => (
                                                <li key={`${strategy}-${idx}`}>
                                                    <span className={styles.textBlock}>
                                                        {strategy}
                                                    </span>
                                                </li>
                                            ),
                                        )}
                                    </ul>
                                </React.Fragment>
                            );
                        },
                    )}
                    {answers.meansSupportYesNo && answers.meansSupportWho && (
                        <div className={styles.textBlock}>
                            I will ask{' '}
                            <span className={styles.boldTextBlock}>{answers.meansSupportWho}</span>{' '}
                            for help with this plan.
                        </div>
                    )}
                </div>
            </div>

            <div className={styles.stabilityPlanListItem}>
                <div className={styles.stabilityPlanListItemNumber}>
                    <div>2</div>
                </div>
                <div className={styles.stabilityPlanListItemContent}>
                    <div className={styles.contentHeader}>
                        Supportive People
                        {edit && (
                            <div
                                className={styles.editButton}
                                onClick={() => history.push('/takeaway/stability-plan/people')}
                            >
                                <span className={styles.editLabel}>Edit</span>
                                <Pencil color="#000000" height={13} />
                            </div>
                        )}
                    </div>
                    <div className={styles.textBlock}>My list of contacts who can help:</div>
                    <ul className={styles.unorderedList}>
                        {(answers.supportivePeople || []).map((obj) => (
                            <li key={`${obj.name}: ${obj.phone}`}>
                                <span className={styles.boldTextBlock}>{obj.name}:</span>{' '}
                                {obj.phone}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

            <div className={styles.stabilityPlanListItem}>
                <div className={styles.stabilityPlanListItemNumber}>
                    <div>3</div>
                </div>
                <div className={styles.stabilityPlanListItemContent}>
                    <div className={styles.contentHeader}>
                        Reasons for Living
                        {edit && (
                            <div
                                className={styles.editButton}
                                onClick={() => history.push('/takeaway/stability-plan/reasons')}
                            >
                                <span className={styles.editLabel}>Edit</span>
                                <Pencil color="#000000" height={13} />
                            </div>
                        )}
                    </div>
                    <ol className={styles.orderedList}>
                        {(answers?.reasonsLive || []).map((reason, idx) => (
                            <li key={idx} className={styles.italicTextBlock}>
                                {reason}
                            </li>
                        ))}
                    </ol>
                </div>
            </div>

            <div className={styles.stabilityPlanListItem}>
                <div className={styles.stabilityPlanListItemNumber}>
                    <div>4</div>
                </div>
                <div className={styles.stabilityPlanListItemContent}>
                    <div className={styles.contentHeader}>
                        Recognize Warning Signs
                        {edit && (
                            <div
                                className={styles.editButton}
                                onClick={() => history.push('/takeaway/stability-plan/warnings')}
                            >
                                <span className={styles.editLabel}>Edit</span>
                                <Pencil color="#000000" height={13} />
                            </div>
                        )}
                    </div>
                    <div className={styles.textBlock}>
                        I know I'm about to be in a crisis when I experience:
                    </div>
                    <ul className={styles.unorderedList}>
                        {['Actions', 'Feelings', 'Thoughts', 'Stressors'].map((word) => {
                            /**
                            List all the selected items in each group.
                            Items that have been placed in the top warning signs list should be bolded.
                            Items that are custom items generated by the patient should be in quotes.
                            If an item is both in the top warning signs list and is custom, it should be bolded and quoted.
                            */

                            const answerKey = `ws${word}`;
                            const warningSigns: string[] = answers[answerKey] || [];
                            const question = questions.find((question) =>
                                question.actions.some(
                                    (action) =>
                                        'answerKey' in action && action.answerKey === answerKey,
                                ),
                            );
                            if (!question) return null;
                            const action = question.actions.find(
                                (action) => 'answerKey' in action && action.answerKey === answerKey,
                            );
                            const choices = 'choices' in action ? action.choices : [];

                            if (!warningSigns.length) return null;
                            return (
                                <li key={word}>
                                    <span className={styles.boldTextBlock}>{word}:</span>{' '}
                                    {warningSigns.map((warningSign, idx) => {
                                        return (
                                            <React.Fragment key={`${warningSign}-{idx}`}>
                                                <span
                                                    className={
                                                        (answers.wsTop || []).includes(warningSign)
                                                            ? styles.boldTextBlock
                                                            : styles.textBlock
                                                    }
                                                >
                                                    {choices.includes(warningSign)
                                                        ? warningSign
                                                        : `"${warningSign}"`}
                                                </span>
                                                {warningSigns.length !== idx + 1 && (
                                                    <span>{', '}</span>
                                                )}
                                            </React.Fragment>
                                        );
                                    })}
                                </li>
                            );
                        })}
                    </ul>
                </div>
            </div>

            <div className={styles.stabilityPlanListItem}>
                <div className={styles.stabilityPlanListItemNumber}>
                    <div>5</div>
                </div>
                <div className={styles.stabilityPlanListItemContent}>
                    <div className={styles.contentHeader}>
                        Coping Strategies
                        {edit && (
                            <div
                                className={styles.editButton}
                                onClick={() => history.push('/takeaway/stability-plan/skills')}
                            >
                                <span className={styles.editLabel}>Edit</span>
                                <Pencil color="#000000" height={13} />
                            </div>
                        )}
                    </div>
                    <div className={styles.textBlock}>The top strategies that help me cope:</div>
                    {['Body', 'Distract', 'Help Others', 'Courage', 'Senses'].map(
                        (copingCategory) => {
                            /**
                            List all the selected items in each group.
                            Items that have been placed in the top coping strategies list should be bolded.
                            Items that are custom items generated by the patient should be in quotes.
                            If an item is both in the top coping strategies list and is custom, it should be bolded and quoted.
                            */

                            const answerKey = `coping${copingCategory.replace(/\s+/, '')}`;
                            const copingStrategies: string[] = answers[answerKey] || [];
                            const question = questions.find((question) =>
                                question.actions.some(
                                    (action) =>
                                        'answerKey' in action && action.answerKey === answerKey,
                                ),
                            );
                            if (!question) return null;
                            const action = question.actions.find(
                                (action) => 'answerKey' in action && action.answerKey === answerKey,
                            );
                            const choices = 'choices' in action ? action.choices : [];
                            if (!copingStrategies.length) return null;
                            return (
                                <React.Fragment key={copingCategory}>
                                    <div className={styles.textBlock}>{copingCategory}:</div>
                                    <ul className={styles.bulletedList}>
                                        {copingStrategies.map((copingStrategy, idx) => (
                                            <li key={`${copingStrategy}-${idx}`}>
                                                <span
                                                    className={
                                                        (answers.copingTop || []).includes(
                                                            copingStrategy,
                                                        )
                                                            ? styles.boldTextBlock
                                                            : styles.textBlock
                                                    }
                                                >
                                                    {choices.includes(copingStrategy)
                                                        ? copingStrategy
                                                        : `"${copingStrategy}"`}
                                                </span>
                                            </li>
                                        ))}
                                    </ul>
                                </React.Fragment>
                            );
                        },
                    )}
                    <div className={styles.textBlock}>Other:</div>
                    <ul className={styles.bulletedList}>
                        <li>Watch Jaspr Videos</li>
                        <li>24/7 National Hotline, call 1-800-273-8255, text 741741</li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export { StabilityPlan };
export default StabilityPlan;
