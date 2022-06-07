import React, { useContext, useEffect, useState } from 'react';
import template from 'lodash/template';
import StoreContext from 'state/context/store';
import Styled from 'styled-components/native';
import Loading from '../loading';
import styles from './index.module.scss';
import jazIcon from 'assets/jazz.png';
import jasperIcon from 'assets/jasper.png';
import defaultIcon from 'assets/defaultChatIcon.png';
import { Patient } from 'state/types';

const Container = Styled.View`${styles.container}
    align-items: flex-start;
    margin-top: 38px;
    margin-left: 18px;
    margin-right: 18px;
`;
const GuideImage = Styled.Image`${styles.guide}`;
const MessageContainer = Styled.View`flex: 1;`;
const Message = Styled.Text`
    ${styles.message}
    flex-wrap: wrap;
    flex-shrink: 1;
    margin-left: 10px;
`;

const Triangle = Styled.View`
    position: absolute;
    top: 5px;
    width: 0;
    height: 0;
    background-color: transparent;
    border-style: solid;
    border-top-width: 12px;
    border-right-width: 12px;
    border-bottom-width: 12px;
    border-left-width: 0px;
    border-top-color: transparent;
    border-right-color: #ffffff;
    border-bottom-color: transparent;
    border-left-color: transparent;
`;

interface MessageQuestionProps {
    currentQuestion: boolean;
    message: string;
    index: number;
}

const MessageQuestion = (props: MessageQuestionProps): JSX.Element => {
    const { currentQuestion, index, message } = props;
    const [store] = useContext(StoreContext);
    const { user } = store;
    const { guide } = user as Patient;
    // Set these false by default and change to true in the onMount
    // useEffect so we can get a correctly calculated content height
    const [isHidden, setIsHidden] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    let templatedMessage = message;
    try {
        templatedMessage = template(message)({ guide });
    } catch {
        templatedMessage = message;
    }

    let chatIcon = defaultIcon;
    if (guide === 'Jaz') {
        chatIcon = jazIcon;
    } else if (guide === 'Jasper') {
        chatIcon = jasperIcon;
    }

    useEffect(() => {
        // Set these here, instead of as default values so final view size can be calculated with useLayoutEffect
        if (currentQuestion) {
            setIsHidden(true);
            setIsLoading(true);
            const loadingTimer = setTimeout(() => {
                setIsLoading(false);
            }, (index + 1) * 1500);
            const hiddenTimer = setTimeout(() => setIsHidden(false), index * 1500);
            return () => {
                clearTimeout(hiddenTimer);
                clearTimeout(loadingTimer);
            };
        } else {
            setIsHidden(false);
            setIsLoading(false);
        }
    }, [index, currentQuestion]);

    return (
        <>
            {!isHidden && isLoading && <Loading />}
            {!isHidden && !isLoading && (
                <Container>
                    <GuideImage style={{ opacity: index === 0 ? 1 : 0 }} source={chatIcon} />

                    <MessageContainer>
                        {index === 0 && <Triangle />}
                        <Message>{templatedMessage}</Message>
                    </MessageContainer>
                </Container>
            )}
        </>
    );
};

export default MessageQuestion;
