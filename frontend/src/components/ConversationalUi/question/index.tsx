import React, { useContext, useCallback, useEffect, useRef, useState } from 'react';
import Sentry from 'lib/sentry';
import toast from 'lib/toast';
import { actionNames, addAction } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import { CSSTransition } from 'react-transition-group';
import { AnswerContext } from '../context';
import { getQuestions, saveAnswers } from 'state/actions/assessment';
import styles from './index.module.scss';
import RankQuestion from '../questions/rank';
import TextQuestion from '../questions/text';
import ListQuestion from '../questions/list';
import ChoiceQuestion from '../questions/choice';
import CounterQuestion from '../questions/counter';
import GiveConsentQuestion from '../questions/giveConsent';
import AssessmentLock from '../questions/assessmentLock';
import InlineMessage from '../questions/message';
import Buttons from '../questions/buttons';
import Video from '../questions/video';
import SecurityImage from '../questions/securityImage';
import SecurityQuestion from '../questions/securityQuestion';
import ScaleButtonsQuestion from '../questions/scalebuttons';
import TabChoiceQuestion from '../questions/tabChoice';
import MeansCustomQuestion from '../questions/meansCustom';
import ComfortSkillsQuestion from '../questions/comfortSkills';
import SharedStoriesQuestion from '../questions/sharedStories';
import CopingStrategiesQuestion from '../questions/copingStrategies';
import SupportivePeopleQuestion from '../questions/supportivePeople';
import RankTopQuestion from '../questions/rankTop';
import StabilityCardQuestion from '../questions/stabilityCard';
import SliderQuestion from '../questions/slider';
import SortEditQuestion from '../questions/sortEdit';
import ListRankQuestion from '../questions/listRank';
import { Patient, AssessmentAnswers } from 'state/types';
import {
    ActionType,
    ListType,
    Question as QuestionType,
    Questions as QuestionsType,
    UIDType,
} from '../questions';

interface Props {
    questionGroup: QuestionType;
    idx: number;
    activityId: number;
    currentIndex: number;
    lastQuestionRef: React.Ref<HTMLDivElement>;
    next: (advance?: boolean, goTo?: UIDType[]) => void;
    uid: string;
    disableAnalytics?: boolean;
    questions: QuestionsType;
}

export type QuestionProps = ActionType & {
    answerKey?: string;
    questions: QuestionsType;
    currentQuestion: boolean;
    currentAnswers: AssessmentAnswers;
    setAnswered: (answered: boolean) => void;
    answered: boolean;
    uid: UIDType;
    next: (goTo?: UIDType[]) => void;
    isValid: boolean;
    setIsValid: (valid: boolean) => void;
    showValidation: boolean | string;
    setShowValidation: (message: string | boolean) => void;
    validationRequired: boolean;
    validate: React.MutableRefObject<() => Promise<void | boolean> | null>;
};

