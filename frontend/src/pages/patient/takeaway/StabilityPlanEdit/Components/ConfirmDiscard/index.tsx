import styles from './index.module.scss';

interface ConfirmDiscardProps {
    cancel: () => void;
    confirm: () => void;
}

const ConfirmDiscard = ({ cancel, confirm }: ConfirmDiscardProps) => {
    return (
        <>
            <div className={styles.text}>Are you sure you want to discard changes?</div>
            <div className={styles.buttons}>
                <div className={styles.button} onClick={cancel}>
                    Cancel
                </div>
                <div className={`${styles.button} ${styles.discard}`} onClick={confirm}>
                    Discard Changes
                </div>
            </div>
        </>
    );
};

export default ConfirmDiscard;
