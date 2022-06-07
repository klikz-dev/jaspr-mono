import React, { useCallback, useContext, useEffect, useRef, useState } from 'react';
import { ScrollView, KeyboardAvoidingView, SafeAreaView } from 'react-native';
import StoreContext from 'state/context/store';
import Styled from 'styled-components/native';
import styles from './index.module.scss';
import Question from './question';
import { useKeyboard } from 'lib/useKeyboard';
import { useHistory } from 'lib/router';

const Container = Styled.ScrollView`${styles.container}`;
const Survey = Styled.View` ${styles.survey}
    padding-top: 0px;
    padding-bottom: 0px;
`;
const BackButton = Styled.TouchableOpacity`
    background-color: #eceef5;
    padding-left: 20px;
    padding-top: 10px;
    padding-bottom: 10px;
`;
const BackButtonText = Styled.Text`
    color: rgba(62,65,79,1);
    font-size: 16px;
    font-weight: 600;
    letter-spacing: -0.2px;
`;
const KeyboardBuffer = Styled.View`
    display: flex;
    height: ${({ keyboardHeight }: { keyboardHeight: number }) =>
        keyboardHeight ? keyboardHeight : 0};
    flex-grow: 0;
    flex-shrink: 0;
`;
import { Questions as QuestionsType, UIDType } from './questions';
import { Patient } from 'state/types';

interface Props {
    backRoute?: string;
    disableAnalytics?: boolean;
    questions: QuestionsType;
    firstQuestionUID?: UIDType;
    onIndexChange?: (index: number) => void;
}

const Questions = (props: Props) => {
    const history = useHistory();
    const [keyboardHeight] = useKeyboard();
    const {
        backRoute,
        disableAnalytics = false,
        firstQuestionUID,
        questions,
        onIndexChange,
    } = props;
    const [store] = useContext(StoreContext);
    const [assessmentResumptionCheck, setAssessmentResumptionCheck] = useState(false);
    const { assessment, user } = store;
    const { online } = user as Patient;
    const { currentSectionUid } = assessment;
    const [showOfflineModal, setShowOfflineModal] = useState(false);
    const containerRef = useRef<ScrollView>(null!); // TODO ScrollView in Native
    const surveyRef = useRef(null);
    const lastQuestionRef = useRef<KeyboardAvoidingView>(null); // TODO KeyboardAvoidingView in native
    const questionsRef = useRef([]);
    const prevIndex = useRef<number | null>(0);
    const [currentIndex, setCurrentIndex] = useState(0);

    questionsRef.current = questions.filter(
        (question) =>
            !question.actions.some((action) =>
                ['section-change', 'progress-bar'].includes(action.type),
            ),
    );

    const numberOfQuestions = questionsRef.current.length;

    useEffect(() => {
        if (onIndexChange) {
            onIndexChange(currentIndex);
        }
    }, [onIndexChange, currentIndex]);

    useEffect(() => {
        setShowOfflineModal(online === false);
    }, [online]);

    const goToQuestion = useCallback((sectionUid) => {
        const idx = questionsRef.current.findIndex((question) => question.uid === sectionUid);
        if (idx > 0 && idx < questionsRef.current.length) {
            // Yes, I mean 0 and not -1.  If it's 0, we are already on the right page
            setCurrentIndex(idx);
        }
    }, []);

    useEffect(() => {
        if (numberOfQuestions > 0) {
            const skipAhead = prevIndex.current !== currentIndex - 1;
            // const surveyViewPortHeight = containerRef.current.offsetHeight - 40;
            // const lastQuestionHeight = lastQuestionRef.current.offsetHeight;
            prevIndex.current = currentIndex;

            if (lastQuestionRef.current) {
                // Push to the end of the stack.  Without the timeout
                // closing the tutorial menu prevents scrolling to the bottom
                const timeout = setTimeout(() => containerRef.current.scrollToEnd(), 1);
                return () => clearTimeout(timeout);
            }
        }
    }, [currentIndex, numberOfQuestions]);

    useEffect(() => {
        if (
            numberOfQuestions > 0 &&
            firstQuestionUID &&
            !assessmentResumptionCheck &&
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
        questions.length,
        numberOfQuestions,
    ]);

    const next = (advance = true, goTo: UIDType): void => {
        if (currentIndex < questionsRef.current.length - 1 && advance) {
            if (goTo) {
                const idx = questionsRef.current.findIndex((question) => question.uid === goTo);
                if (idx > -1) {
                    setCurrentIndex(idx);
                } else {
                    setCurrentIndex(currentIndex + 1);
                }
            } else {
                setCurrentIndex(currentIndex + 1);
            }
        }
    };

    return (
        <>
            {Boolean(backRoute) && (
                <SafeAreaView>
                    <BackButton onPress={() => history.push(backRoute)}>
                        <BackButtonText>‹ Back</BackButtonText>
                    </BackButton>
                </SafeAreaView>
            )}
            {/* @ts-ignore */}
            <Container ref={containerRef}>
                <Survey ref={surveyRef}>
                    {questions
                        .filter((val, idx) => idx <= currentIndex)
                        .map((questionGroup, idx) => {
                            return (
                                <Question
                                    key={`${questionGroup.uid}-${idx}`}
                                    questionGroup={questionGroup}
                                    idx={idx}
                                    currentIndex={currentIndex}
                                    lastQuestionRef={lastQuestionRef}
                                    next={next}
                                    disableAnalytics={disableAnalytics}
                                    questions={questions}
                                />
                            );
                        })}
                </Survey>
                <KeyboardBuffer keyboardHeight={keyboardHeight} />
            </Container>
        </>
    );
};

export default Questions;
