import { useState } from 'react';
import Modal, { Styles } from 'react-modal';
import { useHistory, useRouteMatch, useLocation } from 'lib/router';
import Checkbox from 'components/Checkbox';
import Button from 'components/Button';
import styles from './index.module.scss';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';
import Warning from 'assets/icons/Warning';

const printModalStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'space-evenly',
        background: 'linear-gradient(90deg, rgba(56,60,88,0.83) 0%, rgba(52,50,69,0.83) 100%)',
    },
    content: {
        position: 'static',
        display: 'flex',
        alignSelf: 'center',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        backgroundColor: 'rgba(45,46,67,1)',
        border: 'none',
        borderRadius: '5px',
        padding: 0,
        height: '450px',
        width: '600px',
        margin: 'auto',
        overflow: 'hidden',
    },
};

const PrintSelectionModal = ({
    patient,
    stabilityPlanLabel = 'Stability Plan',
}: {
    patient: PatientGetResponse;
    stabilityPlanLabel: string;
}) => {
    const history = useHistory();
    const location = useLocation();
    const match = useRouteMatch<{ patientId: string }>();
    const patientId = parseInt(match.params.patientId, 10);

    const [include, setInclude] = useState<string[]>([
        'carePlanningReport',
        'interviewSummary',
        'stabilityPlanFull',
        'stabilityPlanAbridged',
    ]);
    const [error, setError] = useState('');
    const { mrn, ssid } = patient;

    const toggleInclude = (name: string) => {
        if (include.indexOf(name) === -1) {
            setError('');
            setInclude([...include, name]);
        } else {
            setInclude(include.filter((e) => e !== name));
        }
    };

    const displaySummaries = (): void => {
        if (!include.length) {
            setError('Must select at least one summary or plan.');
        } else {
            history.push({
                pathname: `/technician/patients/${patientId}/display-summaries/${include.join(
                    '+',
                )}`,
                state: location.state,
            });
        }
    };

    return (
        <Modal isOpen style={printModalStyle}>
            <div className={styles.modalTitle}>Print Patient Summaries</div>
            <div className={styles.patientIdLabel}>
                {mrn && <span>MRN: {mrn}</span>}
                {!mrn && ssid && <span>SSID: {ssid}</span>}
            </div>
            <div className={styles.checkboxes}>
                <Checkbox
                    checked={include.indexOf('carePlanningReport') >= 0}
                    onChange={() => toggleInclude('carePlanningReport')}
                    label="Care Planning Report"
                />

                <Checkbox
                    checked={include.indexOf('interviewSummary') >= 0}
                    onChange={() => toggleInclude('interviewSummary')}
                    label="Suicide Status Interview Summary"
                />

                <Checkbox
                    checked={include.indexOf('stabilityPlanFull') >= 0}
                    onChange={() => toggleInclude('stabilityPlanFull')}
                    label={`${stabilityPlanLabel} - Full`}
                />
                <Checkbox
                    checked={include.indexOf('stabilityPlanAbridged') >= 0}
                    onChange={() => toggleInclude('stabilityPlanAbridged')}
                    label={`${stabilityPlanLabel} - Abridged, Pocket-Size`}
                />
            </div>
            <div className={styles.buttons}>
                <Button variant="secondary" onClick={() => history.goBack()}>
                    Cancel
                </Button>
                <Button onClick={displaySummaries}>Print Preview</Button>
            </div>
            {error && (
                <div className={styles.error}>
                    <Warning />
                    {error}
                </div>
            )}
        </Modal>
    );
};

export default PrintSelectionModal;
