import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Styled from 'styled-components/native';
import { SafeAreaView } from 'react-native';
import styles from './index.module.scss';
import Close from 'assets/close.svg';

const Container = Styled.View`
    flex-direction: column !important;
    align-items: center;
    justify-content: center;
    minHeight: 75px;
    padding: 10px;
    padding-right: 30px;
    background: #4b516a;
    border-bottom-width: 1px;
    border-bottom-color: white;
    color: white;
    text-align: center;
`;
const Closebutton = Styled.TouchableOpacity`${styles.dismiss}`;
const Title = Styled.Text`${styles.title}`;
const Description = Styled.Text`${styles.description}`;

const MaintenanceNotice = () => {
    const [show, setShow] = useState(false);
    const [notice, setNotice] = useState({ title: '', description: '' });

    const dismiss = () => {
        setShow(false);
    };

    useEffect(() => {
        axios.get('https://qa.app.jasprhealth.com/maintenance.json').then((response) => {
            const { data } = response;
            const { noticeStart, end } = data;
            if (new Date(noticeStart) < new Date() && new Date(end) > new Date()) {
                setNotice(data);
                setShow(true);
            }
        });
    }, []);

    return (
        <>
            {show && (
                <SafeAreaView style={{ backgroundColor: 'rgba(31, 33, 50, 1)' }}>
                    <Container>
                        <Closebutton onPress={dismiss}>
                            <Close />
                        </Closebutton>
                        <Title>{notice.title}</Title>
                        <Description>{notice.description}</Description>
                    </Container>
                </SafeAreaView>
            )}
        </>
    );
};

export default MaintenanceNotice;
