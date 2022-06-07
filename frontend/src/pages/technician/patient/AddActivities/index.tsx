import { useEffect, useState } from 'react';
import ReactTooltip from 'react-tooltip';
import useAxios from 'lib/useAxios';
import Checkbox from 'components/Checkbox';
import styles from './index.module.scss';
import Button from 'components/Button';
import { GetResponse } from 'state/types/api/technician/patients/_id';
import { PostResponse } from 'state/types/api/technician/encounter/_id/activities';
import { PostResponse as EncounterPostResponse } from 'state/types/api/technician/encounter';
import { PostResponse as ActivitiesPostResponse } from 'state/types/api/technician/encounter/_id/activities';
import Segment, { AnalyticNames } from 'lib/segment';

interface SetPathProps {
    patient: GetResponse;
    activities: PostResponse;
    setActivities: (activities: PostResponse) => void;
    setPatients?: (patients: GetResponse[] | ((prevVar: GetResponse[]) => GetResponse[])) => void;
    getPatientData: () => void;
    close: () => void;
    createNewEncounter?: boolean;
    stabilityPlanLabel: string;
}

const AddActivities = ({
    patient,
    activities = [],
    setActivities,
    setPatients = () => {},
    getPatientData = () => {},
    close,
    createNewEncounter = false,
    stabilityPlanLabel,
}: SetPathProps) => {
    const axios = useAxios();
    const [saving, setSaving] = useState(false);
    const [csa, setCsa] = useState(false);
    const [csp, setCsp] = useState(false);
    const [skills, setSkills] = useState(false);

    const [error, setError] = useState('');

    useEffect(() => {
        ReactTooltip.rebuild();
        return () => {
            ReactTooltip.rebuild();
        };
    }, []);

    useEffect(() => {
        if (csp) {
            // Crisis Stability Plan requires comfort and skills to be enabled
            setSkills(true);
        }
    }, [csp]);

    const setPath = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setSaving(true);
        setError('');

        try {
            let encounterId = patient.currentEncounter;
            if (createNewEncounter) {
                const encounterResponse = await axios.post<EncounterPostResponse>(
                    `/technician/encounter`,
                    {
                        patient: patient.id,
                    },
                );

                setPatients((patients) =>
                    patients.map((patient) =>
                        patient.id === encounterResponse.data.id ? encounterResponse.data : patient,
                    ),
                );
                encounterId = encounterResponse.data.currentEncounter;
                Segment.track(AnalyticNames.TECHNICIAN_CREATED_NEW_ENCOUNTER);
            }

            const response = await axios.post<ActivitiesPostResponse>(
                `/technician/encounter/${encounterId}/activities`,
                {
                    csp,
                    csa,
                    skills,
                },
            );
            setActivities(response.data.sort((a, b) => a.order - b.order));
            getPatientData();
            Segment.track(AnalyticNames.TECHNICIAN_SET_PATIENT_PATH, {
                activities: { csp, csa, skills },
            });
            close();
        } catch (err) {
            setSaving(false);
            setError('There was an error updating the patient path');
        }
    };

    const currentCsa = activities
        .sort((a, b) => new Date(b.created).getTime() - new Date(a.created).getTime())
        .filter((activity) => activity.type === 'suicide_assessment')?.[0];

    const skillsDisabled =
        csp || activities.some((activity) => activity.type === 'comfort_and_skills');
    const csaDisabled = false; // Can always reassign a CSA
    const cspDisabled = activities.some((activity) => activity.type === 'stability_plan');
    return (
        <form className={styles.container} onSubmit={setPath}>
            <div className={styles.outer}>
                <h4 className={styles.header}>Add Activity</h4>
                <div className={`typography--body1 ${styles.subheader}`}>
                    Select one or more activities for the patient to complete. You can always add
                    additional activities at a later time.
                </div>
                <div className={`${styles.row} ${styles.selectActivities}`}>
                    <div
                        data-tip={
                            skillsDisabled
                                ? 'You cannot add more than<br />one Comfort & Skills Activity to<br />a patient’s path.'
                                : ''
                        }
                        className={`${styles.selector} ${skillsDisabled ? styles.disabled : ''}`}
                    >
                        <Checkbox
                            large
                            checked={skillsDisabled || skills}
                            disabled={saving || skillsDisabled}
                            onChange={({ target }) => setSkills(target.checked)}
                        />
                        <div className={styles.column}>
                            <h6>Comfort &amp; Skills</h6>
                            <span>
                                Activities, calming videos, and shared stories to enable to patient
                                to wait well.
                            </span>
                        </div>
                    </div>
                    <div
                        className={`${styles.selector}  ${cspDisabled ? styles.disabled : ''}`}
                        data-tip={
                            cspDisabled
                                ? `You cannot add more than<br />one Patient ${stabilityPlanLabel} to<br />a patient's path.`
                                : ''
                        }
                    >
                        <Checkbox
                            large
                            checked={cspDisabled || csp}
                            onChange={({ target }) => setCsp(target.checked)}
                            disabled={saving || cspDisabled}
                        />
                        <div className={styles.column}>
                            <h6>Patient {stabilityPlanLabel}</h6>
                            <span>
                                Guides creation of coping plan for suicidal urges and emotional
                                distress.
                            </span>
                        </div>
                    </div>
                    <div className={`${styles.selector}  ${csaDisabled ? styles.disabled : ''}`}>
                        <Checkbox
                            large
                            checked={csaDisabled || csa}
                            onChange={({ target }) => setCsa(target.checked)}
                            disabled={saving || csaDisabled}
                        />
                        <div className={styles.column}>
                            <h6>
                                {currentCsa
                                    ? 'Reassign Comprehensive Suicide Assessment'
                                    : 'Comprehensive Suicide Assessment'}
                            </h6>
                            <span>
                                {currentCsa
                                    ? 'Restart assessment from the beginning to help the patient tell their story, gather risk and protective factors.'
                                    : 'Helps patient tell their story, gathers risk and protective factors.'}
                            </span>
                        </div>
                    </div>
                    {Boolean(error) && <div className={styles.error}>{error}</div>}
                </div>
                <div className={styles.buttons}>
                    <Button variant="tertiary" onClick={close}>
                        Cancel
                    </Button>
                    <Button type="submit" dark>
                        Add
                    </Button>
                </div>
            </div>
        </form>
    );
};

export default AddActivities;
