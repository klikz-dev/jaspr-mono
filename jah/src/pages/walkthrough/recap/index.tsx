import React, { useEffect } from 'react';
import { Platform } from 'react-native';
import { addAction, actionNames } from 'state/actions/analytics';
import Styled from 'styled-components/native';

const Container = Styled.View<{ isIOS: boolean }>`
    flex: 1;
    ${({ isIOS }) =>
        isIOS
            ? `
    shadow-color: #000;
    shadow-offset: 2px 4px;
    shadowOpacity: 0.5;
    shadowRadius: 10px;
    `
            : `
    elevation: 7;
    `}
`;
const Top = Styled.View`
    flex: 1;
    width: 100%;
    padding-top: 50px;
    max-height: 225px;
    height: 100%;
    align-items: center;
    background-color: #2F344F;
`;
const Title = Styled.Text`
    padding-horizontal: 32px;
    color: #ffffff;
    font-size: 36px;
    line-height: 43px;
    text-align: center;
`;
/*const TheWhy = Styled.Text`
    margin-top: 10px;
    color: #6CC5D4;
    font-size: 16px;
    font-style: italic;
    font-weight: 300;
    line-height: 19px;
`;*/
const ScrollView = Styled.ScrollView`
    flex: 1;
    background-color: #2F344F;
`;
const Close = Styled.TouchableOpacity`
    position: absolute;
    top: 10px;
    right: 20px;
`;
const CloseText = Styled.Text`
    color: #ffffff;
    font-size: 30px;
    font-weight: bold;
`;
const StepContainer = Styled.View`
    border-top-width: 1px;
    border-top-color: #5c6597; 
    height: 50px;
`;
const TouchableOpacity = Styled.TouchableOpacity`
    flex: 1;
    justify-content: center;
`;
const StepText = Styled.Text`
    margin-horizontal: 13px;
    color: #FFFFFF;
    font-size: 16px;
    letter-spacing: 0.02px;
`;

interface RecapProps {
    close?: () => void;
    steps: string[];
    setStepIdx?: (idx: number) => void;
}

const Recap = ({ close, steps, setStepIdx }: RecapProps) => {
    useEffect(() => {
        addAction(actionNames.JAH_WALKTHROUGH_ARRIVE_RECAP);
    }, []);

    return (
        <Container isIOS={Platform.OS === 'ios'}>
            <Top>
                {Boolean(close) && (
                    <Close onPress={close}>
                        <CloseText>✕</CloseText>
                    </Close>
                )}
                <Title>Distress{'\n'}Survival Guide</Title>
                {/*<TheWhy>The why behind this ›</TheWhy>*/}
            </Top>
            <ScrollView>
                {steps.map((step, idx) => (
                    <StepContainer key={`${step}-${idx}`}>
                        <TouchableOpacity
                            disabled={!Boolean(setStepIdx)}
                            onPress={
                                setStepIdx
                                    ? () => {
                                          setStepIdx(idx);
                                          close();
                                      }
                                    : () => {}
                            }
                        >
                            <StepText numberOfLines={1}>{step}</StepText>
                        </TouchableOpacity>
                    </StepContainer>
                ))}
            </ScrollView>
        </Container>
    );
};

export default Recap;
