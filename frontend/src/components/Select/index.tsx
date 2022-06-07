import Dropdown, { Option } from 'react-dropdown';
import styles from './index.module.scss';

interface SelectLocationProps {
    placeholder?: string;
    onChange: (option: Option) => void;
    mode?: 'light' | 'dark';
    value: Option;
    options: Option[];
}

const SelectLocation = (props: SelectLocationProps) => {
    const { placeholder, value, mode, onChange, options } = props;

    return (
        <Dropdown
            className={`${styles.select} ${mode === 'light' ? styles.light : 'dark'}`}
            controlClassName={styles.control}
            placeholderClassName={styles.placeholder}
            arrowClassName={styles.arrow}
            menuClassName={styles.menu}
            placeholder={placeholder || ''}
            value={value}
            onChange={onChange}
            options={options}
        />
    );
};

export { SelectLocation };
export default SelectLocation;