const Question = (props: Props) => {
    const {
        questionGroup,
        activityId,
        idx,
        currentIndex,
        lastQuestionRef,
        next,
        uid,
        disableAnalytics,
        questions,
    } = props;

    const [store, dispatch] = useContext(StoreContext);
    const { assessment, user } = store;
    const { answers } = assessment;
    const { guide, activities } = user as Patient;

    const currentQuestion = idx === currentIndex;
    // Set these true by default and change to false in the onMount
    // useEffect so we can get a correctly calculated content height
    const [showActions, setShowActions] = useState<boolean>(true);
    const [answered, setAnswered] = useState<boolean>(currentQuestion);
    const [startAnalyticRecorded, setStartAnalyticRecorded] = useState<boolean>(false);
    const [submissionInProgress, setSubmissionInProgress] = useState<boolean>(false);
    const [updatedAnswers, setUpdatedAnswers] = useState({});

    // Only supports one validation per question
    const [isValid, setIsValid] = useState(false);
    const [showValidation, setShowValidation] = useState<string | boolean>(false);
    const validate = useRef<() => Promise<void>>(null);
    const transitionRef = useRef();

    const listActions = questionGroup.actions
        ? questionGroup.actions.filter<ListType>(
              (action: ActionType): action is ListType => action.type === 'list',
          )
        : [];

    // Checks if the question is the current question.  When editing a question that was previously
    // answered, we want to save the answer, but not advance the questions
    const checkNext = useCallback(
        async (goTo?: UIDType[]) => {
            next(currentQuestion, goTo);
        },
        [currentQuestion, next],
    );

    let pathCode = 1;
    if (activities?.csp && activities?.csa) {
        pathCode = 3;
    } else if (activities?.csp) {
        pathCode = 2;
    }

    const submitAnswers = useCallback(
        async (updatedAnswers) => {
            const response = await saveAnswers(dispatch, updatedAnswers, null, activityId);

            if (response?.data?.nonFieldErrors?.includes('activity is locked')) {
                getQuestions(dispatch);
                toast.error('This activity has been locked by your provider');
            }
        },
        [activityId, dispatch],
    );

    useEffect(() => {
        if (answered && Object.keys(updatedAnswers).length) {
            submitAnswers(updatedAnswers);
            setUpdatedAnswers({});
        }
    }, [answered, dispatch, submitAnswers, updatedAnswers]);

    const shouldSkipQuestion = useCallback(() => {
        if (
            currentQuestion &&
            questionGroup.hideIf?.length > 1 &&
            answers[questionGroup.hideIf[0]] === questionGroup.hideIf[1]
        ) {
            return true;
        } else if (questionGroup.showIf?.includes('SHOW_IF_PATH3') && pathCode !== 3) {
            return true;
        } else if (questionGroup.showIf?.includes('SHOW_IF_PATH2') && pathCode !== 2) {
            return true;
        } else if (
            currentQuestion &&
            questionGroup.showIf?.length > 1 &&
            answers[questionGroup.showIf[0]] !== questionGroup.showIf[1]
        ) {
            return true;
        }
        return false;
    }, [answers, currentQuestion, pathCode, questionGroup.hideIf, questionGroup.showIf]);

    // Record analytic
    useEffect(() => {
        if (
            !disableAnalytics &&
            currentQuestion &&
            !startAnalyticRecorded &&
            questionGroup.uid !== 'start' &&
            !shouldSkipQuestion()
        ) {
            setStartAnalyticRecorded(true);
            addAction(actionNames.ARRIVE, { sectionUid: questionGroup.uid });
        }
    }, [
        startAnalyticRecorded,
        currentQuestion,
        questionGroup.uid,
        dispatch,
        shouldSkipQuestion,
        disableAnalytics,
    ]);

    useEffect(() => {
        if (shouldSkipQuestion()) {
            checkNext();
        }
    }, [shouldSkipQuestion, checkNext]);

    useEffect(() => {
        if (!currentQuestion) {
            setAnswered(true);
            setShowActions(true);
        } else {
            setAnswered(false);
            setShowActions(false);
            const showActionTimer = setTimeout(
                () => setShowActions(true),
                (questionGroup.guide || []).length * 1500,
            );
            return () => clearTimeout(showActionTimer);
        }
    }, [idx, currentQuestion, questionGroup.guide, currentIndex]);

    if (
        questionGroup?.hideIf?.length > 1 &&
        answers[questionGroup.hideIf[0]] === questionGroup.hideIf[1]
    ) {
        return null;
    } else if (
        questionGroup &&
        questionGroup.showIf?.length > 1 &&
        answers[questionGroup.showIf[0]] !== questionGroup.showIf[1]
    ) {
        return null;
    } else if (questionGroup.showIf?.includes('SHOW_IF_PATH3') && pathCode !== 3) {
        return null;
    } else if (questionGroup.showIf?.includes('SHOW_IF_PATH2') && pathCode !== 2) {
        return null;
    }

    if (
        questionGroup.hideIf?.length > 1 &&
        answers[questionGroup.hideIf[0]] === questionGroup.hideIf[1]
    ) {
        return null;
    } else if (
        questionGroup.showIf?.length > 1 &&
        answers[questionGroup.showIf[0]] !== questionGroup.showIf[1]
    ) {
        return null;
    }

    return (
        <AnswerContext.Provider
            value={{
                answers: updatedAnswers,
                updateAnswers: setUpdatedAnswers,
            }}
        >
            <CSSTransition
                appear
                in={true}
                style={{ display: 'flex', flexDirection: 'column' }}
                nodeRef={currentQuestion ? lastQuestionRef : transitionRef}
                classNames={{
                    enter: styles.enter,
                    enterActive: styles.enterActive,
                    enterDone: styles.enterDone,
                }}
                timeout={1}
            >
                <div
                    className={styles.question}
                    ref={currentQuestion ? lastQuestionRef : transitionRef}
                    style={{ transition: 'opacity 2s ease', opacity: 0 }}
                >
                    <div>
                        {questionGroup.guide.map((message, i) => (
                            <InlineMessage
                                key={message}
                                message={message}
                                index={i}
                                currentQuestion={currentQuestion}
                            />
                        ))}
                    </div>

                    {/* Lists need to be in a Row */}
                    {showActions && Boolean(listActions.length) && (
                        <div
                            style={{
                                display: 'flex',
                                flexDirection: 'row',
                                margin: '21px 150px',
                            }}
                        >
                            {listActions.map((action) => (
                                <div
                                    key={action.answerKey}
                                    style={{
                                        display: 'flex',
                                        flexDirection: 'column',
                                        flexBasis: '50%',
                                    }}
                                >
                                    <ListQuestion
                                        {...action}
                                        setAnswered={setAnswered}
                                        answered={answered}
                                    />
                                </div>
                            ))}
                        </div>
                    )}

                    {showActions &&
                        Boolean(questionGroup.actions) &&
                        questionGroup.actions
                            .filter(
                                (action) =>
                                    action.type !== 'list' &&
                                    (!('guide' in action) || action.guide === guide),
                            )
                            .map((action) => {
                                if (action.type === 'buttons') {
                                    return (
                                        <Buttons
                                            key={`button-${questionGroup.uid}`}
                                            {...action}
                                            buttons={action.buttons}
                                            isValid={isValid}
                                            setShowValidation={setShowValidation}
                                            next={checkNext}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                            validate={validate}
                                            submissionInProgress={submissionInProgress}
                                            setSubmissionInProgress={setSubmissionInProgress}
                                        />
                                    );
                                } else if (action.type === 'scalebuttons') {
                                    return (
                                        <ScaleButtonsQuestion
                                            key={`scalebuttons-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                        />
                                    );
                                } else if (action.type === 'text') {
                                    return (
                                        <TextQuestion
                                            key={`text-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                        />
                                    );
                                } else if (action.type === 'rank') {
                                    return (
                                        <div
                                            style={{ margin: '0 168px' }}
                                            key={`rank-${questionGroup.uid}`}
                                        >
                                            {/* @ts-ignore // TODO Fix after looking at props */}
                                            <RankQuestion
                                                {...action}
                                                setAnswered={setAnswered}
                                                answered={answered}
                                            />
                                        </div>
                                    );
                                } else if (action.type === 'list-rank') {
                                    return (
                                        <div
                                            style={{ margin: '0 168px' }}
                                            key={`list-rank-${questionGroup.uid}`}
                                        >
                                            <ListRankQuestion
                                                {...action}
                                                setAnswered={setAnswered}
                                                answered={answered}
                                            />
                                        </div>
                                    );
                                } else if (action.type === 'choice') {
                                    return (
                                        <ChoiceQuestion
                                            key={`choice-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                            uid={uid}
                                            vertical={Boolean(action.vertical)}
                                        />
                                    );
                                } else if (action.type === 'counter') {
                                    return (
                                        <CounterQuestion
                                            key={`counter-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                        />
                                    );
                                } else if (action.type === 'video') {
                                    return (
                                        <Video
                                            key={`video-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                            next={checkNext}
                                        />
                                    );
                                } else if (action.type === 'security-image') {
                                    return (
                                        <SecurityImage
                                            key={`security-image-${questionGroup.uid}`}
                                            currentQuestion={currentQuestion}
                                            isValid={isValid}
                                            setIsValid={setIsValid}
                                            validate={validate}
                                            setShowValidation={setShowValidation}
                                            showValidation={showValidation}
                                        />
                                    );
                                } else if (action.type === 'security-question') {
                                    return (
                                        <SecurityQuestion
                                            key={`security-question-${questionGroup.uid}`}
                                            answered={answered}
                                            isValid={isValid}
                                            setIsValid={setIsValid}
                                            validate={validate}
                                            setShowValidation={setShowValidation}
                                            showValidation={showValidation}
                                            currentQuestion={currentQuestion}
                                        />
                                    );
                                } else if (action.type === 'tab-choice') {
                                    return (
                                        <TabChoiceQuestion
                                            key={`tab-choice-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                            uid={uid}
                                        />
                                    );
                                } else if (action.type === 'means-custom') {
                                    return (
                                        <MeansCustomQuestion
                                            key={`means-custom-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                        />
                                    );
                                } else if (action.type === 'comfort-skills') {
                                    return (
                                        <ComfortSkillsQuestion
                                            key={`comfort-skills-${questionGroup.uid}`}
                                            {...action}
                                        />
                                    );
                                } else if (action.type === 'shared-stories') {
                                    return (
                                        <SharedStoriesQuestion
                                            key={`shared-stories-${questionGroup.uid}`}
                                            {...action}
                                        />
                                    );
                                } else if (action.type === 'coping-strategy') {
                                    // Do not change coping strategy choices without coordinating with the backend
                                    return (
                                        <CopingStrategiesQuestion
                                            key={`coping-strategies-${questionGroup.uid}`} // TODO Change all of these to UID
                                            {...action}
                                            questions={questions}
                                            currentAnswers={answers}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                            isValid={isValid}
                                            setIsValid={setIsValid}
                                            showValidation={showValidation}
                                            setShowValidation={setShowValidation}
                                            validate={validate}
                                        />
                                    );
                                } else if (action.type === 'supportive-people') {
                                    return (
                                        <SupportivePeopleQuestion
                                            key={`supportive-people-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                        />
                                    );
                                } else if (action.type === 'rank-top') {
                                    return (
                                        <RankTopQuestion
                                            key={`rank-top-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                        />
                                    );
                                } else if (action.type === 'stability-card') {
                                    return (
                                        <StabilityCardQuestion
                                            key={`stability-card-${questionGroup.uid}`}
                                            {...action}
                                            answered={answered}
                                            answers={answers}
                                        />
                                    );
                                } else if (action.type === 'sort-edit') {
                                    return (
                                        <SortEditQuestion
                                            key={`sort-edit-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                        />
                                    );
                                } else if (action.type === 'slider') {
                                    return (
                                        <SliderQuestion
                                            key={`slider-${questionGroup.uid}`}
                                            {...action}
                                            setAnswered={setAnswered}
                                            answered={answered}
                                        />
                                    );
                                } else if (action.type === 'give-consent') {
                                    return (
                                        <GiveConsentQuestion
                                            key={`give-consent-${questionGroup.uid}`}
                                            {...action}
                                            answered={answered}
                                            uid={uid}
                                            next={checkNext}
                                        />
                                    );
                                } else if (action.type === 'assessment-lock') {
                                    return (
                                        <AssessmentLock
                                            key="assessment_lock"
                                            setAnswered={setAnswered}
                                            answered={answered}
                                            next={checkNext}
                                        />
                                    );
                                }
                                Sentry.captureException(
                                    `Tried to render question with unknown type ${action.type}`,
                                );
                                return null; // Question type not found
                            })}
                </div>
            </CSSTransition>
        </AnswerContext.Provider>
    );
};

export default Question;
