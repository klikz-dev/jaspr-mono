import React, { useContext, useEffect, useState } from 'react';
import Modal, { Styles } from 'react-modal';
import { useHistory } from 'react-router-dom';
import styles from './index.module.scss';
import { useLocation } from 'lib/router';
import Link from 'components/Link';
import StoreContext from 'state/context/store';
import Section, { StatusType as SectionStatus } from './Section';
import { Activity, Patient, PatientData, Preferences } from 'state/types';
import { PatchResponse } from 'state/types/api/technician/encounter/_id/activities/_id';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';
import { GetResponse as NotesLogGetResponse } from 'state/types/api/technician/notes-log';
import Button from 'components/Button';
import CirclePlus from 'assets/icons/CirclePlus';
import useAxios from 'lib/useAxios';
import Segment, { AnalyticNames } from 'lib/segment';
import CsaInProgress from '../CsaInProgress';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(0,0,0,0.4)',
    },
    content: {
        position: 'relative',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-around',
        flexDirection: 'column',
        border: 'none',
        backgroundColor: '#ffffff',
        padding: '20px 50px',
        overflow: 'hidden',
        borderRadius: '6px',
        maxHeight: '75%',
        inset: 'auto',
    },
};

interface PatientPathProps {
    patient: PatientGetResponse;
    patientData: PatientData;
    setPatientData: (
        patientData: PatientData | ((patientData: PatientData) => PatientData),
    ) => void;
    preferences: Preferences;
    activities: Activity[];
    setActivities: (activities: Activity[] | ((activities: Activity[]) => Activity[])) => void;
}

