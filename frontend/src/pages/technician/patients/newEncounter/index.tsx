import { useEffect, useState } from 'react';
import { DateTime } from 'luxon';
import { useHistory } from 'react-router-dom';
import useAxios from 'lib/useAxios';
import Button from 'components/Button';
import styles from './index.module.scss';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';
import { GetResponse as PreferenceGetResponse } from 'state/types/api/technician/preferences';
import AddActivities from 'pages/technician/patient/AddActivities';

const formatTime = (datetime: string): string => {
    const date = DateTime.fromISO(datetime);
    if (!date.isValid) return '';
    return date.toFormat('MM/dd/yyyy');
};

const daysSince = (datetime: string): number => {
    const now = DateTime.now();
    const date = DateTime.fromISO(datetime);

    const diff = now.diff(date, ['days']);
    return Math.trunc(diff.days);
};

interface NewEncounterProp {
    patient: PatientGetResponse;
    close: () => void;
    setPatients: any;
    setShowNewEncounter: any;
}

const NewEncounter = ({ patient, close, setPatients, setShowNewEncounter }: NewEncounterProp) => {
    const history = useHistory();
    const axios = useAxios();
    const [showAddActivities, setShowAddActivities] = useState(false);
    const [preferences, setPreferences] = useState<PreferenceGetResponse>({
        timezone: 'America/New_York',
        providerNotes: false,
        stabilityPlanLabel: 'Stability Plan',
    });

    // Get preferences
    useEffect(() => {
        (async () => {
            if (patient.departments?.[0]) {
                const response = await axios.get<PreferenceGetResponse>(
                    `/technician/preferences?department=${patient.departments?.[0]}`,
                );
                setPreferences(response.data);
            }
        })();
    }, [axios, patient.departments]);

    return (
        <>
            {!showAddActivities && (
                <div className={styles.container}>
                    <h4>Create New Encounter?</h4>
                    <p>
                        Its been {daysSince(patient.currentEncounterCreated)} days since{' '}
                        {patient.firstName} {patient.lastName} last used Jaspr. If you wish to
                        continue with the existing encounter, click Continue Encounter.
                    </p>
                    <h6>Existing Encounter Details</h6>
                    <div className={styles.row}>
                        <div className={styles.field}>
                            <span className="typography--overline">Created On</span>
                            <span className="typography--h4">
                                {formatTime(patient.currentEncounterCreated)}
                            </span>
                        </div>
                        <div className={styles.field}>
                            <span className="typography--overline">Location</span>
                            <span className="typography--h4">
                                {patient.currentEncounterDepartment}
                            </span>
                        </div>
                    </div>
                    <div className={styles.row} style={{ marginTop: '4rem' }}>
                        <div className={styles.field}>
                            <span className="typography--overline">Patient Name</span>
                            <span className="typography--h4">
                                {patient.firstName} {patient.lastName}
                            </span>
                        </div>
                        <div className={styles.field}>
                            <span className="typography--overline">DOB</span>
                            <span className="typography--h4">
                                {formatTime(patient.dateOfBirth)}
                            </span>
                        </div>
                        <div className={styles.field}>
                            <span className="typography--overline">MRN</span>
                            <span className="typography--h4">{patient.mrn}</span>
                        </div>
                    </div>
                    <div className={styles.row} style={{ marginTop: '6.4rem' }}>
                        <Button variant="tertiary" style={{ marginRight: 'auto' }} onClick={close}>
                            Back
                        </Button>
                        <Button
                            variant="tertiary"
                            style={{ marginRight: '1rem' }}
                            onClick={() => history.push(`/technician/patients/${patient.id}`)}
                        >
                            Continue Encounter
                        </Button>
                        <Button variant="primary" dark onClick={() => setShowAddActivities(true)}>
                            Create New Encounter
                        </Button>
                    </div>
                </div>
            )}
            {showAddActivities && (
                <AddActivities
                    patient={patient}
                    setPatients={setPatients}
                    activities={[]}
                    setActivities={() => {}}
                    getPatientData={() => {}}
                    close={() => history.push(`/technician/patients/${patient.id}`)}
                    createNewEncounter
                    stabilityPlanLabel={preferences.stabilityPlanLabel}
                />
            )}
        </>
    );
};

export default NewEncounter;
