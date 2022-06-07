import Button from 'components/Button';
import styles from './index.module.scss';

interface PatientActivationConfirmationProps {
    submit: () => void;
    cancel: () => void;
    location?: string;
    ssid?: string;
    firstName?: string;
    lastName?: string;
    dob?: string;
    mrn?: string;
    existingPatient?: boolean;
}

const PatientActivationConfirmation = ({
    submit,
    cancel,
    location,
    ssid,
    firstName,
    lastName,
    dob,
    mrn,
    existingPatient = false,
}: PatientActivationConfirmationProps) => {
    return (
        <div className={styles.outer}>
            <div className={styles.header}>
                {existingPatient ? 'Open Existing Patient' : 'Confirm New Patient'}
            </div>
            <table className={styles.confirmationTable}>
                <tbody>
                    <tr>
                        <td>Name of Patient</td>
                        <td>
                            {firstName} {lastName} {!firstName && !lastName && '-'}
                        </td>
                    </tr>
                    <tr>
                        <td>Date of Birth</td>
                        <td>{dob || '-'}</td>
                    </tr>
                    <tr>
                        <td>Medical Record Number</td>
                        <td>{mrn || '-'}</td>
                    </tr>
                    <tr>
                        <td>SSID</td>
                        <td>{ssid ? ssid : '-'}</td>
                    </tr>
                    <tr>
                        <td>Clinic Location</td>
                        <td>{location || '-'}</td>
                    </tr>
                </tbody>
            </table>
            <div className={styles.buttons}>
                <Button onClick={cancel} variant="secondary">
                    Cancel
                </Button>
                <Button onClick={submit}>Begin Session</Button>
            </div>
        </div>
    );
};

export default PatientActivationConfirmation;
