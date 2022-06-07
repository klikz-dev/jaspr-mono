import React, { useState, useContext, useEffect } from 'react';
import useAxios from 'lib/useAxios';
import Modal, { Styles } from 'react-modal';
import Confirm from '../Confirm';
import ConfirmMove from '../ConfirmMove';
import ConfirmJahCredentials from '../ConfirmJahCredentials';
import { getLocations } from 'state/actions/user';
import Button from 'components/Button';
import DateInput from 'components/DateInput';
import zIndexHelper from 'lib/zIndexHelper';
import styles from './index.module.scss';
import StoreContext from 'state/context/store';
import Segment, { AnalyticNames } from 'lib/segment';
import { Technician } from 'state/types';
import { PutResponse } from 'state/types/api/technician/patients/_id';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(0,0,0,0.4)',
        zIndex: zIndexHelper('technician.edit-patient'),
    },
    content: {
        position: 'relative',
        display: 'flex',
        justifyContent: 'space-around',
        flexDirection: 'column',
        border: 'none',
        backgroundColor: '#ffffff',
        padding: 35,
        maxWidth: '688px',
        width: '95%',
        boxShadow: '0px 1px 4px rgba(0, 0, 0, 0.25)',
        overflow: 'hidden',
        inset: 'inherit',
        borderRadius: 3,
    },
};

interface Patient {
    id?: number;
    departments?: number[];
    firstName?: string;
    lastName?: string;
    mrn?: string;
    ssid?: string;
    email?: string;
    mobilePhone?: string;
    dateOfBirth?: string;
    toolsToGoStatus?: 'Not Started' | 'Email Sent' | 'Phone Number Verified' | 'Setup Finished';
    tourComplete?: boolean;
}

interface EditPatientProps {
    patient: PutResponse;
    setPatient: (patient: PutResponse) => void;
    close: () => void;
}

