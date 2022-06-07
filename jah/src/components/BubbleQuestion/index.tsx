import React from 'react';
import Styled from 'styled-components/native';
import CustomBubble from './CustomBubble';

const Container = Styled.View`
    flex-direction: column;
    margin: 21px;
`;
const Title = Styled.Text`
    margin-bottom: 9px;
    font-size: 22px;
    line-height: 26px;
    letter-spacing: 0.165px;
    color: #FFFEFE;
`;
const Bubbles = Styled.View`
    flex-direction: row;
    flex-wrap: wrap;
`;
const Bubble = Styled.TouchableOpacity<{ checked: boolean }>`
    margin-vertical: 2px;
    margin-horizontal: 5.5px;
    align-items: center;
    justify-content: center;
    min-height: 34px;
    padding-left: 15px;
    padding-right: 15px;
    padding-top: 9px;
    padding-bottom: 9px;
    background-color: ${({ checked }) =>
        checked ? 'rgba(92, 101, 151, 1)' : 'rgba(255, 255, 255, 1)'}
    border-radius: 8px;
`;
const BubbleText = Styled.Text<{ checked: boolean }>`
    font-size: 14px;
    color: ${({ checked }) => (checked ? 'rgba(255, 255, 255, 1)' : 'rgba(73, 74, 75, 1)')}
`;

interface EditedAnswers {
    // TODO Crisis Stability Plan keys
    [answerKey: string]: string[];
}

interface BubbleQuestionProps {
    title: string;
    options: string[];
    answerKey: string; // TODO Crisis Stability Plan keys
    editedAnswers: EditedAnswers; // TODO Crisis Stability Plan keys
    setEditedAnswers: (
        // TODO Crisis Stability Plan keys
        editedAnswers: EditedAnswers | ((editedAnswers: EditedAnswers) => EditedAnswers),
    ) => void;
    allowCustom?: boolean;
}

const BubbleQuestion = ({
    title,
    options = [],
    answerKey,
    editedAnswers,
    setEditedAnswers,
    allowCustom = false,
}: BubbleQuestionProps) => {
    const toggleOption = (option: string) => {
        if (!editedAnswers[answerKey].includes(option)) {
            setEditedAnswers((answers) => ({
                ...answers,
                [answerKey]: [...answers[answerKey], option],
            }));
        } else {
            setEditedAnswers((answers) => ({
                ...answers,
                [answerKey]: answers[answerKey].filter((answer) => answer !== option),
            }));
        }
    };

    const addOption = (option: string) => {
        setEditedAnswers((answers) => ({
            ...answers,
            [answerKey]: [...answers[answerKey], option],
        }));
    };

    return (
        <Container>
            <Title>{title}</Title>
            <Bubbles>
                {options.map((option) => (
                    <Bubble
                        key={option}
                        checked={editedAnswers[answerKey].includes(option)}
                        onPress={() => toggleOption(option)}
                    >
                        <BubbleText checked={editedAnswers[answerKey].includes(option)}>
                            {option}
                        </BubbleText>
                    </Bubble>
                ))}
                {editedAnswers[answerKey]
                    .filter((answer) => !options.map((option) => option).includes(answer))
                    .map((option) => (
                        <Bubble checked key={option} onPress={() => toggleOption(option)}>
                            <BubbleText checked>{option}</BubbleText>
                        </Bubble>
                    ))}
                {allowCustom && (
                    <CustomBubble addOption={addOption} answer={editedAnswers[answerKey]} />
                )}
            </Bubbles>
        </Container>
    );
};

export default BubbleQuestion;
