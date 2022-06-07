import React, { useContext, useEffect, useState } from 'react';
import Sentry from 'lib/sentry';
import StoreContext from 'state/context/store';
import PatientInfoHeader from 'components/PatientInfoHeader';
import { getAnswers } from 'state/actions/assessment';
import Chart from './chart';
import logo from 'assets/logo-horizontal.png';
// Temporarily removed per EBPI-1157
//import warning from 'assets/alert.svg';
import styles from './index.module.scss';
import axios from 'axios';
import config from '../../../config';
import { AssessmentAnswers, Skills, VideoRatings } from 'state/types';
import { GetResponse } from 'state/types/api/technician/patients/_id/note';

interface ProviderSummaryProps {
    provider?: boolean;
    patient?: {
        id?: number;
        lastName?: string;
        firstName?: string;
        dateOfBirth?: string;
        mrn?: string;
        ssid?: string;
        lastLoggedInAt?: string;
    };
    answers: AssessmentAnswers;
    skills: Skills;
    patientVideos: VideoRatings;
}

const Page = ({ children }: { children: React.ReactNode }): JSX.Element => {
    return <div className={styles.page}>{children}</div>;
};

const ProviderSummary = (props: ProviderSummaryProps) => {
    const { provider, patient, answers, skills, patientVideos } = props;
    const [store, dispatch] = useContext(StoreContext);
    const [note, setNote] = useState('');
    const { user } = store;
    const { token, userType } = user;

    const noteSplitText = 'The Suicide Status Interview Core Assessment items';
    const [note1, note2] = note.split(noteSplitText);

    const nullOrUndefined = (value: any) => {
        return value === null || value === undefined;
    };

    useEffect(() => {
        if (userType === 'technician' && patient.id) {
            (async () => {
                try {
                    const response = await axios.get<GetResponse>(
                        `${config.apiRoot}/technician/patients/${patient.id}/note`,
                    );
                    const json = response.data;
                    setNote(json.narrativeNote);
                } catch (err) {
                    const { response } = err;
                    if (response?.status === 401) {
                        return dispatch({ type: 'RESET_APP' });
                    } else {
                        Sentry.captureException(err);
                    }
                }
            })();
        }
        // Note: patient property only exists for technician users, so don't access patient.id
    }, [dispatch, patient, userType]);

    const {
        abuseYesNo,
        abuseYesNoDescribe,
        timesTried,
        timesTriedDescribe,
        distress0,
        distress1,
        frustration0,
        frustration1,
        rateAgitation,
        sleepYesNo,
        sleepYesNoDescribe,
        meansYesNo,
        meansYesNoDescribe,
        ratePsych,
        mostPainful,
        mostHopeless,
        rateHopeless,
        mostHate,
        rateSelfHate,
        rateStress,
        mostStress,
        causesAgitation,
        supportivePeople,
        suicideRisk,
        checkInTime0,
        checkInTime1,
        intentYesNo,
        reasonsLive,
        rankFeelings,
        readiness,
        readinessNo,
        readinessDescribe,
        readinessYesReasons,
        readinessChanged,
        readinessYesChanged,
        stabilityRehearsal,
        stabilityConfidence,
        strategiesGeneral,
        strategiesFirearm,
        strategiesMedicine,
        strategiesPlaces,
        strategiesOther,
        strategiesCustom,
        meansWilling,
        oneThing,
        copingBody,
        copingDistract,
        copingHelpOthers,
        copingCourage,
        copingSenses,
        scoringCurrentAttempt,
        // scoringRisk,
        // scoringScore,
        scoringSuicideIndexScore,
        scoringSuicidePlanAndIntent,
    } = answers;

    const assessmentValues = [
        <div key="pain" className={styles.assessment}>
            <span className={styles.header}>
                <strong>Psychological Pain</strong>
            </span>
            <span>
                <em className={styles.quoted}>{mostPainful}</em>
            </span>
            <span>
                <strong className={styles.fillEmpty}>{ratePsych}</strong>
                /5
            </span>
        </div>,
        <div key="stress" className={styles.assessment}>
            <span className={styles.header}>
                <strong>Stress</strong>
            </span>
            <span>
                <em className={styles.quoted}>{mostStress}</em>
            </span>
            <span>
                <strong className={styles.fillEmpty}>{rateStress}</strong>
                /5
            </span>
        </div>,
        <div key="agitation" className={styles.assessment}>
            <span className={styles.header}>
                <strong>Agitation</strong>
            </span>
            <span>
                <em className={styles.quoted}>{causesAgitation}</em>
            </span>
            <span>
                <strong className={styles.fillEmpty}>{rateAgitation}</strong>
                /5
            </span>
        </div>,
        <div key="hopelessness" className={styles.assessment}>
            <span className={styles.header}>
                <strong>Hopelessness</strong>
            </span>
            <span>
                <em className={styles.quoted}>{mostHopeless}</em>
            </span>
            <span>
                <strong className={styles.fillEmpty}>{rateHopeless}</strong>
                /5
            </span>
        </div>,
        <div key="selfhate" className={styles.assessment}>
            <span className={styles.header}>
                <strong>Self-hate</strong>
            </span>
            <span>
                <em className={styles.quoted}>{mostHate}</em>
            </span>
            <span>
                <strong className={styles.fillEmpty}>{rateSelfHate}</strong>
                /5
            </span>
        </div>,
    ];

    const savedContentCount =
        patientVideos?.filter((rating) => rating.saveForLater).length +
        skills.filter((skill) => skill.saveForLater).length +
        [copingBody, copingDistract, copingHelpOthers, copingCourage, copingSenses, null]
            .flat()
            .filter((item) => item).length;

    const supportivePeopleCount = (supportivePeople || []).filter((person) => person.name).length;

    let passedAttempts = null;
    if (intentYesNo === false) {
        passedAttempts = '0';
    } else if (timesTried === 'once') {
        passedAttempts = '1';
    } else if (timesTried === 'many') {
        passedAttempts = '2+';
    }

    // Suicide Index Score Calculations

    const readyHomeSafer =
        meansWilling === 'Very willing' &&
        [
            strategiesGeneral,
            strategiesFirearm,
            strategiesMedicine,
            strategiesPlaces,
            strategiesCustom,
            strategiesOther,
        ].some((list) => list && list.length);

    useEffect(() => {
        if (token && user.userType === 'patient') {
            getAnswers(dispatch);
        }
    }, [dispatch, token, user.userType]);

    /* useEffect(() => {
        const plugin = {
            id: 'savetoimage',
            afterRender: (chart) => setChartPng(chart.toBase64Image()),
        };
        Chart.pluginService.register(plugin);
        return () => {
            Chart.pluginService.unregister(plugin);
        };
    }, []);*/

    /* const showLowCurrentAttempt =
        scoringCurrentAttempt &&
        scoringCurrentAttempt !== 'Current Attempt' &&
        ((scoringCurrentAttempt === 'No Current Attempt' && scoringRisk === 'Low') ||
            (scoringScore !== null &&
                scoringScore > -1 &&
                scoringScore < 3 &&
                scoringSuicidePlanAndIntent !== 'Suicide Plan and Intent' &&
                scoringSuicidePlanAndIntent !== 'Suicide Plan or Intent') ||
            (scoringScore === null && scoringSuicidePlanAndIntent === 'No Suicide Plan or Intent'));
    */

    // Temporarily removed per EBPI-1157
    /* const showMedCurrentAttempt =
        scoringCurrentAttempt &&
        !showLowCurrentAttempt &&
        scoringCurrentAttempt !== 'Current Attempt' &&
        ((scoringCurrentAttempt === 'No Current Attempt' &&
            (scoringRisk === 'Moderate' || scoringRisk === 'High')) ||
            (scoringSuicidePlanAndIntent === 'Suicide Plan and Intent' &&
                scoringCurrentAttempt !== 'Current Attempt') ||
            (scoringSuicidePlanAndIntent === 'Suicide Plan or Intent' &&
                scoringCurrentAttempt !== 'Current Attempt'));
    */

    // Temporarily removed per EBPI-1157
    // eslint-disable-next-line
    const showHighCurrentAttempt =
        !nullOrUndefined(scoringSuicidePlanAndIntent) &&
        scoringCurrentAttempt === 'Current Attempt';
    return (
        <>
            <Page>
                <div className={styles.container}>
                    {provider && patient && <PatientInfoHeader {...patient} answers={answers} />}
                    <header>
                        <h2>Jaspr Care Planning Report</h2>
                        <img className={styles.logo} src={logo} alt="Jaspr Health" />
                    </header>
                    {/* // Temporarily removed per EBPI-1157
                    <section className={styles.stratification}>
                        <div className={styles.col45}>
                            <h3>Initial Self-Reported Risk</h3>
                            <p className={styles.riskDescription}>
                                Risk level category assigned based on highest level category
                                endorsed on any row. (ED-SAFE decision support tool<sup>1</sup>)
                            </p>
                            {(scoringRisk === null || scoringRisk === '') && (
                                <div className={styles.warningContainer}>
                                    <img src={warning} alt="Warning" />
                                    <div className={`${styles.note} ${styles.warning}`}>
                                        Cannot calculate, patient answer missing. Follow up needed
                                        to understand nature of missing information.
                                    </div>
                                </div>
                            )}
                        </div>
                        <div className={`${styles.col55} ${styles.levels}`}>
                            <div className={styles.col33}>
                                <span
                                    className={`${styles.level} ${
                                        scoringRisk === 'Low' ? styles.active : ''
                                    }`}
                                >
                                    Low
                                </span>
                                <p>
                                    <span
                                        className={
                                            scoringRisk !== null &&
                                            scoringRisk !== '' &&
                                            scoringScore <= 2
                                                ? styles.active
                                                : ''
                                        }
                                    >
                                        0 - 2
                                    </span>
                                    <span
                                        className={`${styles.attempt} ${
                                            showLowCurrentAttempt ? styles.active : ''
                                        }`}
                                    >
                                        No current attempt
                                    </span>
                                    <span
                                        className={
                                            scoringSuicidePlanAndIntent ===
                                            'No Suicide Plan or Intent'
                                                ? styles.active
                                                : ''
                                        }
                                    >
                                        No suicide plan or intent
                                    </span>
                                </p>
                            </div>
                            <div className={styles.col33}>
                                <span
                                    className={`${styles.level} ${
                                        scoringRisk === 'Moderate' ? styles.active : ''
                                    }`}
                                >
                                    Moderate
                                </span>
                                <p>
                                    <span
                                        className={
                                            scoringRisk !== null &&
                                            scoringRisk !== '' &&
                                            scoringScore >= 3 &&
                                            scoringScore <= 4
                                                ? styles.active
                                                : ''
                                        }
                                    >
                                        3 - 4
                                    </span>
                                    <span
                                        className={`${styles.attempt} ${
                                            showMedCurrentAttempt ? styles.active : ''
                                        }`}
                                    >
                                        No current attempt
                                    </span>
                                    <span
                                        className={
                                            scoringSuicidePlanAndIntent === 'Suicide Plan or Intent'
                                                ? styles.active
                                                : ''
                                        }
                                    >
                                        Suicide plan or intent
                                    </span>
                                </p>
                            </div>
                            <div className={styles.col33}>
                                <span
                                    className={`${styles.level} ${
                                        scoringRisk === 'High' ? styles.active : ''
                                    }`}
                                >
                                    High
                                </span>
                                <p>
                                    <span
                                        className={
                                            scoringRisk !== null &&
                                            scoringRisk !== '' &&
                                            scoringScore >= 5 &&
                                            scoringScore <= 6
                                                ? styles.active
                                                : ''
                                        }
                                    >
                                        5 - 6
                                    </span>
                                    <span
                                        className={`${styles.attempt} ${
                                            showHighCurrentAttempt ? styles.active : ''
                                        }`}
                                    >
                                        Current attempt
                                    </span>
                                    <span
                                        className={
                                            scoringSuicidePlanAndIntent ===
                                            'Suicide Plan and Intent'
                                                ? styles.active
                                                : ''
                                        }
                                    >
                                        Suicide plan and intent
                                    </span>
                                </p>
                            </div>
                        </div>
                    </section> */}

                    <section className={styles.next}>
                        <h3>Jaspr Use &amp; Steps to Reduce Risk</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Item</th>
                                    <th>Status</th>
                                    <th>Possible Next Step</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Making Home Safer</td>
                                    <td>
                                        <span
                                            className={`${
                                                readyHomeSafer ? styles.ready : styles.incomplete
                                            }`}
                                        >
                                            {readyHomeSafer ? 'Ready to Review' : 'Incomplete'}
                                        </span>
                                    </td>
                                    <td>
                                        {readyHomeSafer
                                            ? 'Verify/strengthen plan to remove or restrict lethal means until suicide crisis is over'
                                            : 'Help needed to remove or restrict lethal means until suicide crisis is over.'}
                                    </td>
                                </tr>
                                <tr>
                                    <td>Sources of Support</td>
                                    <td>
                                        <span
                                            className={`${
                                                supportivePeopleCount > 1
                                                    ? styles.ready
                                                    : styles.incomplete
                                            }`}
                                        >
                                            {supportivePeopleCount > 1
                                                ? 'Ready to Review'
                                                : 'Incomplete'}
                                        </span>
                                    </td>
                                    <td>
                                        {supportivePeopleCount > 1
                                            ? 'Verify adequate support and monitoring including scheduling outpatient appointment ASAP.'
                                            : 'Help needed to increase support & monitoring, including next day appointment'}
                                    </td>
                                </tr>
                                <tr>
                                    <td>Coping Strategies</td>
                                    <td>
                                        <span
                                            className={`${
                                                savedContentCount > 3
                                                    ? styles.ready
                                                    : styles.incomplete
                                            }`}
                                        >
                                            {savedContentCount > 3
                                                ? 'Ready to Review'
                                                : 'Incomplete'}
                                        </span>
                                    </td>
                                    <td>
                                        {savedContentCount > 3
                                            ? 'Strengthen plan to use distraction, positive activities, and other specific strategies to cope with return of suicide urges'
                                            : 'Help needed to identify specific strategies to cope with return of urges (e.g., distracting or pleasant activities)'}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </section>

                    <section className={styles.readiness}>
                        <h3>Patient Reported Readiness for Discharge</h3>

                        <div className={styles.col60}>
                            <div className={styles.readyBubbles}>
                                <div
                                    className={styles.readyBubble}
                                    style={{
                                        backgroundColor:
                                            readiness === 'Not at all ready' ? '#e30000' : '#fff',
                                        borderColor:
                                            readiness === 'Not at all ready' ? '#e30000' : 'gray',
                                    }}
                                >
                                    Not at all
                                </div>
                                <div
                                    className={styles.readyBubble}
                                    style={{
                                        backgroundColor:
                                            readiness === 'Somewhat ready' ? '#FF9448' : '#fff',
                                        borderColor:
                                            readiness === 'Somewhat ready' ? '#FF9448' : 'gray',
                                    }}
                                >
                                    Somewhat
                                </div>
                                <div
                                    className={styles.readyBubble}
                                    style={{
                                        backgroundColor:
                                            readiness === 'Very ready' ? '#7ED321' : '#fff',
                                        borderColor:
                                            readiness === 'Very ready' ? '#7ED321' : 'gray',
                                    }}
                                >
                                    Very
                                </div>
                            </div>
                            <div className={styles.indicator}>
                                <strong>My reasons:</strong>
                                {readiness === 'Very ready' && (
                                    <span
                                        className={`${styles.indicator} ${
                                            readinessYesReasons ? '' : styles.quoted
                                        }`}
                                    >
                                        {readinessYesReasons
                                            ? readinessYesReasons.join(', ')
                                            : readinessDescribe}
                                    </span>
                                )}
                                {(readiness === 'Somewhat ready' ||
                                    readiness === 'Not at all ready') && (
                                    <span
                                        className={`${styles.indicator} ${styles.fillEmpty} ${styles.quoted}`}
                                    >
                                        {readinessNo || readinessDescribe}
                                    </span>
                                )}{' '}
                                {readiness === 'Very ready' && (
                                    <>
                                        <strong>What's changed:</strong>
                                        <span
                                            className={`${styles.indicator} ${styles.fillEmpty} ${styles.quoted}`}
                                        >
                                            {readinessYesChanged || readinessChanged}
                                        </span>{' '}
                                    </>
                                )}
                                <strong>Plan to cope:</strong>
                                <span
                                    className={`${styles.indicator} ${styles.fillEmpty} ${styles.quoted}`}
                                >
                                    {stabilityRehearsal}
                                </span>{' '}
                                <strong>Confidence:</strong>
                                <span className={`${styles.indicator} ${styles.fillEmpty}`}>
                                    <strong>
                                        {!nullOrUndefined(stabilityConfidence)
                                            ? ` ${stabilityConfidence}`
                                            : '[-]'}
                                    </strong>
                                    {!nullOrUndefined(stabilityConfidence) && <span>/ 100</span>}
                                </span>
                            </div>

                            <div className={styles.indicator}>
                                <strong>Willingness to secure means: </strong>
                                <span className={`${styles.indicator} ${styles.fillEmpty}`}>
                                    {meansWilling}
                                </span>
                            </div>
                        </div>
                        <div className={styles.col40}>
                            <Chart
                                checkInTime0={checkInTime0}
                                checkInTime1={checkInTime1}
                                distress0={distress0}
                                distress1={distress1}
                                frustration0={frustration0}
                                frustration1={frustration1}
                            />
                        </div>
                    </section>

                    <section className={styles.findings}>
                        <h3>Self Report Suicide Status Interview Key Findings</h3>
                        <div className={styles.col45}>
                            <div className={styles.finding}>
                                <div className={styles.top}>
                                    <span>Access to Means</span>
                                    <span>
                                        {!nullOrUndefined(meansYesNo)
                                            ? meansYesNo
                                                ? 'YES'
                                                : 'NO'
                                            : '[-]'}
                                    </span>
                                </div>
                                <div className={styles.describe}>
                                    Describe:{' '}
                                    <em className={styles.quoted}>{meansYesNoDescribe}</em>
                                </div>
                            </div>
                            <div className={styles.finding}>
                                <div className={styles.top}>
                                    <span>History Attempts (0, 1, 2+):</span>
                                    <span>
                                        {!nullOrUndefined(passedAttempts) ? passedAttempts : '[-]'}
                                    </span>
                                </div>
                                <div className={styles.describe}>
                                    Describe:{' '}
                                    <em className={styles.quoted}>{timesTriedDescribe}</em>
                                </div>
                            </div>
                            <div className={styles.finding}>
                                <div className={styles.top}>
                                    <span>History Substance Abuse:</span>
                                    <span>
                                        {!nullOrUndefined(abuseYesNo)
                                            ? abuseYesNo
                                                ? 'YES'
                                                : 'NO'
                                            : '[-]'}
                                    </span>
                                </div>
                                <div className={styles.describe}>
                                    Describe:{' '}
                                    <em className={styles.quoted}>{abuseYesNoDescribe}</em>
                                </div>
                            </div>
                            <div className={styles.finding}>
                                <div className={styles.top}>
                                    <span>History Insomnia</span>
                                    <span>
                                        {!nullOrUndefined(sleepYesNo)
                                            ? sleepYesNo
                                                ? 'YES'
                                                : 'NO'
                                            : '[-]'}
                                    </span>
                                </div>
                                <div className={styles.describe}>
                                    Describe:{' '}
                                    <em className={styles.quoted}>{sleepYesNoDescribe}</em>
                                </div>
                            </div>
                        </div>

                        <div className={styles.col55}>
                            <h4 className={styles.scoreHeading}>Suicide Index Score Group</h4>
                            <div className={styles.scale}>
                                <div className={styles.values}>
                                    <div className={styles.scores}>
                                        <div
                                            className={
                                                scoringSuicideIndexScore === 2 ? styles.active : ''
                                            }
                                        >
                                            <span>+2</span>
                                        </div>
                                        <div
                                            className={
                                                scoringSuicideIndexScore === 1 ? styles.active : ''
                                            }
                                        >
                                            <span>+1</span>
                                        </div>
                                        <div
                                            className={
                                                scoringSuicideIndexScore === 0 ? styles.active : ''
                                            }
                                        >
                                            <span>0</span>
                                        </div>
                                        <div
                                            className={
                                                scoringSuicideIndexScore === -1 ? styles.active : ''
                                            }
                                        >
                                            <span>-1</span>
                                        </div>
                                        <div
                                            className={
                                                scoringSuicideIndexScore === -2 ? styles.active : ''
                                            }
                                        >
                                            <span>-2</span>
                                        </div>
                                    </div>
                                    <div className={styles.labels}>
                                        <span className={styles.legend}>Wish to live</span>
                                        <span className={styles.legend}>Wish to die</span>
                                    </div>
                                </div>

                                <div className={styles.note}>
                                    When wish to live is stronger than wish to die, risk for suicide
                                    may be lowered with better response to short term suicide
                                    specific treatment.
                                    <sup>1</sup>
                                </div>
                            </div>
                            <h4 className={styles.scoreHeading}>
                                Self-Reported Overall Risk of Suicide
                            </h4>
                            <div className={styles.scale}>
                                <div className={styles.values}>
                                    <div className={styles.scores}>
                                        <div className={suicideRisk === 1 ? styles.active : ''}>
                                            <span>1</span>
                                        </div>
                                        <div className={suicideRisk === 2 ? styles.active : ''}>
                                            <span>2</span>
                                        </div>
                                        <div className={suicideRisk === 3 ? styles.active : ''}>
                                            <span>3</span>
                                        </div>
                                        <div className={suicideRisk === 4 ? styles.active : ''}>
                                            <span>4</span>
                                        </div>
                                        <div className={suicideRisk === 5 ? styles.active : ''}>
                                            <span>5</span>
                                        </div>
                                    </div>
                                    <div className={styles.labels}>
                                        <span className={styles.legend}>Will not kill self</span>
                                        <span className={styles.legend}>Will kill self</span>
                                    </div>
                                </div>

                                <div className={styles.note}>
                                    Higher scores indicate higher acute suicidality and longer
                                    treatment response moderated by self-hate and hopelessness.
                                    <sup>2</sup>
                                </div>
                            </div>
                            <div className={styles.oneThing}>
                                <div className={styles.heading}>
                                    The One Thing to No Longer Feel Suicidal:
                                </div>
                                <div className={styles.describe}>
                                    Describe: <em className={styles.quoted}>{oneThing}</em>
                                </div>
                            </div>
                        </div>
                    </section>
                    <section
                        className={styles.coreAssessment}
                        style={{ borderBottom: '1px solid #6d7278' }}
                    >
                        <div className={styles.col60}>
                            <h4>SSI Core Assessment</h4>
                            <div
                                className={`${styles.ranker} ${
                                    Boolean(rankFeelings) ? styles.ranked : ''
                                }`}
                            >
                                <div className={styles.rankHeader}>Rank</div>
                                <div className={styles.values} data-count={5}>
                                    {(rankFeelings || '1,2,3,4,5')
                                        .split(',')
                                        .map((rank) => assessmentValues[parseInt(rank, 10) - 1])}
                                </div>
                                <div className={styles.note}>
                                    High hopelessness, self-hate, and overall risk may suggest
                                    chronic suicidality. High agitation and stress may suggest acute
                                    suicidality.
                                    <sup>3</sup>
                                </div>
                            </div>
                        </div>

                        <div className={styles.col40}>
                            <h4>Reasons for Living</h4>
                            <div className={styles.ranker}>
                                <div className={styles.rankHeader}>Rank</div>
                                <div
                                    className={styles.values}
                                    data-count={(reasonsLive || []).length}
                                >
                                    {(reasonsLive || []).map((reason) => (
                                        <div key={reason} className={styles.assessment}>
                                            <em className={styles.quoted}>{reason}</em>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </section>

                    <footer>
                        {/* // Temporarily removed per EBPI-1157
                        1. Boudreaux, E. D., Larkin, C., Camargo, C. A., & Miller, I. W. (2020).
                        Validation of a secondary screener for suicide risk: results from the
                        Emergency Department Safety Assessment and Follow-up Evaluation (ED-SAFE).
                        The Joint Commission Journal on Quality and Patient Safety.
                        <br />
                    */}
                        1. Brown, G. K., Steer, R. A., Henriques, G. R., & Beck, A. T. (2005). The
                        internal struggle between the wish to die and the wish to live: A risk
                        factor for suicide. American Journal of Psychiatry, 162, 1977-1979.
                        <br />
                        2. Jobes DA, Kahn-Greene E, Greene JA, Goeke-Morey M. Clinical improvements
                        of suicidal outpatients: Examining suicide status form responses as
                        predictors and moderators. Archives of Suicide Research. 2009;13(2):147-159.
                        doi: 10.1080/13811110902835080
                        <br />
                        3. Conrad AK, Jacoby AM, Jobes DA, et al. A psychometric investigation of
                        the Suicide Status Form II with a psychiatric inpatient sample. Suicide and
                        Life-Threatening Behavior. 2009;39(3):307-320.
                        doi:10.1521/suli.2009.39.3.307.
                    </footer>
                </div>
            </Page>
            {userType === 'technician' && provider && patient && (
                <>
                    <Page>
                        <PatientInfoHeader {...patient} answers={answers} />
                        <h3>NARRATIVE NOTE (PART 1)</h3>
                        <p className={styles.notePage}>{note1}</p>
                    </Page>
                    <Page>
                        <PatientInfoHeader {...patient} answers={answers} />
                        <h3>NARRATIVE NOTE (PART 2)</h3>
                        <p className={styles.notePage}>
                            {noteSplitText} {note2}
                        </p>
                    </Page>
                </>
            )}
        </>
    );
};

export default ProviderSummary;
