import { useContext, useEffect, useState } from 'react';
import useAxios from 'lib/useAxios';
import copy from 'copy-to-clipboard';
import StoreContext from 'state/context/store';
import Note from './Note';
import Button from 'components/Button';
import config from '../../../../../config';
import styles from './index.module.scss';
import Segment, { AnalyticNames } from 'lib/segment';
import toast from 'lib/toast';
import { Activity, Preferences } from 'state/types';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';
import { GetResponse as NotesLogGetResponse } from 'state/types/api/technician/notes-log';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';
import { GetResponse as NoteGetResponse } from 'state/types/api/technician/patients/_id/note';

interface EhrProps {
    patient: PatientGetResponse;
    providerComments: ProviderCommentsGetResponse;
    activities: Activity[];
    preferences: Preferences;
}

const Ehr = ({ patient, providerComments, activities = [], preferences }: EhrProps) => {
    const axios = useAxios();
    const [store, dispatch] = useContext(StoreContext);
    const { device } = store;
    const { isEhrEmbedded } = device;
    const [narrativeNote, setNarrativeNote] = useState('');
    const [stabilityPlanNote, setStabilityPlanNote] = useState('');
    const [narrativeNoteChecked, setNarrativeNoteChecked] = useState(true);
    const [stabilityPlanNoteChecked, setStabilityPlanNoteChecked] = useState(true);
    const [noteSaving, setNoteSaving] = useState(false);

    useEffect(() => {
        (async () => {
            if (patient.id) {
                const response = await axios.get<NoteGetResponse>(
                    `/technician/patients/${patient.id}/note`,
                );
                const json = response.data;
                setNarrativeNote(json.narrativeNote);
                setStabilityPlanNote(json.stabilityPlanNote);
            }
        })();
    }, [axios, dispatch, patient.currentEncounter, patient.id]);

    const stabilityPlanActive = activities.some((activity) => activity.type === 'stability_plan');
    const suicideAssessmentActive = activities.some(
        (activity) => activity.type === 'stability_plan' || activity.type === 'suicide_assessment',
    );

    const copyToClipboard = () => {
        let data = '';

        if (suicideAssessmentActive && narrativeNoteChecked) {
            data = narrativeNote;
            if (stabilityPlanNote) {
                data = data + '\n\n';
            }
        }
        if (stabilityPlanActive && stabilityPlanNoteChecked) {
            data = data + stabilityPlanNote;
        }
        copy(data, {
            format: 'text/plain',
        });
        sendNoteToEhr();
        Segment.track(AnalyticNames.NOTE_COPIED_TO_CLIPBOARD, {
            stabilityPlan: stabilityPlanNoteChecked,
            narrativeNote: narrativeNoteChecked,
            patient: patient.analyticsToken,
        });
    };

    const sendNoteToEhr = async () => {
        setNoteSaving(true);
        const payload = {
            narrativeNote: narrativeNoteChecked,
            stabilityPlanNote: stabilityPlanNoteChecked,
            encounter: patient.currentEncounter,
        };
        try {
            await axios.post<NotesLogGetResponse>(
                `${config.apiRoot}/technician/notes-log`,
                payload,
            );
            toast.success(
                isEhrEmbedded
                    ? "Patient's documentation has been saved to your Medical Record system"
                    : "Patient's documentation has been copied to your clipboard",
                {
                    dark: true,
                },
            );

            Segment.track(AnalyticNames.NOTE_SENT_TO_EHR, {
                stabilityPlan: stabilityPlanNoteChecked,
                narrativeNote: narrativeNoteChecked,
                patient: patient.analyticsToken,
            });
        } catch (err) {
            toast.error('There was an error saving the patient note', {
                dark: true,
            });
            console.log('err', err);
        } finally {
            setNoteSaving(false);
        }
    };

    const ssiActivities = activities?.filter((activity) =>
        ['stability_plan', 'suicide_assessment', 'lethal_means'].includes(activity.type),
    );

    const stabilityPlan = activities.find((activity) => activity.type === 'stability_plan');
    let stabilityPlanStatus = 'Not Assigned';
    if (stabilityPlan) {
        if (stabilityPlan.status === 'in-progress') {
            stabilityPlanStatus = 'In Progress';
        } else if (stabilityPlan.status === 'completed') {
            stabilityPlanStatus = 'Completed';
        } else {
            stabilityPlanStatus = 'Not Started';
        }
    }

    let ssiStatus = 'Not Assigned';

    if (
        ssiActivities.length &&
        ssiActivities.every((activity) => activity.status === 'completed')
    ) {
        ssiStatus = 'Completed';
    } else if (ssiActivities.some((activity) => activity.status === 'in-progress')) {
        ssiStatus = 'In Progress';
    } else if (ssiActivities.length) {
        ssiStatus = 'Not Started';
    }

    return (
        <div className={styles.ehr}>
            <div className={styles.top}>
                <div>
                    <h3>Jaspr Notes</h3>
                    {isEhrEmbedded && <p>Select documentation to bundle into dot phrase.</p>}
                    {!isEhrEmbedded && <p>Select documentation to copy</p>}
                </div>
            </div>
            <div className={styles.notes}>
                <Note
                    label={`Patient's ${preferences.stabilityPlanLabel}`}
                    description="Coping plan for AVS, to share with patient."
                    status={stabilityPlanStatus}
                    active={stabilityPlanActive}
                    noteType="stability-plan"
                    note={stabilityPlanNote}
                    checked={stabilityPlanNoteChecked}
                    setChecked={setStabilityPlanNoteChecked}
                    currentEncounter={patient.currentEncounter}
                />
                <Note
                    label={
                        Object.keys(providerComments).length > 0
                            ? 'Suicide Status Interview with Provider Notes'
                            : 'Suicide Status Interview'
                    }
                    status={ssiStatus}
                    active={suicideAssessmentActive}
                    description="EHR-ready summary note of all patient self-reports."
                    noteType="narrative-note"
                    note={narrativeNote}
                    checked={narrativeNoteChecked}
                    setChecked={setNarrativeNoteChecked}
                    currentEncounter={patient.currentEncounter}
                />
                <Button
                    dark
                    onClick={isEhrEmbedded ? sendNoteToEhr : copyToClipboard}
                    disabled={noteSaving || (!stabilityPlanNoteChecked && !narrativeNoteChecked)}
                >
                    {isEhrEmbedded ? 'Send to EHR' : 'Copy Documentation'}
                </Button>
            </div>
        </div>
    );
};

export default Ehr;
