import React from 'react';
import questions from './questions.json';
import Styled from 'styled-components/native';
import CUI from 'components/ConversationalUi';
import { Questions } from 'components/ConversationalUi/questions';

const Container = Styled.View`
    flex: 1;
`;

const ForgotPassword = () => {
    return (
        <Container>
            <CUI questions={questions as Questions} disableAnalytics backRoute="/" />
        </Container>
    );
};

export default ForgotPassword;
