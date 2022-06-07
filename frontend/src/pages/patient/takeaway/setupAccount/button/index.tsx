import styles from './index.module.scss';

interface ButtonProps {
    label: string;
    onClick: () => void;
    primary?: boolean;
}

const Button = ({ label, onClick, primary = true }: ButtonProps) => {
    return (
        <div className={`${styles.button} ${primary ? styles.primary : ''}`} onClick={onClick}>
            {label}
        </div>
    );
};

export default Button;
