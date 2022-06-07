import { useContext, useState } from 'react';
import { useHistory } from 'lib/router';
import { actionNames, addAction } from 'state/actions/analytics';
import { lockActivity, startAssessmentLockCounter } from 'state/actions/assessment';
import Menu from 'components/Menu';
import CUI from 'components/ConversationalUi';
import ProgressBar from './progressbar';
import Summaries from './summaries';
import styles from './index.module.scss';
import circleCheckedIcon from 'assets/circle-check.svg';
import jazIcon from 'assets/jazz.png';
import jasperIcon from 'assets/jasper.png';
import Button from 'components/Button';
import StoreContext from 'state/context/store';
import { Patient } from 'state/types';

const Interview = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { assessment, user } = store;
    const { assessmentLocked, activities } = assessment;
    const { assessmentLockTimer, timeSinceCheckin, guide } = user as Patient;
    const [showSummaries, setShowSummaries] = useState(false);

    const assessmentActivities = activities
        .filter((activity) => activity.type !== 'intro')
        .filter((activity) => activity.questions.length !== 0); // comfort_and_skills

    const toggleSummaries = () => {
        if (!showSummaries) {
            addAction(actionNames.SUMMARIES_OPEN);
        } else {
            addAction(actionNames.SUMMARIES_CLOSED);
        }
        setShowSummaries(!showSummaries);
    };

    const outro = activities.find((activity) => activity.type === 'outro');

    const done = () => {
        lockActivity(dispatch, outro);
    };

    const notDone = () => {
        startAssessmentLockCounter(dispatch, assessmentLockTimer + 1);
    };

    const confirmLock = Boolean(assessmentLockTimer) && timeSinceCheckin >= 5;

    const firstQuestionUID = assessmentActivities
        .map((activity) => activity.questions)
        .flat()
        .filter(
            (question) =>
                !question.actions.some((action) => ['section-change'].includes(action.type)),
        )
        .find((question) => question.uid)?.uid;

    return (
        <div className={styles.container}>
            <Menu selectedItem="cams" />
            {confirmLock && !assessmentLocked && (
                <div className={styles.lockOuter}>
                    <div className={styles.lockConfirm}>
                        <div className={styles.row}>
                            <img
                                className={styles.guide}
                                src={guide === 'Jaz' ? jazIcon : jasperIcon}
                                alt={`Your guide ${guide || 'Jaz'}`}
                            />
                            <span>
                                I’ve noticed that you haven’t updated your Interview in a little
                                bit. If you’re done with it, I’ll let your provider know.
                            </span>
                        </div>
                        <div className={styles.buttons}>
                            <Button variant="tertiary" onClick={notDone}>
                                I'm still working on it
                            </Button>
                            <Button onClick={done}>I'm done</Button>
                        </div>
                    </div>
                </div>
            )}
            {assessmentLocked && (
                <div className={styles.lockOuter}>
                    <div className={styles.popup}>
                        <img src={circleCheckedIcon} alt="Checked" />
                        <p>You have completed the interview.</p>

                        {activities.some((activity) =>
                            ['stability_pan', 'comfort_and_skills'].includes(activity.type),
                        ) && <Button onClick={() => history.replace('/')}>Close</Button>}
                    </div>
                </div>
            )}
            {!assessmentLocked && !confirmLock && activities.length && (
                <div className={styles.innerContainer}>
                    <CUI activities={assessmentActivities} firstQuestionUID={firstQuestionUID} />
                    {!showSummaries && (
                        <ProgressBar
                            activities={assessmentActivities}
                            toggleSummaries={toggleSummaries}
                        />
                    )}
                    {showSummaries && <Summaries toggleSummaries={toggleSummaries} />}
                </div>
            )}
        </div>
    );
};

export default Interview;
