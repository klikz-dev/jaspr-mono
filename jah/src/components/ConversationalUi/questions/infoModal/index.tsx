import React, { useState } from 'react';
import { Modal } from 'react-native';
import InfoModal from 'components/InfoModal';
import Styled from 'styled-components/native';

const Button = Styled.TouchableOpacity`
    margin-top: 40px;
    margin-bottom: 20px;
`;
const ButtonText = Styled.Text`
    color: #3E414F;
    font-size: 20px;
    font-weight: 600;
    letter-spacing: -0.25px;
    line-height: 25px;
    text-align: center;
`;

interface InfoModalProps {
    title: string;
    content: { header: string; body: string }[];
}

const InfoModalQuestion = (props: InfoModalProps): JSX.Element => {
    const { title, content } = props;
    const [showModal, setShowModal] = useState(false);

    return (
        <>
            <Button onPress={() => setShowModal(true)}>
                <ButtonText>{title}</ButtonText>
            </Button>
            <Modal visible={showModal} animationType="fade" transparent={true}>
                <InfoModal title={title} content={content} close={() => setShowModal(false)} />
            </Modal>
        </>
    );
};

export default InfoModalQuestion;
