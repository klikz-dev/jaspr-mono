import React from 'react';
import Styled from 'styled-components/native';

const StyledButton = Styled.TouchableOpacity`
    display: flex;
    height: 44px;
    color: #fff;
    fontSize: 16px;
    alignItems: center;
    justifyContent: center;
    margin: 10px 21px;
`;
const Text = Styled.Text``;

interface ButtonProps {
    onClick: () => void;
    label: string;
    primary?: boolean;
}

const Button = ({ onClick, label, primary = true }: ButtonProps) => {
    return (
        <StyledButton
            style={{
                backgroundColor: primary ? '#69BCD2' : '#fff',
                borderColor: primary ? 'transparent' : '#69BCD2',
                borderWidth: primary ? 0 : 1,
            }}
            onPress={onClick}
        >
            <Text style={{ color: primary ? '#fff' : '#69BCD2' }}>{label}</Text>
        </StyledButton>
    );
};

export default Button;
