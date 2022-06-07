import { useEffect, useMemo } from 'react';
import { useHistory, useLocation, useRouteMatch } from 'lib/router';
import ProviderSummary from 'pages/technician/providerSummary';
import CamsSummary from 'pages/patient/takeaway/camsSummary';
import StabilityPlanFull from 'components/StabilityPlan';
import StabilityPlanAbridged from 'components/StabilityCard';
import Button from 'components/Button';
import Segment, { AnalyticNames } from 'lib/segment';
import styles from './index.module.scss';
import { PatientData } from 'state/types';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';

interface DisplaySummariesProps {
    patient: PatientGetResponse;
    patientData: PatientData;
}

const DisplaySummaries = ({ patient, patientData }: DisplaySummariesProps) => {
    const history = useHistory();
    const location = useLocation<{ from: string }>();
    const match = useRouteMatch<{ include: string }>();
    const { patientVideos = [], skills = [], questions = [] } = patientData;
    const answers = { ...patientData?.answers.answers, ...patientData?.answers.metadata };

    const include = useMemo(() => (match.params.include || '').split('+'), [match.params.include]);

    const close = () => {
        history.push(location?.state?.from ? location.state.from : '/');
    };

    useEffect(() => {
        Segment.track(AnalyticNames.SUMMARIES_PREVIEWED, {
            'care-planning-report': include.indexOf('carePlanningReport') >= 0,
            'interview-summary': include.indexOf('interviewSummary') >= 0,
            'stability-plan-full': include.indexOf('stabilityPlanFull') >= 0,
            'stability-plan-abridged': include.indexOf('stabilityPlanAbridged') >= 0,
        });
    }, [include]);

    // * TODO: Page break components joined.
    // * TODO: Print CSS and page CSS in general.
    // * TODO (Maybe): Prop(s) for components to make sure we render what we want?

    return (
        <div className={styles.base}>
            <div className={styles.controlBar}>
                <div className={styles.metadata}>
                    <div className={styles.record}>
                        <strong>ID</strong>
                        <br />
                        {patient.mrn && <span>MRN: {patient.mrn}</span>}
                        {!patient.mrn && patient.ssid && <span>SSID: {patient.ssid}</span>}
                    </div>
                    <div className={styles.record}>
                        <strong>Name</strong>
                        <br />
                        {patient.lastName}
                        {patient.lastName && patient.firstName ? ', ' : ''}
                        {patient.firstName}
                    </div>
                </div>
                <div className={styles.buttons}>
                    <Button variant="secondary" onClick={close}>
                        Close
                    </Button>
                    <Button
                        onClick={() => {
                            Segment.track(AnalyticNames.PRINT_SUMMARIES, {
                                'care-planning-report': include.indexOf('carePlanningReport') >= 0,
                                'interview-summary': include.indexOf('interviewSummary') >= 0,
                                'stability-plan-full': include.indexOf('stabilityPlanFull') >= 0,
                                'stability-plan-abridged':
                                    include.indexOf('stabilityPlanAbridged') >= 0,
                            });
                            window.print();
                        }}
                    >
                        Print
                    </Button>
                </div>
            </div>

            {include.indexOf('carePlanningReport') >= 0 && (
                <ProviderSummary
                    provider
                    patient={patient}
                    answers={answers}
                    skills={skills}
                    patientVideos={patientVideos}
                />
            )}
            {include.indexOf('interviewSummary') >= 0 && (
                <CamsSummary printMode provider patient={patient} answers={answers} />
            )}
            {include.indexOf('stabilityPlanFull') >= 0 && (
                <div style={{ background: 'white' }}>
                    <StabilityPlanFull answers={answers} edit={false} questions={questions} />
                </div>
            )}
            {include.indexOf('stabilityPlanAbridged') >= 0 && (
                <StabilityPlanAbridged answers={answers} />
            )}
        </div>
    );
};

export default DisplaySummaries;
