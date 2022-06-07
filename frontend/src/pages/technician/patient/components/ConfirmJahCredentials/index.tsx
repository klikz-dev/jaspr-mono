import { useState } from 'react';
import Button from 'components/Button';
import Checkbox from 'components/Checkbox';
import styles from './index.module.scss';

interface ConfirmationJAHCredentialsProps {
    submit: () => void;
    cancel: () => void;
    firstName?: string;
    lastName?: string;
    mrn?: string;
    ssid?: string;
    email: string;
    mobilePhone: string;
}

const ConfirmationJAHCredentials = ({
    submit,
    cancel,
    firstName,
    lastName,
    mrn,
    ssid,
    email,
    mobilePhone,
}: ConfirmationJAHCredentialsProps) => {
    const [confirmed, setConfirmed] = useState(false);

    return (
        <div className={styles.outer}>
            <div className={styles.header}></div>
            <div className={styles.container}>
                <div className={`${styles.row} ${styles.title}`}>
                    Confirm Jaspr at Home credentials for{' '}
                    <strong style={{ display: 'inline' }}>
                        {firstName ? firstName : ''} {lastName ? lastName : ''}
                        {firstName || lastName ? ',' : ' '} {mrn || ssid}
                    </strong>
                </div>
                <div className={styles.credentials}>
                    <div className={styles.credential}>
                        <span>Email</span> <strong>{email}</strong>
                    </div>
                    <div className={styles.credential}>
                        <span>Phone</span> <strong>{mobilePhone}</strong>
                    </div>
                </div>
                <div className={styles.row}></div>
                <label className={styles.row}>
                    <Checkbox
                        checked={confirmed}
                        onChange={() => setConfirmed((confirmed) => !confirmed)}
                        label="I confirm that the submitted email and phone number are correct for the listed
                        patient."
                    />
                </label>
            </div>

            <div className={styles.buttons}>
                <Button onClick={cancel} variant="secondary">
                    Discard Changes
                </Button>
                <Button onClick={submit} disabled={!confirmed}>
                    Confirm
                </Button>
            </div>
        </div>
    );
};

export default ConfirmationJAHCredentials;
