import { useContext, useState } from 'react';
import StoreContext from 'state/context/store';
import { activatePatient } from 'state/actions/user';
import { useHistory } from 'lib/router';
import Button from 'components/Button';
import styles from './index.module.scss';
import Segment, { AnalyticNames } from 'lib/segment';

interface PatientActivationProps {
    id: number;
    department: number;
    ssid?: string;
    firstName?: string;
    lastName?: string;
    dob?: string;
    mrn?: string;
    firstActivation?: boolean;
    allowActivationMethodChange: boolean;
    setActivationMethod: (activationMethod: 'direct' | 'pin') => void;
}

const PatientActivation = ({
    id,
    department,
    ssid,
    firstName,
    lastName,
    dob,
    mrn,
    firstActivation,
    allowActivationMethodChange,
    setActivationMethod,
}: PatientActivationProps) => {
    const history = useHistory();
    const [, dispatch] = useContext(StoreContext);
    const [showConfirm, setShowConfirm] = useState(false);
    const close = () => history.replace('/technician/patients');

    const confirm = () => {
        setShowConfirm(true);
    };

    const start = () => {
        // Sets location
        activatePatient(dispatch, { patient: id, department }, firstActivation);
    };

    return (
        <div className={styles.outer}>
            {!showConfirm && <div className={styles.header}>Confirm Patient Identity</div>}
            <div className={styles.close} onClick={close}>
                ⨉
            </div>
            {!showConfirm && (
                <>
                    <div className={styles.details}>
                        {!Boolean(ssid) && (
                            <>
                                <div className={styles.row}>
                                    <div className={styles.field}>Name</div>
                                    <div className={styles.value}>
                                        {firstName} {lastName} {!firstName && !lastName && '-'}
                                    </div>
                                </div>
                                <div className={styles.row}>
                                    <div className={styles.field}>DOB</div>
                                    <div className={styles.value}>{dob || '-'}</div>
                                </div>
                                <div className={styles.row}>
                                    <div className={styles.field}>MRN</div>
                                    <div className={styles.value}>{mrn || '-'}</div>
                                </div>
                            </>
                        )}

                        {Boolean(ssid) && (
                            <div className={styles.row}>
                                <div className={styles.field}>SSID</div>
                                <div className={styles.value}>{ssid ? ssid : '-'}</div>
                            </div>
                        )}
                    </div>
                    <div className={styles.deviceInstructions}>How will the patient use Jaspr?</div>
                    <div className={styles.buttons}>
                        {allowActivationMethodChange && (
                            <Button
                                variant="tertiary"
                                onClick={() => {
                                    Segment.track(
                                        AnalyticNames.TECHNICIAN_CHANGED_ACTIVATION_METHOD,
                                        {
                                            method: 'pin',
                                        },
                                    );
                                    setActivationMethod('pin');
                                }}
                            >
                                On Another Device
                            </Button>
                        )}
                        <Button dark onClick={confirm}>
                            On This Device
                        </Button>
                    </div>
                </>
            )}
            {showConfirm && (
                <>
                    <div className={styles.buttons} style={{ marginTop: '4rem' }}>
                        <Button dark onClick={start}>
                            Start Patient Session
                        </Button>
                    </div>
                    <div className={styles.warning}>
                        <span className={styles.important}>IMPORTANT</span>
                        <span>
                            Start session before handing <br />
                            tablet to patient.
                        </span>
                    </div>
                </>
            )}
        </div>
    );
};

export default PatientActivation;