const PatientPath = ({
    patient,
    patientData,
    setPatientData,
    preferences,
    activities = [],
    setActivities,
}: PatientPathProps) => {
    const history = useHistory();
    const location = useLocation();
    const axios = useAxios();
    const [store] = useContext(StoreContext);
    const { device } = store;
    const { isEhrEmbedded } = device;
    const [viewCsaInProgressModal, setViewCsaInProgressModal] = useState<false | number>(false);
    const [userNotifiedCSAInProgress, setUserNotifiedCSAInProgress] = useState(false);
    const { id, toolsToGoStatus } = patient;
    const { answers = {} } = patientData?.answers || {};

    /**
     * Show the CSA In progress modal if the status is in progress when the technician
     * navigates to this screen, or the status changes while the technician is on this
     * screen
     */
    useEffect(() => {
        const suicideAssessment = activities.find(
            (activity) =>
                activity.type === 'suicide_assessment' && activity.status === 'in-progress',
        );
        if (!userNotifiedCSAInProgress && suicideAssessment) {
            setUserNotifiedCSAInProgress(true);
            setViewCsaInProgressModal(suicideAssessment.id);
        }
    }, [activities, userNotifiedCSAInProgress]);

    const toggleLock = async (activity: Activity, locked: boolean) => {
        const response = await axios.patch<PatchResponse>(
            `/technician/encounter/${patient.currentEncounter}/activities/${activity.id}`,
            {
                locked,
            },
        );

        setActivities((activities) => {
            const updatedActivities = activities
                .map((originalActivity) => {
                    if (originalActivity.id === activity.id) {
                        return response.data;
                    }
                    return originalActivity;
                })
                .sort((a, b) => a.order - b.order);

            return updatedActivities;
        });
    };

    const statusLookup = {
        'not-assigned': 'Not Assigned',
        assigned: 'Assigned',
        'not-started': 'Not Started',
        'in-progress': 'In Progress',
        completed: 'Completed',
        updated: 'Updated',
    };

    const typeLookup = {
        outro: 'Exit Questions',
        intro: 'Introduction',
        lethal_means: 'Lethal Means',
        comfort_and_skills: 'Comfort & Skills',
        suicide_assessment: 'Comprehensive Suicide Assessment',
        stability_plan: `Patient's ${preferences.stabilityPlanLabel}`,
    };

    const convertToolsToGoStatus = (status: Patient['toolsToGoStatus']): SectionStatus => {
        switch (status) {
            case 'Not Started':
                return 'Not Started';
            case 'Email Sent':
                return 'Completed';
            case 'Phone Number Verified':
                return 'Completed';
            case 'Setup Finished':
                return 'Completed';
            default:
                return 'Not Started';
        }
    };

    const sendNoteToEhr = async (e: React.MouseEvent) => {
        e.preventDefault();
        const payload = {
            narrativeNote: true,
            stabilityPlanNote: true,
            encounter: patient.currentEncounter,
        };
        try {
            axios.post<NotesLogGetResponse>(`/technician/notes-log`, payload);
            Segment.track(AnalyticNames.NOTE_SENT_TO_EHR, {
                stabilityPlan: true,
                narrativeNote: true,
                patient: patient.analyticsToken,
            });
        } catch (err) {
            console.log('err', err);
        }
    };

    return (
        <div className={styles.patientPath}>
            <h3 className="typography--overline">Assigned Activities</h3>

            <div className={styles.timeline}>
                {activities
                    .sort((a, b) => a.order - b.order)
                    .map((activity) => (
                        <React.Fragment key={activity.id}>
                            <Section
                                // @ts-ignore
                                status={statusLookup[activity.status]}
                                assigned
                                completedTimestamp={activity.statusUpdated}
                                title={typeLookup[activity.type]}
                                type={activity.type}
                                preferences={preferences}
                            >
                                {activity.type === 'suicide_assessment' &&
                                    activity.status !== 'completed' &&
                                    activity.status !== 'updated' && (
                                        <div
                                            className={styles.linkButtons}
                                            style={{ marginTop: '3.8rem' }}
                                        >
                                            <Button
                                                variant="tertiary"
                                                onClick={() =>
                                                    setViewCsaInProgressModal(activity.id)
                                                }
                                            >
                                                Mark as Completed
                                            </Button>
                                        </div>
                                    )}
                                {activity.type === 'stability_plan' && (
                                    <>
                                        <div className={styles.cspData}>
                                            <div
                                                className={`typography--overline ${styles.cspDatum}`}
                                            >
                                                Confidence
                                                <br />
                                                <span className={styles.value}>
                                                    {answers?.stabilityConfidence
                                                        ? answers.stabilityConfidence
                                                        : '-'}
                                                </span>
                                            </div>
                                            <div
                                                className={`typography--overline ${styles.cspDatum}`}
                                            >
                                                Readiness
                                                <br />
                                                <span className={styles.value}>
                                                    {answers?.readiness ? answers.readiness : '-'}
                                                </span>
                                            </div>
                                        </div>

                                        <div className={styles.linkButtons}>
                                            <Link
                                                to={{
                                                    pathname: location.pathname,
                                                }}
                                                onClick={(e) => {
                                                    e.preventDefault();
                                                    toggleLock(activity, !activity.locked);
                                                }}
                                            >
                                                {activity.locked ? 'Unlock' : 'Lock'}
                                            </Link>
                                        </div>
                                    </>
                                )}
                            </Section>
                            {activity.type === 'stability_plan' && (
                                <Section
                                    key={`${activity.id}-jah`}
                                    status={convertToolsToGoStatus(toolsToGoStatus)}
                                    type="jah"
                                    assigned
                                    title="Jaspr at Home"
                                >
                                    {toolsToGoStatus === 'Not Started' && (
                                        <p>
                                            The patient can create credentials through their
                                            take-away kit.
                                        </p>
                                    )}
                                </Section>
                            )}
                        </React.Fragment>
                    ))}
                <div className={styles.addActivityRow} style={{ marginRight: 'auto' }}>
                    <CirclePlus showPlus />
                    <Button
                        variant="secondary"
                        onClick={() => {
                            history.push({
                                pathname: `/technician/patients/${id}/path`,
                                state: { from: location },
                            });
                        }}
                    >
                        Add Activity
                    </Button>
                </div>
            </div>
            <div
                className={styles.linkButtons}
                style={{ paddingBottom: '0.8rem', paddingRight: '0.8rem' }}
            >
                <Link
                    to={{
                        pathname: `/technician/patients/${id}/print`,
                        state: { from: location },
                    }}
                >
                    Print Documents
                </Link>
                {isEhrEmbedded && (
                    <Link to={{ pathname: location.pathname }} onClick={sendNoteToEhr}>
                        Send to EHR
                    </Link>
                )}
            </div>
            <Modal isOpen={Boolean(viewCsaInProgressModal)} style={modalStyle}>
                <CsaInProgress
                    close={() => setViewCsaInProgressModal(false)}
                    toggleLock={toggleLock}
                    activity={activities.find((activity) => activity.id === viewCsaInProgressModal)}
                    patient={patient}
                    patientData={patientData}
                    preferences={preferences}
                />
            </Modal>
        </div>
    );
};

export default PatientPath;
