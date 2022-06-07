import { useState } from 'react';
import Button from 'components/Button';
import styles from './index.module.scss';

interface ConfirmationMoveProps {
    submit: () => void;
    cancel: () => void;
    from: string;
    to: string;
    ssid?: string;
    firstName?: string;
    lastName?: string;
    mrn?: string;
}

const ConfirmationMove = ({
    submit,
    cancel,
    from,
    to,
    firstName,
    lastName,
    mrn,
    ssid,
}: ConfirmationMoveProps) => {
    const [authorized, setAuthorized] = useState(false);

    return (
        <div className={styles.outer}>
            <div className={styles.header}></div>
            <div className={styles.container}>
                <div className={`${styles.row} ${styles.title}`}>
                    Confirm Clinic Location transfer for{' '}
                    <strong style={{ display: 'inline-flex' }}>
                        {firstName} {lastName}, {mrn || ssid}
                    </strong>
                </div>
                <div className={styles.locations}>
                    <div className={styles.location}>
                        <span>From</span> <strong>{from}</strong>
                    </div>
                    <div className={styles.location}>
                        <span>To</span> <strong>{to}</strong>
                    </div>
                </div>
                <div className={styles.row}></div>
                <label className={styles.row}>
                    <input
                        className={styles.checkbox}
                        type="checkbox"
                        checked={authorized}
                        onChange={() => setAuthorized((authorized) => !authorized)}
                    />
                    I am authorized to share this patient information for continuity of care.
                </label>
            </div>

            <div className={styles.buttons}>
                <Button onClick={cancel} variant="secondary">
                    Discard Changes
                </Button>
                <Button onClick={submit} disabled={!authorized}>
                    Confirm
                </Button>
            </div>
        </div>
    );
};

export default ConfirmationMove;
