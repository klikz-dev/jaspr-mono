import React from 'react';
import styles from './index.module.scss';

type Props = {
    label: string;
    note?: string;
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    type?: string;
    disabled?: boolean;
    value: string;
    autoComplete?: HTMLInputElement['autocomplete'];
};

const FormField = (props: Props) => {
    const {
        label,
        note,
        onChange,
        type = 'text',
        disabled = false,
        value,
        autoComplete = 'off',
    } = props;

    return (
        <label className={styles.label}>
            <span className={styles.labelText}>{label} </span>
            <span className={styles.note} style={{ lineHeight: '18px' }}>
                {note}
            </span>
            <input
                type={type}
                onChange={onChange}
                autoComplete={autoComplete}
                disabled={disabled}
                value={value}
                className={styles.input}
            />
        </label>
    );
};

export default FormField;
