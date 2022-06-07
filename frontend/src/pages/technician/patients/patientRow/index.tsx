import { useHistory } from 'lib/router';
import Button from 'components/Button';
import PatientInfo from '../../patient/components/PatientInfo';
import styles from './index.module.scss';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';
import Arrow from 'assets/icons/Arrow';

const PatientRow = ({
    patient,
    setShowNewEncounter,
}: {
    patient: PatientGetResponse;
    setShowNewEncounter: (showNewEncounter: false | number) => void;
}) => {
    const history = useHistory();

    const goToPatient = () => {
        if (patient?.suggestNewEncounter) {
            setShowNewEncounter(patient.id);
        } else {
            history.push(`/technician/patients/${patient.id}`);
        }
    };

    return (
        <div className={styles.patientContainer}>
            <PatientInfo {...patient} />

            <div className={styles.buttons}>
                <Button
                    variant="secondary"
                    onClick={() =>
                        history.push({
                            pathname: `/technician/patients/${patient.id}/documentation/notes/0`,
                            state: { from: history.location.pathname },
                        })
                    }
                >
                    Jaspr Note
                </Button>
                <Button
                    dark
                    onClick={() =>
                        history.push(`/technician/patients/${patient.id}/activate-tablet`)
                    }
                >
                    Open Patient Session
                </Button>
                <button className={styles.openPatientButton} onClick={goToPatient}>
                    <Arrow direction="right" />
                </button>
            </div>
        </div>
    );
};

export default PatientRow;
