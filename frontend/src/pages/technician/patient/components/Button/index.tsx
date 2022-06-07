import styles from './index.module.scss';

interface ButtonProps {
    secondary?: boolean;
    label: string;
    onClick?: () => void;
    disabled?: boolean;
    icon?: string;
}

const Button = ({
    secondary = false,
    label,
    onClick = () => {},
    disabled = false,
    icon,
}: ButtonProps) => {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`${styles.button} ${secondary ? styles.secondary : styles.primary}`}
        >
            {icon && <img className={styles.icon} src={icon} alt="" />}
            {label}
        </button>
    );
};

export default Button;
