import { useContext } from 'react';
import { useHistory } from 'lib/router';
import { formatDate } from 'lib/helpers';
import StoreContext from 'state/context/store';
import styles from './index.module.scss';
import EditPatientIcon from 'assets/edit-patient.svg';

type PatientInfoProps = {
    id: number;
    firstName: string;
    lastName: string;
    dateOfBirth: string;
    mrn?: string;
    ssid?: string;
};

const PatientInfo = ({ id, firstName, lastName, mrn, ssid, dateOfBirth }: PatientInfoProps) => {
    const history = useHistory();
    const [store] = useContext(StoreContext);
    const { device } = store;
    const { inPatientContext } = device;

    return (
        <div className={styles.patientInfo}>
            <div className="typography--h4">
                {firstName} {lastName}
            </div>
            <div className={`typography--body3 ${styles.detail}`}>
                {ssid ? 'SSID' : 'MRN'}: {ssid || mrn} &#183; DOB: {formatDate(dateOfBirth)}
                {!inPatientContext && (
                    <img
                        style={{
                            marginLeft: 5,
                            cursor: 'pointer',
                        }}
                        tabIndex={0}
                        aria-label="Edit the patient"
                        onClick={() => history.push(`/technician/patients/${id}/edit`)}
                        onKeyDown={(e) => {
                            if (e.key === ' ' || e.key === 'Enter' || e.key === 'Spacebar') {
                                history.push(`/technician/patients/${id}/edit`);
                            }
                        }}
                        src={EditPatientIcon}
                        alt="Edit Patient"
                    />
                )}
            </div>
        </div>
    );
};

export default PatientInfo;
