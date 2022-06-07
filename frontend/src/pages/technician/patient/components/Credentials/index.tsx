import React, { useEffect, useState } from 'react';
import useAxios from 'lib/useAxios';
import { useHistory } from 'lib/router';
import Modal from 'components/Modal';
import Button from '../Button';
import styles from './index.module.scss';
import ConfirmationJAHCredentials from '../ConfirmJahCredentials';
import { PutResponse } from 'state/types/api/technician/patients/_id';
import Segment, { AnalyticNames } from 'lib/segment';

interface CredentialsProps {
    patient: PutResponse;
    setPatient: (patient: PutResponse) => void;
}

const Credentials = ({ patient, setPatient }: CredentialsProps) => {
    const axios = useAxios();
    const history = useHistory();
    const [email, setEmail] = useState(patient?.email ?? '');
    const [mobilePhone, setMobilePhone] = useState(patient?.mobilePhone ?? '');
    const [showConfirmation, setShowConfirmation] = useState(false);

    const close = () => history.replace(`/technician/patients/${patient.id}`);

    const confirm = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setShowConfirmation(true);
    };

    const submit = async () => {
        const response = await axios.put<PutResponse>(`/technician/patients/${patient.id}`, {
            ...patient,
            mobilePhone,
            email,
        });
        if (response.status === 200) {
            setPatient(response.data);
            Segment.track(AnalyticNames.TECHNICIAN_UPDATED_PATIENT_JAH_CREDENTIALS);
            close();
        }

        // TODO handle non 200 responses
    };

    useEffect(() => {
        setEmail(patient.email);
        setMobilePhone(patient.mobilePhone);
    }, [patient.email, patient.mobilePhone]);

    return (
        <Modal isOpen style={{ content: { maxHeight: 389 } }}>
            <>
                <div className={styles.credentials}>
                    <div className={styles.close} onClick={close}>
                        ⨉
                    </div>
                    {!showConfirmation && (
                        <>
                            <h3>Jaspr at Home Credentials</h3>
                            <form onSubmit={confirm}>
                                <label>
                                    Email
                                    <input
                                        required
                                        type="email"
                                        autoComplete="off"
                                        autoCapitalize="off"
                                        autoFocus
                                        value={email}
                                        onChange={({ target }) => setEmail(target.value)}
                                    />
                                </label>
                                <label>
                                    Phone Number
                                    <input
                                        required
                                        type="tel"
                                        autoComplete="off"
                                        autoCapitalize="off"
                                        value={mobilePhone}
                                        onChange={({ target }) => setMobilePhone(target.value)}
                                    />
                                </label>
                                <Button label="Save" />
                            </form>
                        </>
                    )}
                </div>
                {showConfirmation && (
                    <ConfirmationJAHCredentials
                        {...patient}
                        mobilePhone={mobilePhone}
                        email={email}
                        submit={submit}
                        cancel={close}
                    />
                )}
            </>
        </Modal>
    );
};

export default Credentials;
