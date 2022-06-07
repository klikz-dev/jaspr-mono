import { useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import scrollIntoView from 'smooth-scroll-into-view-if-needed';
import { getAnswers, lockActivity, setCurrentSectionUid } from 'state/actions/assessment';
import StoreContext from 'state/context/store';
import Modal, { Styles } from 'react-modal';
import zIndexHelper from 'lib/zIndexHelper';
import styles from './index.module.scss';
import Question from './question';
import closeIcon from 'assets/close.png';
import { AssignedActivities, UIDType } from './questions';
import { Patient } from 'state/types';
import Sentry from 'lib/sentry';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'space-evenly',
        backgroundColor: 'rgba(45, 44, 63, 0.85)',
        zIndex: zIndexHelper('patient.offline'),
    },
    content: {
        position: 'static',
        display: 'flex',
        width: 'auto',
        height: 'auto',
        alignSelf: 'center',
        backgroundColor: 'transparent',
        border: 'none',
    },
};

interface QuestionsProps {
    disableAnalytics?: boolean;
    activities: AssignedActivities;
    firstQuestionUID?: UIDType;
}

const Questions = (props: QuestionsProps) => {
    const { disableAnalytics = false, firstQuestionUID, activities } = props;
    const [store, dispatch] = useContext(StoreContext);
    const [assessmentResumptionCheck, setAssessmentResumptionCheck] = useState(false);
    const [answersFetched, setAnswersFetched] = useState(false);
    const { assessment, user } = store;
    const { token, online, inEr, userType } = user as Patient;
    const { currentSectionUid } = assessment;
    const [showOfflineModal, setShowOfflineModal] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null!);
    const surveyRef = useRef(null);
    const lastQuestionRef = useRef<HTMLDivElement>(null);
    const questionsRef = useRef([]);
    const prevIndex = useRef<number | null>(0);
    const [currentActivity, setCurrentActivity] = useState<string>(null);
    const activeActivities = activities.filter((activity) => !activity.locked);
    const activity = activeActivities.find((activity) => activity.type === currentActivity);
    const questions = useMemo(
        () =>
            activity?.questions.filter(
                (question) => !question.actions.some((action) => action.type === 'section-change'),
            ) || [],
        [activity?.questions],
    );
    const currentIndex = questions.findIndex(
        (question) => question.uid === currentSectionUid && currentSectionUid !== null,
    );
    const numberOfQuestions = questions?.length || 0;

    useEffect(() => {
        let currentActivity = activeActivities[0];
        if (currentSectionUid) {
            currentActivity =
                activeActivities.find((activity) =>
                    activity.questions.some((question) => question.uid === currentSectionUid),
                ) || currentActivity;
        }

        if (currentActivity) {
            setCurrentActivity(currentActivity.type);
            if (
                currentActivity.questions.findIndex(
                    (question) => question.uid === currentSectionUid,
                ) === -1
            ) {
                setCurrentSectionUid(
                    dispatch,
                    currentActivity.questions.filter(
                        (question) => !question.uid.startsWith('sectionChange'),
                    )[0].uid,
                );
            }
        }
    }, [activeActivities, currentSectionUid, dispatch]);

    useEffect(() => {
        (async () => {
            if (token && userType === 'patient' && inEr) {
                await getAnswers(dispatch);
                setAnswersFetched(true);
            }
        })();
    }, [token, dispatch, userType, inEr]);

    useEffect(() => {
        setShowOfflineModal(online === false);
    }, [online]);

    const goToQuestion = useCallback(
        (sectionUid) => setCurrentSectionUid(dispatch, sectionUid),
        [dispatch],
    );

    useEffect(() => {
        if (numberOfQuestions > 0) {
            const skipAhead = prevIndex.current !== currentIndex - 1;
            prevIndex.current = currentIndex;
            if (lastQuestionRef.current) {
                scrollIntoView(lastQuestionRef.current, {
                    behavior: skipAhead ? 'auto' : 'smooth',
                    block: 'start',
                });
            }
        }
    }, [currentIndex, numberOfQuestions]);

    useEffect(() => {
        if (
            answersFetched &&
            numberOfQuestions > 0 &&
            firstQuestionUID &&
            !assessmentResumptionCheck &&
            currentSectionUid &&
            currentSectionUid !== firstQuestionUID
        ) {
            // Resume from last question
            goToQuestion(currentSectionUid);
            setAssessmentResumptionCheck(true);
        }
    }, [
        goToQuestion,
        currentSectionUid,
        assessmentResumptionCheck,
        firstQuestionUID,
        numberOfQuestions,
        answersFetched,
    ]);

    const next = useCallback(
        (advance = true, goTo: UIDType[] = []): void => {
            if (currentIndex < questions.length - 1 && advance) {
                if (goTo.length) {
                    let sectionFound = false;
                    goTo.forEach((section) => {
                        // Can only skip to questions in the same module
                        const nextQuestion = questions.find((question) => question.uid === section);
                        if (nextQuestion) {
                            setCurrentSectionUid(dispatch, nextQuestion.uid);
                            sectionFound = true;
                        }
                    });
                    if (!sectionFound) {
                        setCurrentSectionUid(dispatch, questions[currentIndex + 1].uid);
                    }
                } else {
                    setCurrentSectionUid(dispatch, questions[currentIndex + 1].uid);
                }
            } else if (advance) {
                // GO TO NEXT ACTIVITY
                lockActivity(dispatch, activity);
                const activityIndex = activeActivities.findIndex(
                    (activeActivity) => activeActivity.id === activity.id,
                );
                if (activityIndex + 1 < activeActivities.length) {
                    const nextSectionUid = activeActivities[activityIndex + 1].questions.find(
                        (question) => !question.uid.startsWith('sectionChange'),
                    ).uid;
                    setCurrentSectionUid(dispatch, nextSectionUid);
                }
            }
        },
        [activeActivities, activity, currentIndex, dispatch, questions],
    );

    useEffect(() => {
        if (assessmentResumptionCheck && activity && currentIndex === -1) {
            // TODO let's remove the section change questions in favor of a different delineation method
            if (!currentSectionUid?.startsWith('sectionChange')) {
                console.warn('CUI in Invalid State', activity, currentSectionUid);
                Sentry.captureException(
                    `CUI in invalid state.  Current section uid is ${currentSectionUid} and active activity is ${activity.id} ${activity.type} ${activity.status}`,
                );
            }
            next();
        }
    }, [activity, assessmentResumptionCheck, currentIndex, currentSectionUid, next]);

    return (
        <div className={styles.container} ref={containerRef}>
            <div className={styles.survey} ref={surveyRef}>
                {questions
                    ?.filter((val, idx) => idx <= currentIndex)
                    .map((questionGroup, idx) => {
                        return (
                            <Question
                                key={`${questionGroup.uid}-${idx}`}
                                activityId={activity.id}
                                questionGroup={questionGroup}
                                idx={idx}
                                currentIndex={currentIndex}
                                lastQuestionRef={lastQuestionRef}
                                next={next}
                                uid={questionGroup.uid}
                                questions={questionsRef.current}
                                disableAnalytics={disableAnalytics}
                            />
                        );
                    })}
            </div>
            <Modal isOpen={showOfflineModal} style={modalStyle}>
                <div className={styles.offlineModal}>
                    <img
                        className={styles.closeButton}
                        src={closeIcon}
                        alt="Close offline alert"
                        onClick={() => setShowOfflineModal(false)}
                    />
                    Sorry, no internet connection.
                    <br />
                    Please try again.
                    <div className={styles.button} onClick={() => setShowOfflineModal(false)}>
                        Okay
                    </div>
                </div>
            </Modal>
        </div>
    );
};

export default Questions;
