import { formatDateTime } from 'lib/helpers';
import styles from './index.module.scss';
import { AssessmentAnswers } from 'state/types';

interface PatientInfoHeaderType {
    // TODO MRN type Union SSID type
    dateOfBirth?: string;
    mrn?: string;
    ssid?: string;
    firstName?: string;
    lastName?: string;
    answers: AssessmentAnswers;
}

const PatientInfoHeader = ({
    dateOfBirth = '',
    mrn = '',
    ssid = '',
    firstName = '',
    lastName = '',
    answers = {},
}: PatientInfoHeaderType) => {
    const [birthYear, birthMonth, birthDay] = (dateOfBirth || '').split('-'); // TODO Sometimes null

    const { created, modified } = answers;

    return (
        <div className={styles.providerHeader}>
            <span style={{ flex: 2 }}>
                Name:{' '}
                <strong>
                    {lastName}
                    {firstName && lastName ? ', ' : ''}
                    {firstName}
                </strong>
            </span>
            <span>
                DOB: <strong>{dateOfBirth && `${birthMonth}/${birthDay}/${birthYear}`}</strong>
            </span>
            <span>
                ID:{' '}
                <strong>
                    {mrn && <span>{mrn} (MRN)</span>}
                    {!mrn && ssid && <span>{ssid} (SSID)</span>}
                </strong>
            </span>
            <span style={{ flex: 2, marginLeft: 'auto', textAlign: 'right' }}>
                Created: <strong>{formatDateTime(created)}</strong>
            </span>
            <span style={{ flex: 2, textAlign: 'right' }}>
                Last Modified: <strong>{formatDateTime(modified)}</strong>
            </span>
        </div>
    );
};

export { PatientInfoHeader };
export default PatientInfoHeader;
