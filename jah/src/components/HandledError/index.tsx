import React, { useContext } from 'react';
import StoreContext from 'state/context/store';
import { dismissError } from 'state/actions/error';
import { Modal } from 'react-native';
import Styled from 'styled-components/native';
import Chat from 'pages/walkthrough/guide/chat';
import styles from './index.module.scss';

const Container = Styled.View`${styles.container}`;
const Button = Styled.TouchableOpacity`${styles.button}`;
const ButtonText = Styled.Text`${styles.buttonText}`;

const HandledError = () => {
    const [store] = useContext(StoreContext);
    const { error } = store;
    const { showError } = error;

    return (
        <Modal
            visible={showError}
            animationType="slide"
            supportedOrientations={['portrait', 'landscape']}
        >
            <Container>
                <Chat value="Oops, something went wrong. Try again." />
                <Button onPress={dismissError}>
                    <ButtonText>Close</ButtonText>
                </Button>
            </Container>
        </Modal>
    );
};

export default HandledError;