const EditPatient = ({ setPatient, patient, close }: EditPatientProps) => {
    const axios = useAxios();
    const [store, dispatch] = useContext(StoreContext);
    const { user } = store;
    const { token, locations, userType } = user as Technician;
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [showConfirmationMove, setShowConfirmationMove] = useState(false);
    const [showConfirmJahCredentials, setShowConfirmJahCredentials] = useState(false);
    const [error, setError] = useState('');
    const [location, setLocation] = useState<number>();
    const [id, setId] = useState<number>(null);
    const [ssid, setSsid] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [dateOfBirth, setDateOfBirth] = useState('');
    const [mrn, setMrn] = useState('');
    const [mobilePhone, setMobilePhone] = useState('');
    const [email, setEmail] = useState('');

    const jahCredentialsEditable = patient?.toolsToGoStatus === 'Email Sent';
    const jahCredentialsUpdated =
        jahCredentialsEditable &&
        ((mobilePhone && mobilePhone !== patient?.mobilePhone) ||
            (email && email !== patient?.email));

    useEffect(() => {
        if (id !== patient?.id) {
            setError('');
            setId(patient.id);
            setLocation(patient.departments?.[0]);
            setSsid(patient.ssid || '');
            setFirstName(patient.firstName || '');
            setLastName(patient.lastName || '');
            setDateOfBirth(patient.dateOfBirth || '');
            setMrn(patient.mrn);
            setMobilePhone(patient.mobilePhone || '');
            setEmail(patient.email || '');
        }
    }, [id, patient]);

    useEffect(() => {
        if (userType === 'technician' && token) {
            getLocations(dispatch);
        }
    }, [token, dispatch, userType]);

    const cancelConfirmation = () => {
        setShowConfirmation(false);
        setShowConfirmationMove(false);
        setShowConfirmJahCredentials(false);
        Segment.track(AnalyticNames.TECHNICIAN_CANCELED_EDITING_PATIENT);
    };

    const isValidDate = () => {
        const date = new Date(dateOfBirth);
        return date instanceof Date && !isNaN(date as any);
    };

    const confirm = (e: React.FormEvent<HTMLFormElement>) => {
        e && e.preventDefault();
        if (!location) {
            setError('Department is required');
        } else if (ssid && (firstName || lastName || mrn || dateOfBirth)) {
            setError(
                'Patients cannot have an SSID AND any of the following fields: First name, Last name, Date of Birth, MRN',
            );
        } else if (!ssid && !firstName) {
            setError('First Name is required');
        } else if (!ssid && !lastName) {
            setError('Last Name is required');
        } else if (!ssid && !dateOfBirth) {
            setError('Date of Birth is required');
        } else if (!ssid && !isValidDate()) {
            setError('Please enter date in the format MM/DD/YYYY');
        } else if (!ssid && !mrn) {
            setError('Medical Record Number is required');
        } else {
            if (patient?.departments?.[0] !== location) {
                setShowConfirmationMove(true);
            } else if (jahCredentialsUpdated) {
                setShowConfirmJahCredentials(true);
            } else {
                setShowConfirmation(true);
            }
        }
    };

    const confirmMove = () => {
        setShowConfirmationMove(false);

        if (jahCredentialsUpdated) {
            setShowConfirmJahCredentials(true);
            setShowConfirmation(false);
        } else {
            setShowConfirmJahCredentials(false);
            setShowConfirmation(true);
        }
    };

    const confirmCredentials = () => {
        setShowConfirmationMove(false);
        setShowConfirmJahCredentials(false);
        setShowConfirmation(true);
    };

    const changeLocation = ({ target }: React.ChangeEvent<HTMLSelectElement>) => {
        const locationId = parseInt(target.value, 10);
        if (locationId) {
            setLocation(locationId);
        } else {
            setLocation(null);
        }
    };

    /*const updateSSID = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!/^[-a-zA-Z0-9_]*$/.test(e.target.value)) {
            // Set the error if the SSID isn't blank and isn't valid.
            setError('SSIDs can only contain letters, numbers, hyphens, and underscores.');
        } else {
            // Set the error to empty when they update the SSID if it's blank or valid.
            setError('');
        }
        setSsid(e.target.value);
    };*/

    const submit = async () => {
        const formatDob = () => {
            return new Date(dateOfBirth).toISOString().substring(0, 10);
        };

        try {
            const payload: Patient = ssid
                ? {
                      ssid,
                      departments: [location],
                  }
                : {
                      firstName,
                      lastName,
                      dateOfBirth: formatDob(),
                      mrn,
                      departments: [location],
                  };

            // Only include JAH Credentials if they have been changed and are set
            if (jahCredentialsUpdated) {
                payload.mobilePhone = mobilePhone;
                payload.email = email;
                Segment.track(AnalyticNames.TECHNICIAN_UPDATED_PATIENT_JAH_CREDENTIALS);
            }

            const response = await axios.put<PutResponse>(`/technician/patients/${patient.id}`, {
                id: patient.id,
                ...payload,
            });

            const json = response.data;
            setPatient(json);

            Segment.track(AnalyticNames.TECHNICIAN_EDITED_PATIENT, {
                department: json.departments?.[0],
                ssid: json.ssid,
            });

            close(); // Close modal
        } catch (err) {
            const { response } = err;
            if (response?.status === 400) {
                cancelConfirmation();
                const json = response.data;
                if (json.ssid?.length > 0) {
                    setError(json.ssid[0]);
                } else if (json.departments?.length > 0) {
                    setError(json.departments[0]);
                } else if (json.dateOfBirth?.length) {
                    setError(json.dateOfBirth[0]);
                } else if (json.email?.length) {
                    setError(json.email[0]);
                } else if (json.mobilePhone?.length) {
                    setError(json.mobilePhone[0]);
                } else if (json.nonFieldErrors?.length > 0) {
                    setError(json.nonFieldErrors[0]);
                } else {
                    setError('There was an unknown error');
                }
            } else if (response?.status === 500) {
                setError('There was an unknown error');
            }

            return response;
        }
    };

    return (
        <Modal isOpen style={modalStyle}>
            <form className={styles.editPatient} onSubmit={confirm}>
                {showConfirmation && !showConfirmationMove && !showConfirmJahCredentials && (
                    <Confirm
                        //@ts-ignore
                        submit={submit}
                        cancel={cancelConfirmation}
                        location={locations.find(({ id }) => id === location)?.name}
                        ssid={ssid}
                        firstName={firstName}
                        lastName={lastName}
                        dob={dateOfBirth}
                        mrn={mrn}
                        edit
                    />
                )}

                {!showConfirmation && showConfirmationMove && !showConfirmJahCredentials && (
                    <ConfirmMove
                        from={locations.find(({ id }) => id === patient?.departments?.[0])?.name}
                        to={locations.find(({ id }) => id === location)?.name}
                        firstName={firstName}
                        lastName={lastName}
                        ssid={ssid}
                        mrn={mrn}
                        submit={confirmMove}
                        cancel={close}
                    />
                )}

                {!showConfirmation && !showConfirmationMove && showConfirmJahCredentials && (
                    <ConfirmJahCredentials
                        submit={confirmCredentials}
                        cancel={close}
                        ssid={ssid}
                        firstName={firstName}
                        lastName={lastName}
                        email={email}
                        mobilePhone={mobilePhone}
                        mrn={mrn}
                    />
                )}

                {!showConfirmation && !showConfirmationMove && !showConfirmJahCredentials && (
                    <div className={styles.outer}>
                        <h4 className={styles.header}>Edit Patient Information</h4>
                        <div className={`typography--body1 ${styles.subheader}`}>
                            Enter patient details.
                        </div>
                        <div className={styles.container}>
                            <div className={styles.row}>
                                <label className={styles.label}>
                                    <span className={styles.formLabel}>First Name</span>
                                    <input
                                        required
                                        className={styles.input}
                                        value={firstName}
                                        onChange={({ target }) => setFirstName(target.value)}
                                    />
                                </label>

                                <label className={styles.label}>
                                    <span className={styles.formLabel}>Last Name</span>
                                    <input
                                        required
                                        className={styles.input}
                                        value={lastName}
                                        onChange={({ target }) => setLastName(target.value)}
                                    />
                                </label>

                                <label className={styles.label}>
                                    <span className={styles.formLabel}>Clinic Location</span>
                                    <select
                                        required
                                        value={location}
                                        onChange={changeLocation}
                                        className={styles.select}
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

                            <div className={styles.row}>
                                <label className={styles.label}>
                                    <span className={styles.formLabel}>Date of Birth</span>
                                    <DateInput
                                        required
                                        className={styles.input}
                                        value={dateOfBirth || ''}
                                        onChange={(value) => setDateOfBirth(value)}
                                    />
                                </label>

                                <label className={styles.label}>
                                    <span className={styles.formLabel}>Medical Record Number</span>
                                    <input
                                        required
                                        className={styles.input}
                                        value={mrn || ''}
                                        onChange={({ target }) => setMrn(target.value)}
                                    />
                                </label>

                                {/*
                                <label className={styles.label}>
                                    <span className={styles.formLabel}>SSID</span>
                                    <input
                                        className={styles.input}
                                        onChange={updateSSID}
                                        placeholder="SSID"
                                        value={ssid || ''}
                                        maxLength={25}
                                    />
                                </label>
                                */}
                            </div>

                            {patient?.tourComplete && ( // JAH Credentials can only be set after a patient has finished onboarding
                                <>
                                    <div
                                        className={styles.header}
                                        style={{
                                            alignSelf: 'flex-start',
                                            padding: '13px 0px 10px',
                                        }}
                                    >
                                        Jaspr at Home Credentials
                                    </div>

                                    <div className={styles.row}>
                                        <label
                                            className={styles.label}
                                            style={{
                                                flex: 2,
                                                width: 'auto',
                                                marginRight: 20,
                                                maxWidth: 390,
                                            }}
                                        >
                                            <span className={styles.formLabel}>Email</span>
                                            <input
                                                className={styles.input}
                                                readOnly={!jahCredentialsEditable}
                                                disabled={!jahCredentialsEditable}
                                                placeholder="Email"
                                                value={email}
                                                onChange={({ target }) => setEmail(target.value)}
                                                type="email"
                                                autoComplete="off"
                                                autoCapitalize="off"
                                            />
                                        </label>

                                        <label
                                            className={styles.label}
                                            style={{ marginRight: 'auto' }}
                                        >
                                            <span className={styles.formLabel}>Phone Number</span>
                                            <input
                                                className={styles.input}
                                                readOnly={!jahCredentialsEditable}
                                                disabled={!jahCredentialsEditable}
                                                onChange={({ target }) =>
                                                    setMobilePhone(target.value)
                                                }
                                                placeholder="Phone Number"
                                                value={mobilePhone}
                                                maxLength={25}
                                                type="tel"
                                                autoComplete="off"
                                                autoCapitalize="off"
                                            />
                                        </label>
                                    </div>
                                </>
                            )}
                        </div>

                        <div className={styles.error}>{error}</div>
                        <div className={styles.buttons}>
                            <Button variant="tertiary" onClick={close}>
                                Cancel
                            </Button>
                            <Button type="submit" dark>
                                Submit
                            </Button>
                        </div>
                    </div>
                )}
            </form>
        </Modal>
    );
};

export default EditPatient;
