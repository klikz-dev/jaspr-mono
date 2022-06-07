import Button from 'components/Button';
import styles from './index.module.scss';

interface ConfirmationProps {
    submit: () => void;
    cancel: () => void;
    location: string;
    ssid?: string;
    firstName?: string;
    lastName?: string;
    dob?: string;
    mrn?: string;
    edit?: boolean;
}

const Confirmation = ({
    submit,
    cancel,
    location,
    ssid,
    firstName,
    lastName,
    dob,
    mrn,
    edit = false,
}: ConfirmationProps) => {
    return (
        <div className={styles.outer}>
            <div className={styles.header}>
                Review {edit ? 'Updated' : 'New'} Patient Information
            </div>
            <div className={styles.close} onClick={cancel}>
                ⨉
            </div>
            <div className={styles.container}>
                <div className={styles.row}>
                    <label className={styles.label}>
                        <span className={styles.formLabel}>Name of Patient</span>
                        <span className={styles.value}>
                            {firstName} {lastName} {!firstName && !lastName && '-'}
                        </span>
                    </label>

                    <label className={styles.label}>
                        <span className={styles.formLabel}>Clinic Location</span>
                        <span className={styles.value}>{location || '-'}</span>
                    </label>
                </div>

                <div className={styles.row}>
                    <label className={styles.label}>
                        <span className={styles.formLabel}>Date of Birth</span>
                        <span className={styles.value}>{dob || '-'}</span>
                    </label>

                    <label className={styles.label}>
                        <span className={styles.formLabel}>Medical Record Number</span>
                        <span className={styles.value}>{mrn || '-'}</span>
                    </label>

                    <label className={styles.label}>
                        <span className={styles.formLabel}>SSID</span>
                        <span className={styles.value}>{ssid ? ssid : '-'}</span>
                    </label>
                </div>
            </div>

            <div className={styles.buttons}>
                <div className={styles.edit} onClick={cancel}>
                    Edit
                </div>
                <Button dark onClick={submit}>
                    Confirm
                </Button>
            </div>
        </div>
    );
};

export default Confirmation;
