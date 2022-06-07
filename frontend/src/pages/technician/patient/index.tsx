import { useCallback, useContext, useEffect, useState } from 'react';
import ReactTooltip from 'react-tooltip';
import useAxios from 'lib/useAxios';
import { useHistory, NavLink, Switch, Route, useLocation, useRouteMatch } from 'lib/router';
import StoreContext from 'state/context/store';
import PatientInfo from './components/PatientInfo';
import EditPatient from './components/EditPatient';
import styles from './index.module.scss';
import Button from 'components/Button';
import PatientPath from './components/PatientPath';
import PastReports from './components/PastReports';
import SetPath from './SetPath';
import logoSrc from 'assets/logo.svg';
import Documentation from './Documentation';
import Ehr from './Documentation/Ehr';
import DisplaySummaries from './DisplaySummaries';
import ActivateTablet from './components/ActivateTablet';
import Credentials from './components/Credentials';
import PrintSelectedModal from './components/PrintSelectionModal';
import { GetResponse as PreferenceGetResponse } from 'state/types/api/technician/preferences';
import { GetResponse as PatientGetResponse } from 'state/types/api/technician/patients/_id';
import { Activity, PatientData, Technician } from 'state/types';
import { GetResponse as PatientDataGetResponse } from 'state/types/api/technician/patient-data';
import { GetResponse as ProviderCommentsGetResponse } from 'state/types/api/technician/encounter/_id/provider-comments';
import LethalMeans from './components/LethalMeans';
import Arrow from 'assets/icons/Arrow';

