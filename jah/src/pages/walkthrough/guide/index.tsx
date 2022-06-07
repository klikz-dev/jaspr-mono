import React from 'react';
import Styled from 'styled-components/native';
import Chat from './chat';

const Container = Styled.View`
    position: relative;
    overflow: hidden;
    flex: 1;
    width: 100%;
    background-color: #2F344F;
    border-top-left-radius: 30px;
    border-top-right-radius: 30px;
`;

interface GuideProps {
    value: string;
}

const Guide = ({ value }: GuideProps) => {
    return (
        <Container>
            <Chat value={value} />
        </Container>
    );
};

export default Guide;
