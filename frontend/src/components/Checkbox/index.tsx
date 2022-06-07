import React from 'react';
import styles from './index.module.scss';

interface CheckboxProps {
    label?: string;
    sublabel?: string;
    checked?: boolean;
    onChange?: (value: any) => void;
    disabled?: boolean;
    labelStyle?: React.CSSProperties;
    large?: boolean;
}

const Checkbox = ({
    label = '',
    sublabel = '',
    checked = false,
    onChange = () => {},
    disabled = false,
    labelStyle = {},
    large = false,
}: CheckboxProps) => {
    return (
        <label className={styles.checkbox}>
            <input type="checkbox" checked={checked} onChange={onChange} disabled={disabled} />
            <span className={`${styles.check} ${large ? styles.large : ''}`} />
            <div className={styles.labels}>
                {Boolean(label) && (
                    <span className={styles.label} style={labelStyle}>
                        {label}
                    </span>
                )}
                {Boolean(sublabel) && <span>{sublabel}</span>}
            </div>
        </label>
    );
};
export { Checkbox };
export default Checkbox;
