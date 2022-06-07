import { useState, useContext, useEffect } from 'react';
import Modal, { Styles } from 'react-modal';
import useAxios from 'lib/useAxios';
import { useHistory } from 'react-router-dom';
import { useRouteMatch } from 'lib/router';
import Hamburger from 'components/Hamburger';
import logo from 'assets/logo.png';
import NewPatient from './newPatient';
import PatientRow from './patientRow';
import StoreContext from 'state/context/store';
import styles from './index.module.scss';
import { GetResponse } from 'state/types/api/technician/patients';
import NewEncounter from './newEncounter';
import Button from 'components/Button';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        background: 'rgba(68, 78, 105, 0.25)',
    },
    content: {
        position: 'relative',
        top: 'auto',
        left: 'auto',
        right: 'auto',
        bottom: 'auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        backgroundColor: 'rgba(255,255,255,1)',
        border: 'none',
        borderRadius: '4px',
        padding: 40,
        overflow: 'visible', // Allow polyfill calendar widget to flow outside modal
        width: '95%',
        maxWidth: '1000px',
        marginLeft: '100px',
        marginRight: '78px',
    },
};

const PatientList = () => {
    const history = useHistory();
    const axios = useAxios();
    const [store, dispatch] = useContext(StoreContext);
    const { device } = store;
    const { inPatientContext, patientContextId } = device;
    const { params } = useRouteMatch<{ patientId: string }>();
    const [searchValue, setSearchValue] = useState('');
    const [patients, setPatients] = useState<GetResponse>([]);
    const [newPatientModalOpen, setNewPatientModalOpen] = useState(false);
    const [showNewEncounter, setShowNewEncounter] = useState(null);
    const modalOpen = newPatientModalOpen;

    useEffect(() => {
        if (inPatientContext && patientContextId) {
            history.replace(`/technician/patients/${patientContextId}`);
        }
    }, [history, inPatientContext, patientContextId]);

    useEffect(() => {
        const CancelToken = axios.CancelToken;
        const source = CancelToken.source();

        (async () => {
            try {
                const response = await axios.get<GetResponse>(
                    `/technician/patients${searchValue ? `?q=${searchValue}` : ''}`,
                    {
                        cancelToken: source.token,
                    },
                );
                const sorted = response.data.sort((a, b) => {
                    const sortDateA = new Date(a.lastLoggedInAt || a.created).getTime();
                    const sortDateB = new Date(b.lastLoggedInAt || b.created).getTime();
                    return sortDateB - sortDateA;
                });

                setPatients(sorted);
                return response;
            } catch (err) {}
        })();

        return () => {
            if (source) {
                source.cancel();
            }
        };
    }, [axios, dispatch, searchValue]);

    if (inPatientContext) {
        <div>Loading patient...</div>;
    }

    return (
        <div className={styles.container}>
            <div className={styles.controls}>
                <img alt="" className={styles.logo} src={logo} />
                {!modalOpen && (
                    <div
                        style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            flex: 1,
                            marginRight: '80px',
                        }}
                    >
                        <div className={styles.search}>
                            <input
                                type="search"
                                value={searchValue}
                                placeholder="Search all records"
                                onChange={({ target }) => setSearchValue(target.value)}
                            />
                        </div>
                        <Button onClick={() => setNewPatientModalOpen(true)} icon="plus" dark>
                            Add New
                        </Button>
                    </div>
                )}
                <Hamburger />
            </div>
            <div className={styles.searchStats}>
                {searchValue && (
                    <>
                        {patients.length} records found matching:{' '}
                        <span className={styles.displayedSearchValue}>{searchValue}</span>
                    </>
                )}
            </div>
            <div className={`${styles.patientList} ${modalOpen ? styles.obscure : ''}`}>
                {patients.map((patient) => (
                    <PatientRow
                        key={patient.id}
                        patient={patient}
                        setShowNewEncounter={setShowNewEncounter}
                    />
                ))}
            </div>
            <Modal isOpen={Boolean(showNewEncounter)} style={modalStyle}>
                {showNewEncounter && (
                    <NewEncounter
                        patient={patients.find((patient) => patient.id === showNewEncounter)}
                        close={() => setShowNewEncounter(false)}
                        setPatients={setPatients}
                        setShowNewEncounter={setShowNewEncounter}
                    />
                )}
            </Modal>
            <Modal isOpen={!Boolean(params.patientId) && newPatientModalOpen} style={modalStyle}>
                <NewPatient
                    close={() => setNewPatientModalOpen(false)}
                    patients={patients}
                    setPatients={setPatients}
                    setSearchValue={setSearchValue}
                    setShowNewEncounter={setShowNewEncounter}
                />
            </Modal>
        </div>
    );
};

export default PatientList;
