import { useContext, useEffect, useState } from 'react';
import Modal, { Styles } from 'react-modal';
import useAxios from 'lib/useAxios';
import { useHistory } from 'lib/router';
import zIndexHelper from 'lib/zIndexHelper';
import StoreContext from 'state/context/store';
import Button from 'components/Button';
import styles from './index.module.scss';
import ActivatePatient from '../ActivatePatient';
import Segment, { AnalyticNames } from 'lib/segment';
import { PostResponse } from 'state/types/api/technician/tablet-pin';
import Checkbox from 'components/Checkbox';
import { Activity } from 'state/types';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(0,0,0,0.4)',
        zIndex: zIndexHelper('technician.tablet-activation'),
        backdropFilter: 'blur(59px)',
    },
    content: {
        position: 'relative',
        display: 'flex',
        maxWidth: '800px',
        width: '90%',
        inset: 0,
        flexDirection: 'column',
        border: 'none',
        backgroundColor: '#ffffff',
        padding: '4rem',
        overflow: 'hidden',
        borderRadius: '1rem',
    },
};

type ActivateTabletProps = {
    id: number;
    firstName?: string;
    lastName?: string;
    departments?: number[];
    dateOfBirth?: string; // 2000-12-31
    tourComplete?: boolean;
    currentEncounter: number;
    mrn?: string;
    ssid?: string;
    activities?: Activity[];
};

const ActivateTablet = ({
    id,
    firstName = '',
    lastName = '',
    mrn = '',
    ssid = '',
    departments,
    dateOfBirth,
    currentEncounter,
    tourComplete = false,
    activities,
}: ActivateTabletProps) => {
    const axios = useAxios();
    const history = useHistory();
    const [store] = useContext(StoreContext);
    const [pin, setPin] = useState('');
    const { device } = store;
    const { isTablet, isEhrEmbedded } = device;
    const [activationMethod, setActivationMethod] = useState<null | 'direct' | 'pin'>(null);
    const [technicianOperated, setTechnicianOperated] = useState<boolean>(false);
    const [allowActivationMethodChange, setAllowActivationMethodChange] = useState(true);

    const isIpad = //https://stackoverflow.com/a/58017456
        navigator.userAgent.match(/Mac/) &&
        navigator.maxTouchPoints &&
        navigator.maxTouchPoints > 2;

    useEffect(() => {
        if (isIpad || isTablet) {
            // Always use the direct method running on an ipad or a device specified as a tablet
            setActivationMethod('direct');
            setAllowActivationMethodChange(false);
        } else if (isEhrEmbedded) {
            // Always use the pin method when embedded in an EHR session
            setActivationMethod('pin');
            setAllowActivationMethodChange(false);
        } else {
            setActivationMethod('pin');
            setAllowActivationMethodChange(true);
        }
    }, [isEhrEmbedded, isIpad, isTablet]);

    useEffect(() => {
        if (currentEncounter) {
            (async () => {
                const response = await axios.post<PostResponse>(`/technician/tablet-pin`, {
                    encounter: currentEncounter,
                    technicianOperated,
                });
                setPin(response.data.pin);
                // TODO Error handling
            })();
        }
    }, [axios, currentEncounter, technicianOperated]);

    return (
        <Modal isOpen={true} style={modalStyle}>
            {activationMethod === 'direct' && (
                <ActivatePatient
                    id={id}
                    department={departments?.[0]}
                    ssid={ssid}
                    firstName={firstName}
                    lastName={lastName}
                    dob={dateOfBirth}
                    mrn={mrn}
                    firstActivation={!tourComplete}
                    allowActivationMethodChange={allowActivationMethodChange}
                    setActivationMethod={setActivationMethod}
                />
            )}
            {activationMethod === 'pin' && (
                <>
                    <div className={styles.header}>
                        <h4>Starting Patient Session</h4>
                        {activities?.find((activity) => activity.type === 'stability_plan') && (
                            <div className={styles.technicianOperated}>
                                <Checkbox
                                    checked={technicianOperated}
                                    onChange={() => setTechnicianOperated((cur) => !cur)}
                                    label="Go directly to Safety/Stability Planning"
                                    sublabel="Patient will not use tablet"
                                    labelStyle={{ fontWeight: 600 }}
                                />
                            </div>
                        )}
                        <div className={styles.details}>
                            <div className={styles.record}>
                                <span className="typography--overline">Patient Name</span>
                                <span className="typography--body1">
                                    {firstName} {lastName}
                                </span>
                            </div>
                            <div className={styles.record}>
                                <span className="typography--overline">{mrn ? 'MRN' : 'SSID'}</span>
                                <span className="typography--body1">{mrn || ssid}</span>
                            </div>
                        </div>

                        <br />

                        <span className={styles.instructions}>
                            Enter the following code into an available tablet.
                        </span>
                    </div>
                    <span className={styles.code}>{pin}</span>
                    <div className={styles.buttons}>
                        {allowActivationMethodChange && (
                            <Button
                                variant="tertiary"
                                onClick={() => {
                                    Segment.track(
                                        AnalyticNames.TECHNICIAN_CHANGED_ACTIVATION_METHOD,
                                        {
                                            method: 'device',
                                        },
                                    );
                                    setActivationMethod('direct');
                                }}
                            >
                                Open patient session on this device
                            </Button>
                        )}
                        <Button dark onClick={() => history.replace(`/technician/patients/${id}`)}>
                            Close
                        </Button>
                    </div>
                </>
            )}
        </Modal>
    );
};

export default ActivateTablet;
