import React from 'react';
import { StyleProp, ViewStyle } from 'react-native';
import Styled, { ThemeProvider } from 'styled-components/native';
import { ViewProps } from '.';
import styles from './styles';

const StyledButton = Styled.TouchableOpacity`
    ${styles.button}
    ${({ secondary }: { secondary: boolean }) => (secondary ? styles.secondary : styles.primary)}
`;

const StyledText = Styled.Text`
    ${styles.text}
`;

const View = ({
    secondary = false,
    onClick,
    style,
    label,
    theme,
    disabled = false,
}: ViewProps & { style: StyleProp<ViewStyle> }) => {
    return (
        <ThemeProvider theme={theme}>
            <StyledButton
                secondary={secondary}
                onPress={onClick}
                disabled={disabled}
                // TODO Fixme
                style={(style ? style : {}) as any}
            >
                <StyledText>{label}</StyledText>
            </StyledButton>
        </ThemeProvider>
    );
};

export default View;
