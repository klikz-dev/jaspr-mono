import React, { Component } from 'react';
import Styled from 'styled-components/native';
import * as Sentry from 'sentry-expo';
import { reloadAsync } from 'expo-updates';
import styles from './index.module.scss';

const Container = Styled.View`${styles.container}`;
const Alert = Styled.View`${styles.alert}`;
const Message = Styled.Text`${styles.message}`;
const Button = Styled.TouchableOpacity`${styles.button}`;
const ButtonText = Styled.Text`${styles.buttonText}`;

interface Props {
    children: React.ReactNode;
}

interface State {
    hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error) {
        // Update state so the next render will show the fallback UI.
        return { hasError: true };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        console.error(error, errorInfo);
        Sentry.Native.captureException(error);
    }

    async restart(): Promise<void> {
        await reloadAsync();
    }

    render() {
        const { children } = this.props;
        const { hasError } = this.state;

        if (hasError) {
            return (
                <Container>
                    <Alert>
                        <Message>Something went wrong, we’ll need to restart the app.</Message>
                        <Button onPress={this.restart}>
                            <ButtonText>Restart</ButtonText>
                        </Button>
                    </Alert>
                </Container>
            );
        }

        return children;
    }
}

export default ErrorBoundary;
