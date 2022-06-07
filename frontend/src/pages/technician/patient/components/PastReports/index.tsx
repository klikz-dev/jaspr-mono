import { useEffect, useState } from 'react';
import useAxios from 'lib/useAxios';
import { formatDate } from 'lib/helpers';
import { Link, Route, useRouteMatch } from 'lib/router';
import Report from './Report';
import styles from './index.module.scss';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';
import { GetResponse as NotesLogGetResponse } from 'state/types/api/technician/notes-log';

export interface ReportType {
    id: number;
    patient: number;
    clinic: string;
    department: string;
    system: string;
    created: string;
    note: string;
    noteType: 'stability_plan' | 'narrative_note'; // TODO Change to -
}

interface PastReportsProps {
    patient: PatientGetResponse;
    stabilityPlanLabel: string;
}

const PastReports = ({ patient, stabilityPlanLabel }: PastReportsProps) => {
    const axios = useAxios();
    const match = useRouteMatch<{ patientId: string; reportId?: string }>();
    const patientId = parseInt(match.params.patientId, 10);
    const reportId = parseInt(match.params.reportId, 10);

    const [reports, setReports] = useState<NotesLogGetResponse>([]);
    useEffect(() => {
        (async () => {
            if (patient.currentEncounter) {
                const response = await axios.get<NotesLogGetResponse>(
                    `/technician/notes-log?patient=${patientId}`,
                );
                setReports(response.data);
            }
        })();
    }, [axios, patient.currentEncounter, patientId]);

    const narrativeNotes = reports.filter((report) => report.noteType === 'narrative_note');
    const stabilityPlanNotes = reports.filter((report) => report.noteType === 'stability_plan');

    return (
        <div className={styles.pastReports}>
            <div className={styles.details}>
                <h6>Past Self-Reports</h6>

                <div className={`typography--body2 ${styles.title}`}>
                    Comprehensive Suicide Assessment
                </div>
                <div className={styles.reports}>
                    {narrativeNotes.length === 0 && (
                        <p className="typography--body3">
                            There are no past self-report assessments available.
                        </p>
                    )}
                    {narrativeNotes.map((report) => (
                        <div key={report.id} className={`typography--body1 ${styles.report}`}>
                            <Link to={`/technician/patients/${patient.id}/report/${report.id}`}>
                                {formatDate(report.created)} - {report.clinic} - {report.department}
                            </Link>
                        </div>
                    ))}
                </div>
                <hr />
                <div className={`typography--body2 ${styles.title}`}>
                    Patient's {stabilityPlanLabel}
                </div>
                <div className={styles.reports}>
                    {stabilityPlanNotes.length === 0 && (
                        <p className="typography--body3">
                            There is no past {stabilityPlanLabel.toLowerCase()}'s available.
                        </p>
                    )}
                    {stabilityPlanNotes.map((report) => (
                        <div key={report.id} className={`typography--body1 ${styles.report}`}>
                            <Link to={`/technician/patients/${patient.id}/report/${report.id}`}>
                                {formatDate(report.created)} - {report.clinic} - {report.department}
                            </Link>
                        </div>
                    ))}
                </div>
            </div>
            <Route exact path={`/technician/patients/:patientId/report/:reportId`}>
                <Report
                    patient={patient}
                    report={reports.find((report) => report.id === reportId)}
                />
            </Route>
        </div>
    );
};

export default PastReports;
