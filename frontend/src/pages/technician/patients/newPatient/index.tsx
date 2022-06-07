import React, { useState, useContext, useEffect } from 'react';
import useAxios from 'lib/useAxios';
import Segment, { AnalyticNames } from 'lib/segment';
import { getLocations } from 'state/actions/user';
import { GetResponse as PreferenceGetResponse } from 'state/types/api/technician/preferences';
import Button from 'components/Button';
import Checkbox from 'components/Checkbox';
import DateInput from 'components/DateInput';
import styles from './index.module.scss';
import StoreContext from 'state/context/store';
import Alert from 'assets/icons/Alert';
import {
    GetResponse as GetPatientsResponse,
    PostResponse,
} from 'state/types/api/technician/patients';
import { GetResponse as GetPatientResponse } from 'state/types/api/technician/patients/_id';
import { Technician } from 'state/types';

interface NewPatientProps {
    close: () => void;
    patients: GetPatientsResponse;
    setPatients: (patients: GetPatientsResponse) => void;
    setSearchValue: (searchValue: string) => void;
    setShowNewEncounter: (patient: GetPatientResponse | null) => void;
}

const NewPatient = ({
    close,
    patients,
    setPatients,
    setSearchValue,
    setShowNewEncounter,
}: NewPatientProps) => {
    const axios = useAxios();
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { token, locations = [], userType } = user as Technician;
    const [screen, setScreen] = useState<'patient' | 'activities'>('patient');
    const [error, setError] = useState('');
    const [location, setLocation] = useState<number | ''>(); // TODO Why do I set this to blank instead of null?
    const [ssid /*setSsid*/] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [dob, setDob] = useState('');
    const [mrn, setMrn] = useState('');
    const [csa, setCsa] = useState(false);
    const [csp, setCsp] = useState(false);
    const [skills, setSkills] = useState(false);
    const [preferences, setPreferences] = useState<PreferenceGetResponse>({
        timezone: 'America/New_York',
        providerNotes: false,
        stabilityPlanLabel: 'Stability Plan',
    });

    // Get preferences
    useEffect(() => {
        (async () => {
            if (location) {
                const response = await axios.get<PreferenceGetResponse>(
                    `/technician/preferences?department=${location}`,
                );
                setPreferences(response.data);
            }
        })();
    }, [axios, location]);

    useEffect(() => {
        if (userType === 'technician' && token) {
            getLocations(dispatch);
        }
    }, [token, dispatch, userType]);

    useEffect(() => {
        // If only one location listed, set it automatically
        if (locations?.length === 1) {
            setLocation(locations[0].id);
        }
    }, [locations]);

    useEffect(() => {
        if (csp) {
            // Crisis Stability Plan requires comfort and skills to be enabled
            setSkills(true);
        }
    }, [csp]);

    const changeLocation = ({ target }: React.ChangeEvent<HTMLSelectElement>) => {
        setLocation(parseInt(target.value, 10) || '');
        if (error?.indexOf('SSIDs') === -1) {
            // Set the error to empty when they update the location if it's blank or valid.
            setError('');
        }
    };

    const confirm = (e: TouchEvent | MouseEvent | React.FormEvent<HTMLFormElement>) => {
        e && e.preventDefault();
        if (ssid && (firstName || lastName || mrn || dob)) {
            setError(
                'Patients cannot have an SSID AND any of the following fields: First name, Last name, DOB, MRN',
            );
        } else {
            if (screen === 'patient') {
                setScreen('activities');
            } else {
                if (!(skills || csp || csa)) {
                    setError('You must select at least one activity to create a patient path.');
                } else {
                    onSubmit();
                }
            }
        }
    };

    const onSubmit = async () => {
        const payload = ssid
            ? {
                  ssid,
                  department: location,
                  activities: {
                      csp,
                      csa,
                      skills,
                  },
              }
            : {
                  firstName,
                  lastName,
                  dateOfBirth: dob,
                  mrn,
                  department: location,
                  activities: {
                      csp,
                      csa,
                      skills,
                  },
              };

        try {
            const response = await axios.post<PostResponse>(`/technician/patients`, {
                ...payload,
            });

            const json = response.data;

            Segment.track(AnalyticNames.CREATE_PATIENT, {
                department: payload.department,
                patient: json.analyticsToken,
                activities: { csp, csa, skills },
            });
            setPatients([json, ...patients]);
            close();
        } catch (err) {
            const response = err.response;
            if (response?.status === 400) {
                const json: {
                    nonFieldErrors?: string[];
                    ssid?: string[];
                    department?: string[];
                    dateOfBirth?: string[];
                } = response.data;
                if (json.ssid?.length > 0) {
                    setError(json.ssid[0]);
                } else if (json.department?.length > 0) {
                    setError(json.department[0]);
                } else if (json.dateOfBirth?.length) {
                    setError(json.dateOfBirth[0]);
                } else if (json.nonFieldErrors?.length > 0) {
                    setError(json.nonFieldErrors[0]);
                } else {
                    setError('There was an unknown error');
                }
                setScreen('patient');
            } else if (response?.status === 409) {
                const json = response.data;
                const idx = patients.findIndex((patient) => patient.id === json.object.id);
                if (idx === -1) {
                    setPatients([...patients, json.object]);
                }
                setShowNewEncounter(json.object.id);
                Segment.track(AnalyticNames.TECHNICIAN_TRIED_TO_CREATE_DUPLICATE_PATIENT);
                close();
            } else {
                setError('There was an unknown error');
            }
        }
    };

    return (
        <form className={styles.newPatient} onSubmit={confirm}>
            {screen === 'patient' && (
                <div className={styles.outer}>
                    <h4 className={styles.header}>Create New Patient</h4>
                    <div className={`typography--body1 ${styles.subheader}`}>
                        Enter patient details.
                    </div>
                    <div className={styles.container}>
                        <div className={styles.row}>
                            <label className={`typography--body1 ${styles.label}`}>
                                <span className={styles.formLabel}>First Name</span>
                                <input
                                    className={styles.input}
                                    value={firstName}
                                    onChange={({ target }) => setFirstName(target.value)}
                                    required
                                />
                            </label>

                            <label className={`typography--body1 ${styles.label}`}>
                                <span className={styles.formLabel}>Last Name</span>
                                <input
                                    className={styles.input}
                                    value={lastName}
                                    onChange={({ target }) => setLastName(target.value)}
                                    required
                                />
                            </label>

                            <label className={`typography--body1 ${styles.label}`}>
                                <span className={styles.formLabel}>Clinic Location</span>
                                <select
                                    value={location}
                                    onChange={changeLocation}
                                    className={styles.select}
                                    required
                                >
                                    <option className={styles.option} value=""></option>
                                    {locations?.map(({ id, name }) => (
                                        <option className={styles.option} key={id} value={id}>
                                            {name}
                                        </option>
                                    ))}
                                </select>
                            </label>
                        </div>

                        <div className={styles.row} style={{ marginBottom: '1.6rem' }}>
                            <label className={`typography--body1 ${styles.label}`}>
                                <span className={styles.formLabel}>Date of Birth</span>
                                <DateInput
                                    required
                                    className={styles.input}
                                    value={dob}
                                    onChange={(value) => setDob(value)}
                                />
                            </label>
                            <label className={`typography--body1 ${styles.label}`}>
                                <span className={styles.formLabel}>Medical Record Number</span>
                                <input
                                    required
                                    className={styles.input}
                                    value={mrn}
                                    onChange={({ target }) => setMrn(target.value)}
                                />
                            </label>
                            {/*(
                            <label className={`typography--body1 ${styles.label}`}>
                                <span className={styles.formLabel}>SSID</span>
                                <input
                                    required
                                    pattern="^[a-zA-Z0-9_]*$"
                                    className={styles.input}
                                    onChange={(e) => setSsid(e.target.value)}
                                    value={ssid}
                                    maxLength={25}
                                />
                            </label>
                            )*/}
                        </div>
                        <div className={styles.error}>
                            <span className="typography--caption">{error}</span>
                        </div>
                        <div className={styles.buttons}>
                            <Button variant="tertiary" onClick={close}>
                                Cancel
                            </Button>
                            <Button type="submit" dark>
                                Continue
                            </Button>
                        </div>
                    </div>
                </div>
            )}
            {screen === 'activities' && (
                <div className={styles.outer}>
                    <h4 className={styles.header}>Create New Patient</h4>
                    <div className={`typography--body1 ${styles.subheader}`}>
                        Select one or more activities for the patient to complete. You can always
                        add additional activities as a later time.
                    </div>
                    <div className={`${styles.row} ${styles.selectActivities}`}>
                        <div className={styles.selector}>
                            <Checkbox
                                large
                                checked={skills}
                                disabled={csp}
                                onChange={({ target }) => setSkills(target.checked)}
                            />
                            <div className={styles.column}>
                                <h6>Comfort &amp; Skills</h6>
                                <span>
                                    Activities, calming videos, and shared stories to enable to
                                    patient to wait well.
                                </span>
                            </div>
                        </div>
                        <div className={styles.selector}>
                            <Checkbox
                                large
                                checked={csp}
                                onChange={({ target }) => setCsp(target.checked)}
                            />
                            <div className={styles.column}>
                                <h6>Patient {preferences.stabilityPlanLabel}</h6>
                                <span>
                                    Guides creation of coping plan for suicidal urges and emotional
                                    distress.
                                </span>
                            </div>
                        </div>
                        <div className={styles.selector}>
                            <Checkbox
                                large
                                checked={csa}
                                onChange={({ target }) => setCsa(target.checked)}
                            />
                            <div className={styles.column}>
                                <h6>Comprehensive Suicide Assessment</h6>
                                <span>
                                    Helps patient tell their story, gathers risk and protective
                                    factors.
                                </span>
                            </div>
                        </div>
                        {Boolean(error) && (
                            <div className={styles.error} style={{ paddingLeft: '2.6rem' }}>
                                <Alert />
                                <div style={{ marginLeft: '2.6rem' }}>
                                    Unable to create patient
                                    <br />
                                    <span className="typography--caption">{error}</span>
                                </div>
                            </div>
                        )}
                    </div>
                    <div className={styles.buttons}>
                        <Button variant="tertiary" onClick={() => setScreen('patient')}>
                            Cancel
                        </Button>
                        <Button type="submit" dark>
                            Create Patient
                        </Button>
                    </div>
                </div>
            )}
        </form>
    );
};

export default NewPatient;
