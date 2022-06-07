import React from 'react';
import Styled from 'styled-components/native';
import CUI from 'components/ConversationalUi';
import questions from './questions.json';
import { Questions } from 'components/ConversationalUi/questions';

const Container = Styled.View`
    flex: 1;
`;
const Onboarding = () => {
    return (
        <Container>
            <CUI questions={questions as Questions} />
        </Container>
    );
};

export default Onboarding;