const Patient = () => {
    const axios = useAxios();
    const history = useHistory();
    const location = useLocation<{ from?: string }>();
    const match = useRouteMatch<{ patientId: string }>();
    const patientId = parseInt(match.params.patientId, 10);
    const [store] = useContext(StoreContext);
    const { device, user } = store;
    const { supportUrl } = user as Technician;
    const { inPatientContext, isEhrEmbedded } = device;
    const [patient, setPatient] = useState<PatientGetResponse>();
    const [patientData, setPatientData] = useState<PatientData>();
    const [providerComments, setProviderComments] = useState<ProviderCommentsGetResponse>({});
    const [department, setDepartment] = useState<number>();
    const [currentEncounter, setCurrentEncounter] = useState<number>();
    const [activities, setActivities] = useState<Activity[]>();
    const [preferences, setPreferences] = useState<PreferenceGetResponse>({
        timezone: 'America/New_York',
        providerNotes: false,
        stabilityPlanLabel: 'Stability Plan',
    });

    // Get preferences
    useEffect(() => {
        (async () => {
            if (department) {
                const response = await axios.get<PreferenceGetResponse>(
                    `/technician/preferences?department=${department}`,
                );
                setPreferences(response.data);
            } else {
                const response = await axios.get<PreferenceGetResponse>(`/technician/preferences`);
                setPreferences(response.data);
            }
        })();
    }, [axios, department]);

    // Get patient
    useEffect(() => {
        (async () => {
            const response = await axios.get<PatientGetResponse>(
                `/technician/patients/${patientId}`,
            );

            const { currentEncounter } = response.data;
            setPatient(response.data);
            setDepartment(response.data.departments?.[0]);
            setCurrentEncounter(response.data.currentEncounter);

            if (!currentEncounter) {
                history.replace(`${match.url}/path`);
            }
        })();
    }, [axios, history, match.url, patientId]);

    const getPatientData = useCallback(async (): Promise<void> => {
        if (currentEncounter) {
            const responseData = await axios.get<PatientDataGetResponse>(
                `/technician/patient-data/${department}/${patientId}`,
                { headers: { Heartbeat: 'ignore' } },
            );

            const questions = responseData.data.questions
                .filter((module: any) => module.type !== 'intro')
                .map((module: any) => module.questions)
                .flat();

            responseData.data['questions'] = questions;

            setPatientData(responseData.data);
        }
    }, [axios, currentEncounter, department, patientId]);

    // Get patient data
    useEffect(() => {
        getPatientData();
    }, [getPatientData, activities]);

    // Get Provider Comments
    useEffect(() => {
        (async () => {
            if (currentEncounter) {
                const responseProviderComments = await axios.get<ProviderCommentsGetResponse>(
                    `/technician/encounter/${currentEncounter}/provider-comments`,
                );

                setProviderComments(responseProviderComments.data);
            }
        })();
    }, [axios, currentEncounter]);

    // Get assigned activities
    useEffect(() => {
        (async () => {
            if (currentEncounter) {
                const responseActivities = await axios.get<Activity[]>(
                    `/technician/encounter/${currentEncounter}/activities`,
                );

                setActivities(responseActivities.data.sort((a, b) => a.order - b.order));
            }
        })();
    }, [axios, currentEncounter]);

    // Refresh patient data regularly
    useEffect(() => {
        const interval = window.setInterval(async () => {
            const patientResponse = await axios.get<PatientGetResponse>(
                `/technician/patients/${patientId}`,
                {
                    headers: { Heartbeat: 'ignore' },
                },
            );
            setPatient(patientResponse.data);

            getPatientData();

            const responseActivities = await axios.get<Activity[]>(
                `/technician/encounter/${currentEncounter}/activities`,
            );

            setActivities(responseActivities.data.sort((a, b) => a.order - b.order));
        }, 30000);
        return () => window.clearInterval(interval);
    }, [axios, currentEncounter, department, getPatientData, patientId]);

    if (!patient) {
        return <div>Loading...</div>;
    }

    return (
        <div className={styles.container}>
            <header>
                {!inPatientContext && (
                    <div
                        className={styles.backButton}
                        onClick={() =>
                            location?.state?.from
                                ? history.replace(location.state.from)
                                : history.replace('/technician/patients')
                        }
                    >
                        <Arrow direction="left" />
                    </div>
                )}

                <PatientInfo {...patient} />
                <Switch>
                    <Route
                        exact
                        path={[
                            `${match.path}/documentation/notes/:sectionId`,
                            `${match.path}/documentation/ehr`,
                        ]}
                    >
                        <nav className={styles.documentationNav}>
                            <NavLink
                                className="typography--body1"
                                activeClassName={styles.active}
                                to={`/technician/patients/${patient.id}/documentation/notes/0`}
                                isActive={(_, location) => {
                                    const match =
                                        /\/technician\/patients\/[0-9]*\/documentation\/notes\/[0-9]*$/g;
                                    return match.test(location.pathname);
                                }}
                            >
                                {preferences.providerNotes ? 'Add Notes (optional)' : 'Review'}
                            </NavLink>
                            <NavLink
                                className="typography--body1"
                                activeClassName={styles.active}
                                to={`/technician/patients/${patient.id}/documentation/ehr`}
                            >
                                {isEhrEmbedded ? 'Send to EHR' : 'Copy & Paste Documents'}
                            </NavLink>
                        </nav>
                        <Button
                            variant="tertiary"
                            style={{ marginTop: 'auto' }}
                            onClick={() => history.replace(`/technician/patients/${patient.id}`)}
                        >
                            Close
                        </Button>
                    </Route>
                    <Route exact path={`${match.path}`}>
                        <div className={styles.buttons}>
                            <Button
                                variant="secondary"
                                onClick={() =>
                                    history.push({
                                        pathname: `/technician/patients/${patient.id}/documentation/notes/0`,
                                        state: { from: location.pathname },
                                    })
                                }
                            >
                                Jaspr Note
                            </Button>
                            <Button
                                dark
                                onClick={() =>
                                    history.push(
                                        `/technician/patients/${patient.id}/activate-tablet`,
                                    )
                                }
                            >
                                Open Patient Session
                            </Button>
                        </div>
                    </Route>

                    <Route path="*">
                        <img src={logoSrc} alt="" style={{ width: '56px', marginLeft: 'auto' }} />
                    </Route>
                </Switch>
            </header>
            <main>
                <Switch>
                    <Route
                        exact
                        path={[
                            `${match.path}`,
                            `${match.path}/path`,
                            `${match.path}/activate-tablet`,
                            `${match.path}/credentials`,
                            `${match.path}/print`,
                            `${match.path}/edit`,
                            `${match.path}/report/:reportId`,
                        ]}
                    >
                        <section style={{ flexBasis: '60%' }}>
                            <PatientPath
                                patient={patient}
                                setPatientData={setPatientData}
                                patientData={patientData}
                                activities={activities}
                                setActivities={setActivities}
                                preferences={preferences}
                            />
                        </section>
                        <section
                            style={{
                                display: 'flex',
                                flexDirection: 'column',
                                flexBasis: '30%',
                                height: '100%',
                            }}
                        >
                            <LethalMeans assessment={patientData?.answers?.answers} />
                            <PastReports
                                patient={patient}
                                stabilityPlanLabel={preferences.stabilityPlanLabel}
                            />
                            <Button
                                variant="secondary"
                                icon="help"
                                style={{ marginTop: 'auto', marginLeft: 'auto' }}
                                onClick={() => {
                                    window.location.href = supportUrl;
                                }}
                            >
                                Support
                            </Button>
                        </section>
                    </Route>

                    <Route path={`${match.path}/documentation/notes/:sectionIndex`}>
                        <Documentation
                            patientData={patientData}
                            providerComments={providerComments}
                            setProviderComments={setProviderComments}
                            currentEncounter={patient.currentEncounter}
                            preferences={preferences}
                        />
                    </Route>
                    <Route path={`${match.path}/documentation/ehr`}>
                        <Ehr
                            patient={patient}
                            providerComments={providerComments}
                            activities={activities}
                            preferences={preferences}
                        />
                    </Route>
                    <Route exact path={`${match.path}/display-summaries/:include`}>
                        <DisplaySummaries patient={patient} patientData={patientData} />
                    </Route>
                </Switch>

                {/* MODALS */}
                <Route path={`${match.path}/path`}>
                    <SetPath
                        patient={patient}
                        getPatientData={getPatientData}
                        activities={activities}
                        setActivities={setActivities}
                        stabilityPlanLabel={preferences.stabilityPlanLabel}
                    />
                </Route>
                <Route exact path={`${match.path}/activate-tablet`}>
                    <ActivateTablet {...patient} activities={activities} />
                </Route>
                <Route exact path={`${match.path}/credentials`}>
                    <Credentials patient={patient} setPatient={setPatient} />
                </Route>
                <Route exact path={`${match.path}/print`}>
                    <PrintSelectedModal
                        patient={patient}
                        stabilityPlanLabel={preferences.stabilityPlanLabel}
                    />
                </Route>
                <Route exact path={`${match.path}/edit`}>
                    <EditPatient
                        patient={patient}
                        setPatient={setPatient}
                        close={() => {
                            history.replace(`/technician/patients/${patientId}`);
                        }}
                    />
                </Route>
            </main>
            <ReactTooltip
                className={`${styles.tooltip} typography--caption`}
                effect="float"
                insecure={false}
                arrowColor="rgba(68, 78, 105, 1)"
                multiline
            />
        </div>
    );
};

export default Patient;
