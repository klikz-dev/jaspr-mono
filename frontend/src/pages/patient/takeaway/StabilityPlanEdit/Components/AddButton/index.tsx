import styles from './index.module.scss';

interface AddButtonProps {
    label?: string;
    onClick: () => void;
}

const AddButton = ({ label = 'Add another', onClick }: AddButtonProps) => {
    return (
        <div className={styles.addButton} onClick={onClick}>
            {label}
        </div>
    );
};

export default AddButton;
