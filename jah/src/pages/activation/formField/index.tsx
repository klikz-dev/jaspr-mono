import React from 'react';
import { NativeSyntheticEvent, TextInputChangeEventData } from 'react-native';
import Styled from 'styled-components/native';
import styles from './index.module.scss';

type Props = {
    label: string;
    note?: string;
    onChange: (event: NativeSyntheticEvent<TextInputChangeEventData>) => void;
    disabled?: boolean;
    value: string;
};

const Label = Styled.View`${styles.label}`;
const Note = Styled.Text`${styles.note}`;
const LabelText = Styled.Text`${styles.labelText}`;
const Input = Styled.TextInput`${styles.input}`;

const FormField = (props: Props) => {
    const { label, note, onChange, disabled = false, value } = props;

    return (
        <Label>
            <LabelText>{label} </LabelText>
            <Note>{note}</Note>
            <Input value={value} onChange={onChange} editable={disabled} />
        </Label>
    );
};

export default FormField;
