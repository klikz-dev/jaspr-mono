import { useContext, useEffect } from 'react';
import { useHistory } from 'lib/router';
import StoreContext from 'state/context/store';
import PatientInfoHeader from 'components/PatientInfoHeader';
import { getAnswers } from 'state/actions/assessment';
import Menu from 'components/Menu';
import RankedFeelings from './rankedFeelings';
import RankedReasonsLivingDying from './rankedReasonsLivingDying';
import styles from './index.module.scss';
import { AssessmentAnswers, Patient } from 'state/types';

interface CamsSummaryProps {
    printMode?: boolean;
    provider?: boolean;
    patient?: {
        lastName?: string;
        firstName?: string;
        dateOfBirth?: string;
        mrn?: string;
        ssid?: string;
        lastLoggedInAt?: string;
    };
    answers: AssessmentAnswers;
}

const CamsSummary = ({ printMode = false, provider, patient, answers = {} }: CamsSummaryProps) => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { token } = user as Patient;

    useEffect(() => {
        if (token && user.userType === 'patient') {
            getAnswers(dispatch);
        }
    }, [token, dispatch, user.userType]);

    const emDash = String.fromCharCode(8212);

    const allCaps = (value?: string): string => {
        if (!value) return emDash;
        return value
            .split('')
            .map((c) => c.toUpperCase())
            .join('');
    };
    const yesOrNo = (value?: boolean | null) =>
        value === true ? 'YES' : value === false ? 'NO' : emDash;

    const numOrDash = (value?: number | null) =>
        value || value?.toString() === '0' ? value : emDash; // TODO JACOB review value type

    return (
        <div className={styles.container} style={{ flexDirection: printMode ? 'column' : 'row' }}>
            {printMode && provider && patient && (
                <PatientInfoHeader {...patient} answers={answers} />
            )}
            {!printMode && <Menu selectedItem="takeaway" />}
            <div className={styles.area} style={{ padding: printMode ? '0' : 'inherit' }}>
                {!printMode && (
                    <div className={styles.header}>
                        <div className={styles.back} onClick={() => history.push('/takeaway')}>
                            Back
                        </div>
                        <h1 className={styles.title}>Your Suicide Status Interview Responses</h1>
                        <div className={styles.backPlaceholder}>Back</div>
                    </div>
                )}
                <div className={styles.summary} style={{ margin: printMode ? '0' : 'inherit' }}>
                    <div className={styles.sectionTitle}>
                        Section One: Specific Risk &amp; Protective Factors
                    </div>
                    <RankedFeelings answers={answers} />
                    <div className={styles.divider} />
                    <div className={styles.ratingBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>Overall Risk of Suicide (1-5)</div>
                        <div className={styles.item}>{answers.suicideRisk || emDash}</div>
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.ratingBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>
                            Suicide related to thoughts about yourself (1-5)
                        </div>
                        <div className={styles.item}>{answers.suicidalYourself || emDash}</div>
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.ratingBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>
                            Suicide related to thoughts about others (1-5)
                        </div>
                        <div className={styles.item}>{answers.suicidalOthers || emDash}</div>
                    </div>
                    <div className={styles.divider} />
                    <RankedReasonsLivingDying answers={answers} />
                    <div className={styles.divider} />
                    <div className={styles.ratingBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>
                            Wish to live to the following extent (0-8)
                        </div>
                        <div className={styles.item}>{numOrDash(answers.wishLive)}</div>
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.ratingBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>
                            Wish to die to the following extent (0-8)
                        </div>
                        <div className={styles.item}>{numOrDash(answers.wishDie)}</div>
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.inlineDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>
                            If there were one thing that would make you no longer feel suicidal,
                            what would that be?
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={answers.oneThing ? styles.italicsItemQuotes : styles.item}>
                            {answers.oneThing || emDash}
                        </div>
                    </div>
                    <div className={styles.pageBreak} />
                    {printMode && provider && patient && (
                        <PatientInfoHeader {...patient} answers={answers} />
                    )}
                    <div className={styles.sectionTitle}>Section Two: General Risk Factors</div>
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>Do you have suicidal thoughts?</div>
                            {answers.suicidalYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.suicidalYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.suicidalYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>
                            How frequently do you think about suicide?
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>
                            {numOrDash(answers.suicidalFreq)} time
                            {answers.suicidalFreq === 1 ? '' : 's'} per{' '}
                            {allCaps(answers.suicidalFreqUnits)}
                        </div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>
                            When you think about suicide, how long do the thoughts last?
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{allCaps(answers.lengthSuicidalThought)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Are these thoughts about killing yourself new or worse than usual
                                for you?
                            </div>
                            {answers.worseYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.worseYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.worseYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Do you have a plan or plans of how you would end your life?
                            </div>
                            {answers.planYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.planYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.planYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Do you have access to the means to take your life?
                            </div>
                            {answers.meansYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.meansYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.meansYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>Do you have access to a firearm?</div>
                            {answers.firearmsYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.firearmsYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.firearmsYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Have you taken any steps to prepare to take your life?
                            </div>
                            {answers.stepsYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.stepsYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.stepsYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Have you practiced how you would take your life?
                            </div>
                            {answers.practicedYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.practicedYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.practicedYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Have you ever made an attempt to kill yourself with the intent to
                                die?
                            </div>
                            {answers.intentYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.intentYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.intentYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Are you here today because of a current suicide attempt?
                            </div>
                            {answers.currentYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.currentYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.currentYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                How many suicide attempts have you made in your lifetime?
                            </div>
                            {answers.timesTriedDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.timesTriedDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>
                            {answers.timesTried === 'once'
                                ? 'SINGLE ATTEMPT'
                                : answers.timesTried === 'many'
                                ? 'MULTIPLE ATTEMPTS (2 OR MORE)'
                                : emDash}
                        </div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.pageBreak} />
                    {printMode && provider && patient && (
                        <PatientInfoHeader {...patient} answers={answers} />
                    )}
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Have you ever intentionally injured yourself without intending to
                                kill yourself?
                            </div>
                            {answers.nssiYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.nssiYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.nssiYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Have you ever been hospitalized for a mental health or substance use
                                problem?
                            </div>
                            {answers.hospitalizedYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.hospitalizedYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.hospitalizedYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Do you or others think you are impulsive?
                            </div>
                            {answers.impulsiveYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.impulsiveYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.impulsiveYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Do you or others think you have an alcohol or drug abuse problem?
                            </div>
                            {answers.abuseYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.abuseYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.abuseYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Have you experienced death, the loss of a job, or other losses?
                            </div>
                            {answers.lossesYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.lossesYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.lossesYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Are you having romantic and/or relationship problems?
                            </div>
                            {answers.relationshipYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.relationshipYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.relationshipYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Do you feel that others will be better off without you?
                            </div>
                            {answers.burdenOnOthersYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.burdenOnOthersYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.burdenOnOthersYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Are you having health or physical pain problems?
                            </div>
                            {answers.healthYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.healthYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.healthYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Are you having problems falling asleep, staying asleep, or sleeping
                                too much?
                            </div>
                            {answers.sleepYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.sleepYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.sleepYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Are you having any legal or financial problems?
                            </div>
                            {answers.legalYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.legalYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.legalYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Are you experiencing shame about anything in your history or your
                                current life?
                            </div>
                            {answers.shameYesNoDescribe && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.shameYesNoDescribe}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.shameYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.pageBreak} />
                    {printMode && provider && patient && (
                        <PatientInfoHeader {...patient} answers={answers} />
                    )}
                    <div className={styles.sectionTitle}>
                        Section Three: Making Home Safe & Stability Plan
                    </div>
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Selected strategies to protect yourself during a crisis (lethal
                                means safety):
                            </div>
                            <div className={styles.indentItem}>
                                {answers.strategiesGeneral?.length && (
                                    <>
                                        <strong>General:</strong>
                                        <span>{answers.strategiesGeneral?.join(', ')}</span>
                                    </>
                                )}
                                {answers.strategiesFirearm?.length && (
                                    <>
                                        <strong>Firearm:</strong>
                                        <span>{answers.strategiesFirearm?.join(', ')}</span>
                                    </>
                                )}
                                {answers.strategiesMedicine?.length && (
                                    <>
                                        <strong>Medicine:</strong>
                                        <span>{answers.strategiesMedicine?.join(', ')}</span>
                                    </>
                                )}
                                {answers.strategiesPlaces?.length && (
                                    <>
                                        <strong>Places:</strong>
                                        <span>{answers.strategiesPlaces?.join(', ')}</span>
                                    </>
                                )}
                                {answers.strategiesOther?.length && (
                                    <>
                                        <strong>Other:</strong>
                                        <span>{answers.strategiesOther?.join(', ')}</span>
                                    </>
                                )}
                                {answers.strategiesCustom?.length && (
                                    <>
                                        <strong>Custom:</strong>
                                        <span>{answers.strategiesCustom?.join(', ')}</span>
                                    </>
                                )}
                            </div>
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Can someone help you take these steps?
                            </div>
                            {answers.meansSupportWho && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.meansSupportWho}
                                    </span>
                                </div>
                            )}
                        </div>

                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{yesOrNo(answers.meansSupportYesNo)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>
                            How willing are you to secure your means with the steps you identified?
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{allCaps(answers.meansWilling)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                When you think about what brought you here today, what made the
                                urges to harm yourself go up?
                            </div>
                            {answers.crisisDesc && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.crisisDesc}
                                    </span>
                                </div>
                            )}
                        </div>

                        <div className={styles.columnFiller} />
                        <div className={styles.item}></div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>Coping Strategies</div>
                            <div className={styles.row}>
                                <div className={styles.indentItem}>
                                    {answers.copingBody?.length && (
                                        <>
                                            <strong>Body:</strong>
                                            <span>{answers.copingBody?.join(', ')}</span>
                                        </>
                                    )}

                                    {answers.copingDistract?.length && (
                                        <>
                                            <strong>Distract:</strong>
                                            <span>{answers.copingDistract?.join(', ')}</span>
                                        </>
                                    )}

                                    {answers.copingHelpOthers?.length && (
                                        <>
                                            <strong>Help Others:</strong>
                                            <span>{answers.copingHelpOthers?.join(', ')}</span>
                                        </>
                                    )}
                                </div>
                                <div className={styles.indentItem}>
                                    {answers.copingCourage?.length && (
                                        <>
                                            <strong>Courage:</strong>
                                            <span>{answers.copingCourage?.join(', ')}</span>
                                        </>
                                    )}

                                    {answers.copingSenses?.length && (
                                        <>
                                            <strong>Senses:</strong>
                                            <span>{answers.copingSenses?.join(', ')}</span>
                                        </>
                                    )}

                                    <strong>Other:</strong>
                                    <span>Watch Jaspr Videos</span>
                                </div>
                            </div>
                        </div>

                        <div className={styles.columnFiller} />
                        <div className={styles.item}></div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.pageBreak} />
                    {printMode && provider && patient && (
                        <PatientInfoHeader {...patient} answers={answers} />
                    )}
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>Supportive People</div>
                            <div className={styles.indentItem}>
                                {/* @ts-ignore */}
                                {answers.supportivePeople?.map((supportivePerson) => (
                                    <span
                                        key={`${supportivePerson.name}-${supportivePerson.phone}`}
                                    >
                                        {supportivePerson.name}: {supportivePerson.phone}
                                    </span>
                                ))}
                                <span>24/7 National Hotline: Call 1-800-273-8255</span>
                                <span>24/7 National Text Line: Text 741741</span>
                            </div>
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>Reasons for Living</div>
                            <div className={styles.indentItem}>
                                {answers.reasonsLive?.map((reasonLive) => (
                                    <span className={styles.item}>{reasonLive}</span>
                                ))}
                            </div>
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>Warning Signs</div>
                            <div className={styles.indentItem}>
                                {answers.wsActions?.length && (
                                    <>
                                        <strong>Actions:</strong>
                                        <span>{answers.wsActions?.join(', ')}</span>
                                    </>
                                )}
                                {answers.wsFeelings?.length && (
                                    <>
                                        <strong>Feelings:</strong>
                                        <span>{answers.wsFeelings?.join(', ')}</span>
                                    </>
                                )}
                                {answers.wsThoughts?.length && (
                                    <>
                                        <strong>Thoughts:</strong>
                                        <span>{answers.wsThoughts?.join(', ')}</span>
                                    </>
                                )}
                                {answers.wsStressors?.length && (
                                    <>
                                        <strong>Stressors:</strong>
                                        <span>{answers.wsStressors?.join(', ')}</span>
                                    </>
                                )}
                            </div>
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskDescriptionBlock}>
                        <div className={styles.columnFiller} />
                        <div>
                            <div className={styles.boldItem}>
                                Your plan to survive the worst moments in your own words:
                            </div>
                            {answers.stabilityRehearsal && (
                                <div className={styles.item}>
                                    Describe:{' '}
                                    <span className={styles.italicsItemQuotes}>
                                        {answers.stabilityRehearsal}
                                    </span>
                                </div>
                            )}
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}></div>
                        <div className={styles.columnFiller} />
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.ratingBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>
                            How confident are you in your ability to use the strategies you
                            selected? (0-100)
                        </div>
                        <div className={styles.item}>{numOrDash(answers.stabilityConfidence)}</div>
                    </div>
                    <div className={styles.divider} />
                    <div className={styles.riskBlock}>
                        <div className={styles.columnFiller} />
                        <div className={styles.boldItem}>
                            How ready to leave the emergency room are you feeling?
                        </div>
                        <div className={styles.columnFiller} />
                        <div className={styles.item}>{allCaps(answers.readiness)}</div>
                        <div className={styles.columnFiller} />
                    </div>
                    {['Not at all ready', 'Somewhat ready'].includes(answers.readiness) && (
                        <>
                            <div className={styles.divider} />
                            <div className={styles.riskDescriptionBlock}>
                                <div className={styles.columnFiller} />
                                <div>
                                    <div className={styles.boldItem}>
                                        What would make you feel more ready?
                                    </div>
                                    {answers.readinessNo && (
                                        <div className={styles.item}>
                                            Describe:{' '}
                                            <span className={styles.italicsItemQuotes}>
                                                {answers.readinessNo}
                                            </span>
                                        </div>
                                    )}
                                </div>
                                <div className={styles.columnFiller} />
                                <div className={styles.item}></div>
                                <div className={styles.columnFiller} />
                            </div>
                        </>
                    )}
                    {answers.readiness === 'Very ready' && (
                        <>
                            <div className={styles.divider} />
                            <div className={styles.riskDescriptionBlock}>
                                <div className={styles.columnFiller} />
                                <div>
                                    <div className={styles.boldItem}>
                                        What makes you feel very ready? Check all that apply.
                                    </div>
                                    {answers.readinessYesReasons && (
                                        <div className={styles.item}>
                                            Describe:{' '}
                                            <span>{answers.readinessYesReasons?.join(', ')}</span>
                                        </div>
                                    )}
                                </div>
                                <div className={styles.columnFiller} />
                                <div className={styles.item}></div>
                                <div className={styles.columnFiller} />
                            </div>
                        </>
                    )}
                    {answers.readiness === 'Very ready' && (
                        <>
                            <div className={styles.divider} />
                            <div className={styles.riskDescriptionBlock}>
                                <div className={styles.columnFiller} />
                                <div>
                                    <div className={styles.boldItem}>
                                        What has changed since you arrived at the emergency room?
                                    </div>
                                    {answers.readinessYesChanged && (
                                        <div className={styles.item}>
                                            Describe:{' '}
                                            <span className={styles.italicsItemQuotes}>
                                                {answers.readinessYesChanged}
                                            </span>
                                        </div>
                                    )}
                                </div>
                                <div className={styles.columnFiller} />
                                <div className={styles.item}></div>
                                <div className={styles.columnFiller} />
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CamsSummary;
