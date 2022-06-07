import React, { useContext, useEffect, useState } from 'react';
import { DateTime } from 'luxon';
import Sentry from 'lib/sentry';
import { Link, useLocation, useRouteMatch } from 'lib/router';
import { activatePatientFromPin, logout } from 'state/actions/user';
import StoreContext from 'state/context/store';
import logo from 'assets/logo.svg';
import styles from './index.module.scss';
import { useHistory } from 'lib/router';
import Button from 'components/Button';
import { Device } from 'state/types';
import { setDevice } from 'state/actions/device';
import Segment, { AnalyticNames } from 'lib/segment';

const PIN_LENGTH = 6;

const formatDate = (date: string) => {
    const processedDate = DateTime.fromISO(date);
    if (!processedDate.isValid) return '';
    return processedDate.toLocaleString(DateTime.DATE_MED);
};

const StartPatientSession = () => {
    const history = useHistory();
    const location = useLocation();
    const routeMatch = useRouteMatch<{ codeType: 'department' | 'system'; code: string }>();
    const [store, dispatch] = useContext(StoreContext);
    const [pin, setPin] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState('');
    const [showDiagnostics, setShowDiagnostics] = useState(false);
    const [config, setConfig] = useState({ codeType: '', code: '' });
    const [patient, setPatient] = useState<{
        dateOfBirth?: string;
        location?: {
            system: { id: number; name: string };
            clinic: { id: number; name: string };
            department: { id: number; name: string };
        };
        firstName?: string;
        lastName?: string;
        ssid?: string;
        mrn?: string;
    }>(null);
    const [technicianOperated, setTechnicianOperated] = useState(false);
    // @ts-ignore
    const appInstalled = 'standalone' in window.navigator && window.navigator['standalone'];

    /** If there is an application update and the user has not begun to interact with the app
     * then automatically update to the latest version
     */
    useEffect(() => {
        if (store.device.updateAvailable && !patient && !pin && !error) {
            window.location.reload();
        }
    }, [error, patient, pin, store.device.updateAvailable]);

    useEffect(() => {
        if (routeMatch.params.code && routeMatch.params.codeType) {
            const device: Device = {
                isTablet: true,
                code: routeMatch.params.code,
                codeType: routeMatch.params.codeType,
            };
            setDevice(dispatch, device);
            Segment.track(AnalyticNames.SET_DEVICE, device);
            window.sessionStorage.setItem('code', routeMatch.params.code);
            window.sessionStorage.setItem('codeType', routeMatch.params.codeType);
        }
    }, [dispatch, routeMatch.params]);

    const submit = async () => {
        if (pin.length !== 6) {
            setError('Please enter in the full PIN');
            return;
        }
        setError('');
        setSubmitting(true);
        try {
            const code = store.device?.code ?? null;
            const codeType = store.device?.codeType ?? null;
            const response = await activatePatientFromPin(
                dispatch,
                routeMatch.params.codeType,
                routeMatch.params.code,
                pin,
            );
            if (response.status === 200) {
                setPatient(response.data.patient);
                setTechnicianOperated(response.data.technicianOperated);
                setSubmitting(false);
                setPin('');
                setError('');
            } else if (response.status === 401) {
                setError(`Tablet not configured for ${codeType} ${code}`);
                setSubmitting(false);
                setPin('');
                Sentry.captureException(
                    `There was an error submitting pin ${pin} for ${codeType} ${code}`,
                );
            } else {
                const error =
                    response.data.departmentCode?.[0] ||
                    response.data.pinCode?.[0] ||
                    response.data.nonFieldErrors?.[0];
                if (error) {
                    setError(
                        response.data.departmentCode?.[0] ||
                            response.data.pinCode?.[0] ||
                            response.data.nonFieldErrors?.[0],
                    );
                } else {
                    // A valid but unknown response from the server (e.g. an unaccounted for 400 error)
                    setError(`There was an unknown error with code: ${response.status}`);
                    Sentry.captureException(
                        `There was an error submitting pin ${pin} for department ${codeType} ${code} with response ${
                            response.status
                        } ${response.data.toString()}`,
                    );
                }

                setSubmitting(false);
                setPin('');
            }
        } catch (err) {
            // Connection issues with the server (CORS, timeout, no internet)
            setSubmitting(false);
            const code = store.device?.code ?? null;
            const codeType = store.device?.codeType ?? null;

            if (err.code === 'ECONNABORTED') {
                setError('Request timed out waiting for the server.');
            } else if (err.response === undefined) {
                console.log('code', err.code);
                setError('Unable to connect to server.');
            } else {
                setError('There was an unexpected error.');
            }

            Sentry.captureException(
                `There was an error submitting pin ${pin} for ${codeType} with code ${code} ${err.code} and message ${err.message}`,
            );
        }
    };

    const confirm = () => {
        history.replace('/');
    };

    const change = ({ target }: React.ChangeEvent<HTMLInputElement>) => {
        const newPin = target.value.trim().toUpperCase();
        setPin(newPin);
        setError('');
    };

    const setConfiguration = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (config.codeType && config.code) {
            // We want to ensure the browser reloads so that the manifest gets set and loaded within the 5 second browser limit
            window.location.href = `${window.location.origin}/start-patient-session/${config.codeType}/${config.code}`;
        }
    };

    return (
        <div className={styles.startPatientSession}>
            {patient && (
                <div className={styles.verification}>
                    <section className={styles.section}>
                        <img src={logo} alt="" />
                        <h3>Verify Patient Information</h3>
                        <div className={styles.details}>
                            <div className={styles.row}>
                                <div className={styles.column}>
                                    <span className={`${styles.field} typography--h5`}>
                                        Name of Patient
                                    </span>
                                    <span className={styles.value}>
                                        {patient.firstName} {patient.lastName}{' '}
                                        {!patient.firstName && !patient.lastName && '-'}
                                    </span>
                                </div>
                                <div className={styles.column}>
                                    <span className={`${styles.field} typography--h5`}>MRN</span>
                                    <span className={styles.value}>{patient.mrn}</span>
                                </div>
                            </div>
                            <div className={styles.row}>
                                <div className={styles.column}>
                                    <span className={`${styles.field} typography--h5`}>
                                        Date of Birth
                                    </span>
                                    <span className={styles.value}>
                                        {formatDate(patient.dateOfBirth) || '-'}
                                    </span>
                                </div>

                                <div className={styles.column}>
                                    <span className={`${styles.field} typography--h5`}>Clinic</span>
                                    <span
                                        className={styles.value}
                                    >{`${patient.location?.clinic?.name} - ${patient.location?.department?.name}`}</span>
                                </div>
                            </div>
                            {technicianOperated && (
                                <div className={styles.row}>
                                    <div className={styles.column}>
                                        <h6 style={{ margin: 0 }}>
                                            Going directly to Safety/Stability Planning
                                        </h6>
                                        <span
                                            className="typography--body2"
                                            style={{ color: 'rgba(184, 188, 204, 1)' }}
                                        >
                                            Patient will not use tablet
                                        </span>
                                    </div>
                                </div>
                            )}
                            <div className={styles.buttons}>
                                <button
                                    className={styles.textButton}
                                    onClick={() => {
                                        logout(dispatch);
                                        setPatient(null);
                                    }}
                                >
                                    Cancel
                                </button>
                                <Button onClick={confirm}>Confirm</Button>
                            </div>
                        </div>
                    </section>
                    <section className={`${styles.section} ${styles.prompts}`}>
                        <h3>Jaspr Health Script</h3>
                        <span className="typography--h5">
                            Suggested Prompts for Introducing the App
                        </span>
                        <ol>
                            <li>"We're so glad you're here."</li>
                            <li>"This may be a while."</li>
                            <li>"Here is what you've told me."</li>
                            <li>"I think Jaspr may help."</li>
                            <li>"Would you like to give it a try?"</li>
                        </ol>
                    </section>
                </div>
            )}
            {!patient && (
                <>
                    <img src={logo} alt="" />
                    {routeMatch.params.codeType && routeMatch.params.code && (
                        <div className={styles.center}>
                            <>
                                <span
                                    className={styles.instructions}
                                    style={{ visibility: submitting ? 'hidden' : 'visible' }}
                                >
                                    Enter in 6-digit code:
                                </span>
                                <input
                                    autoComplete="off"
                                    autoCapitalize="characters"
                                    autoFocus
                                    maxLength={PIN_LENGTH}
                                    value={pin}
                                    onChange={change}
                                    pattern="[A-Za-z1-9]{5}"
                                />

                                <div
                                    className={styles.input}
                                    style={{ visibility: submitting ? 'hidden' : 'visible' }}
                                >
                                    {Array.from(Array(PIN_LENGTH)).map((_, idx) => (
                                        <span className={styles.digit} key={idx}>
                                            {pin[idx]}
                                        </span>
                                    ))}
                                </div>
                                {!submitting && <Button onClick={submit}>Submit</Button>}
                                {submitting && (
                                    <span className={styles.validating}>Validating Pin...</span>
                                )}
                                {!store.user?.online && (
                                    <div className={styles.error}>
                                        Your device is not connected to the internet. Unable to
                                        submit PIN.
                                    </div>
                                )}

                                <div className={styles.error}>{error}</div>
                            </>
                        </div>
                    )}
                    {(!routeMatch.params.codeType || !routeMatch.params.code) && (
                        <div className={styles.notConfigured}>
                            <span className={styles.setupInstructions}>
                                Your device is not configured for PIN activations. Please contact
                                your JASPR IT support person. If you know your configuration CODE,
                                you may enter it below.
                            </span>
                            <form onSubmit={setConfiguration}>
                                <label>
                                    Code Type
                                    <select
                                        value={config.codeType}
                                        onChange={(e) =>
                                            setConfig((config) => ({
                                                ...config,
                                                codeType: e.target.value,
                                            }))
                                        }
                                    >
                                        <option></option>
                                        <option value="system">System</option>
                                        <option value="department">Department</option>
                                    </select>
                                </label>
                                <label>
                                    Code
                                    <input
                                        type="text"
                                        value={config.code}
                                        onChange={(e) =>
                                            setConfig((config) => ({
                                                ...config,
                                                code: e.target.value,
                                            }))
                                        }
                                    />
                                </label>
                                <Button type="submit">Set Configuration</Button>
                            </form>
                        </div>
                    )}
                    <Link
                        to={{ pathname: '/login', search: location.search }}
                        className={styles.goLogin}
                    >
                        Go to Login
                    </Link>
                    <div
                        className={styles.diagnostics}
                        style={{ display: showDiagnostics ? 'flex' : 'none' }}
                    >
                        <span>Tablet: {store.device?.isTablet.toString()}</span>
                        <span>App Installed: {appInstalled ? 'True' : 'False'}</span>
                        <span>Code: {store.device?.code}</span>
                        <span>Code Type: {store.device?.codeType}</span>
                        <span>
                            Version:
                            {` ${process.env.REACT_APP_VERSION}.${process.env.REACT_APP_BUILD_NUMBER}`}
                        </span>
                    </div>
                    <span
                        className={styles.infoIcon}
                        onClick={() => {
                            setShowDiagnostics((showDiagnostics) => !showDiagnostics);
                        }}
                    >
                        ⓘ
                    </span>
                </>
            )}
        </div>
    );
};

export default StartPatientSession;
