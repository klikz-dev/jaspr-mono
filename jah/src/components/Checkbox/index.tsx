import React from 'react';
import Styled from 'styled-components/native';
import CheckIcon from './checkmark.svg';

interface CheckboxProps {
    label?: string;
    checked?: boolean;
    onChange?: (value: any) => void;
    disabled?: boolean;
    labelStyle: React.CSSProperties;
}

const Container = Styled.TouchableOpacity`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
`;
const Input = Styled.View`
    width: 21px;
    height: 21px;
    background-color: #179bb0;
    border-radius: 3px;
`;
const Label = Styled.Text`
    margin-left: 10px;
`;

const Checkbox = ({
    label = '',
    labelStyle = {},
    checked = false,
    onChange = () => {},
    disabled = false,
}: CheckboxProps) => (
    <Container onPress={disabled ? () => null : () => onChange(!checked)}>
        <Input>
            {checked && (
                <CheckIcon
                    width={12}
                    height={16}
                    style={{ position: 'absolute', left: 5, top: 2.5 }}
                />
            )}
        </Input>
        {/* @ts-ignore */}
        <Label style={labelStyle}>{label}</Label>
    </Container>
);

export default Checkbox;
