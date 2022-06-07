import React from 'react';
import Styled from 'styled-components/native';

const Container = Styled.View`
    flex-direction: row;
    align-items: center;
    padding-horizontal: 14px;
    padding-vertical: 8px;
    background-color: #5C6597;
    border-radius: 8px;
    margin-right: 12px;
    margin-bottom: 10px;
`;
const Label = Styled.Text`
    flex-wrap: wrap;
    color: #FFFEFE;
    font-size: 18px;
    letter-spacing: 0.14px;
    line-height: 23px;
`;
const Dot = Styled.View`
    width: 9px;
    height: 9px;
    margin-top: 2px;
    margin-left: 5px;
    border-radius: 4.5px;
    background-color: #DC6130;
`;

interface StabilityItemProps {
    label: string;
    showDot?: boolean;
}

const StabilityItem = ({ label, showDot = false }: StabilityItemProps): JSX.Element => {
    return (
        <Container>
            <Label>{label}</Label>
            {showDot && <Dot />}
        </Container>
    );
};

export default StabilityItem;
