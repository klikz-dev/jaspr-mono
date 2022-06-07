import React, { useContext, useCallback, useEffect, useRef, useState } from 'react';
import * as Sentry from 'sentry-expo';
import { setCurrentSectionUid } from 'state/actions/assessment';
import { actionNames, addAction } from 'state/actions/analytics';
import StoreContext from 'state/context/store';
import { Platform, Dimensions, KeyboardAvoidingView } from 'react-native';
//import Sentry from 'lib/sentry';
import Styled from 'styled-components/native';
import InlineMessage from '../questions/message';
import Buttons from '../questions/buttons';
import Slideshow from '../questions/slideshow';
import AccountActivation from '../questions/accountActivation';
import styles from './index.module.scss';
import HomeButton from '../questions/homeButton';
import AccountCode from '../questions/accountCode';
import PrivacyPolicy from '../questions/privacyPolicy';
import SetPassword from '../questions/setPassword';
import RequestPermission from '../questions/requestPermission';
import InfoModal from '../questions/infoModal';
import { useKeyboard } from 'lib/useKeyboard';
import { Patient, AssessmentAnswers } from 'state/types';
import {
    ActionType,
    ListType,
    Question as QuestionType,
    Questions as QuestionsType,
    UIDType,
} from '../questions';

const Container = Styled.View<{ minHeight: number }>`
    display: flex;
    align-self: flex-start;
    flex-direction: column;
    width: 100%;
    padding-top: 28px;
    padding-bottom: 14px;
    min-height: ${({ minHeight }) => `${minHeight}px`}
`;
const QuestionContainer = Styled.KeyboardAvoidingView`${styles.question}; flex-grow: 1; `;
const View = Styled.View`flex-grow: 1;`;
const ActionContainer = Styled.View`
    margin-top: auto;
    flex-grow: 1;
`;

interface Props {
    questionGroup: QuestionType;
    idx: number;
    currentIndex: number;
    lastQuestionRef: React.Ref<KeyboardAvoidingView>;
    next: (advance?: boolean, goTo?: UIDType) => void;
    disableAnalytics?: boolean;
    questions: QuestionsType;
}

export type QuestionProps = ActionType & {
    //answerKey: keyof AssessmentAnswers; // TODO Can we tie this up better with the question model
    answerKey?: string;
    questions: QuestionsType;
    currentQuestion: boolean;
    currentAnswers: AssessmentAnswers;
    setAnswered: (answered: boolean) => void;
    answered: boolean;
    uid: UIDType;
    next: (goTo?: UIDType) => void;
    isValid: boolean;
    setIsValid: (valid: boolean) => void;
    showValidation: boolean | string;
    setShowValidation: (message: string | boolean) => void;
    validationRequired: boolean;
    validate: React.MutableRefObject<() => Promise<void | boolean> | null>;
};

const Question = (props: Props) => {
    const { questionGroup, idx, currentIndex, lastQuestionRef, next, disableAnalytics } = props;
    const [keyboardHeight] = useKeyboard();
    const [store, dispatch] = useContext(StoreContext);
    const { assessment, user } = store;
    const { answers } = assessment;
    const { guide, path } = user as Patient;

    const currentQuestion = idx === currentIndex;
    // Set these true by default and change to false in the onMount
    // useEffect so we can get a correctly calculated content height
    const [showActions, setShowActions] = useState<boolean>(true);
    const [answered, setAnswered] = useState<boolean>(currentQuestion);
    const [startAnalyticRecorded, setStartAnalyticRecorded] = useState<boolean>(false);
    const [submissionInProgress, setSubmissionInProgress] = useState<boolean>(false);

    // Only supports one validation per question
    const [isValid, setIsValid] = useState(false);
    const [showValidation, setShowValidation] = useState<string | boolean>(false);
    const validate = useRef<() => Promise<void>>(null);

    const listActions = questionGroup.actions
        ? questionGroup.actions.filter<ListType>(
              (action: ActionType): action is ListType => action.type === 'list',
          )
        : [];

    // Checks if the question is the current question.  When editing a question that was previously
    // answered, we want to save the answer, but not advance the questions
    const checkNext = useCallback(
        (goTo?: UIDType) => {
            next(currentQuestion, goTo);
        },
        [currentQuestion, next],
    );

    let pathCode = 1;
    if (path?.csp && path?.srat) {
        pathCode = 3;
    } else if (path?.csp) {
        pathCode = 2;
    }

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
            setCurrentSectionUid(dispatch, questionGroup.uid);
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
        <Container
            minHeight={currentQuestion ? Dimensions.get('window').height - keyboardHeight - 100 : 0}
        >
            <QuestionContainer
                behavior={Platform.OS === 'ios' ? 'padding' : 'padding'}
                // @ts-ignore // TODO Fix KeyboardAvoidingView Ref typescript
                ref={currentQuestion ? lastQuestionRef : null}
            >
                <View>
                    {questionGroup?.guide?.map((message, i) => (
                        <InlineMessage
                            key={message}
                            message={message}
                            index={i}
                            currentQuestion={currentQuestion}
                        />
                    ))}
                    <ActionContainer>
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
                                    } else if (action.type === 'activate-account') {
                                        return (
                                            <AccountActivation
                                                key={`account-activation-${questionGroup.uid}`}
                                                {...action}
                                                isValid={isValid}
                                                setIsValid={setIsValid}
                                                showValidation={showValidation}
                                                setShowValidation={setShowValidation}
                                                answered={answered}
                                                validate={validate}
                                            />
                                        );
                                    } else if (action.type === 'activation-code') {
                                        return (
                                            <AccountCode
                                                key={`account-code-${questionGroup.uid}`}
                                                {...action}
                                                isValid={isValid}
                                                setIsValid={setIsValid}
                                                showValidation={showValidation}
                                                setShowValidation={setShowValidation}
                                                answered={answered}
                                                validate={validate}
                                            />
                                        );
                                    } else if (action.type === 'privacy-policy') {
                                        return (
                                            <PrivacyPolicy
                                                key={`privacy-policy-${questionGroup.uid}`}
                                                next={checkNext}
                                                currentQuestion={currentQuestion}
                                            />
                                        );
                                    } else if (action.type === 'set-password') {
                                        return (
                                            <SetPassword
                                                key={`account-code-${questionGroup.uid}`}
                                                {...action}
                                                isValid={isValid}
                                                setIsValid={setIsValid}
                                                showValidation={showValidation}
                                                setShowValidation={setShowValidation}
                                                answered={answered}
                                                validate={validate}
                                            />
                                        );
                                    } else if (action.type === 'request-permission') {
                                        return (
                                            <RequestPermission
                                                key={`request-permission-${questionGroup.uid}`}
                                                {...action}
                                            />
                                        );
                                    } else if (action.type === 'info-modal') {
                                        return (
                                            <InfoModal
                                                key={`info-modal-${questionGroup.uid}`}
                                                {...action}
                                            />
                                        );
                                    } else if (action.type === 'slideshow') {
                                        return (
                                            <Slideshow
                                                key={`slideshow-${questionGroup.uid}`}
                                                slides={action.slides}
                                                currentQuestion={currentQuestion}
                                                next={checkNext}
                                            />
                                        );
                                    } else if (action.type === 'homeButton') {
                                        return (
                                            <HomeButton key={`homebutton-${questionGroup.uid}`} />
                                        );
                                    }
                                    Sentry.Native.captureException(
                                        `Tried to render native question with unknown type ${action.type}`,
                                    );
                                    return null;
                                })}
                    </ActionContainer>
                </View>
            </QuestionContainer>
        </Container>
    );
};

export default Question;
