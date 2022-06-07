import React, { useState } from 'react';
import Styled from 'styled-components/native';

const AddButton = Styled.TouchableOpacity`
    flex-direction: row;
    margin-vertical: 2px;
    margin-horizontal: 5.5px;
    align-items: center;
    justify-content: center;
    height: 34px;
    padding-left: 15px;
    padding-right: 15px;
    border-radius: 8px;
    background-color: rgba(255, 255, 255, 1);
`;
const AddButtonText = Styled.Text`
    font-size: 14px;
    line-height: 30px;
    letter-spacing: 0.875px;
    color: #179BB0;
`;
const AddButtonPlus = Styled.Text`
    margin-right: 5px;
    font-size: 30px;
    line-height: 30px;
    color: #179BB0;
`;
const Input = Styled.TextInput`
    height: 36px;
    margin-vertical: 2px;
    margin-horizontal: 5.5px;
    padding-left: 15px;
    padding-right: 15px;
    padding-top: 9px;
    padding-bottom: 9px;
    border-radius: 4px;
    font-size: 14px;
    color: rgba(255, 255, 255, 1);
    border-width: 1px;
    border-color: rgba(150, 151, 152, 1);
    background-color: rgba(120, 126, 142, 1);
`;

interface CustomBubbleProps {
    addOption: (option: string) => void;
    answer: string[];
}

const CustomBubble = ({ addOption, answer }: CustomBubbleProps) => {
    const [isEditing, setIsEditing] = useState(false);
    const [strategy, setStrategy] = useState('');

    const saveStrategy = () => {
        if (strategy !== '' && !answer.includes(strategy)) {
            addOption(strategy);
        }
        setIsEditing(false);
        setStrategy('');
    };

    if (isEditing) {
        return (
            <Input
                autoFocus
                value={strategy}
                onChangeText={(value) => setStrategy(value)}
                onBlur={saveStrategy}
                numberOfLines={1}
                returnKeyLabel="done"
                maxLength={10000}
                autoCompleteType="off"
                textContentType="none"
            />
        );
    }
    return (
        <AddButton onPress={() => setIsEditing(true)}>
            <AddButtonPlus>+</AddButtonPlus>
            <AddButtonText>Add custom</AddButtonText>
        </AddButton>
    );
};

export default CustomBubble;
