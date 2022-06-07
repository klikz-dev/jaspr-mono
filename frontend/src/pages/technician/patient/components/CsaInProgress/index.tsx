import Button from 'components/Button';
import { useState } from 'react';
import { Activity } from 'state/types';
import Documentation from '../../Documentation';
import styles from './index.module.scss';

interface CsaInProgressProps {
    close: () => void;
    toggleLock: (activity: Activity, locked: boolean) => void;
    activity: Activity;
    patient: any;
    patientData: any;
    preferences: any;
}

const CsaInProgress = ({
    close,
    toggleLock,
    activity,
    patient,
    patientData,
    preferences,
}: CsaInProgressProps) => {
    const [screen, setScreen] = useState<'main' | 'confirmation' | 'notes'>('main');
    return (
        <div className={styles.container}>
            {screen === 'main' && (
                <>
                    <h4>Comprehensive Suicide Assessment in Progress</h4>
                    <div className={styles.buttons}>
                        <Button variant="tertiary" onClick={() => setScreen('confirmation')}>
                            Mark as Completed
                        </Button>
                        <Button variant="tertiary" onClick={() => setScreen('notes')}>
                            Review Notes
                        </Button>
                        <Button dark onClick={close}>
                            Leave as in Progress
                        </Button>
                    </div>
                </>
            )}
            {screen === 'confirmation' && (
                <>
                    <h4>Conclude the Comprehensive Suicide Assessment?</h4>
                    <p>
                        This action will conclude the assessment for your patient and they will no
                        longer be able to make changes. To update the Comprehensive Suicide
                        Assessment you will have to reassign it.
                    </p>
                    <div className={styles.buttons}>
                        <Button variant="tertiary" onClick={close}>
                            No
                        </Button>
                        <Button
                            dark
                            onClick={() => {
                                toggleLock(activity, true);
                                close();
                            }}
                        >
                            Yes
                        </Button>
                    </div>
                </>
            )}
            {screen === 'notes' && (
                <>
                    <h4>Review Notes</h4>
                    <div style={{ overflowY: 'auto', margin: '0 -20px' }}>
                        <Documentation
                            patientData={patientData}
                            currentEncounter={patient.currentEncounter}
                            preferences={preferences}
                        />
                    </div>

                    <div className={styles.buttons} style={{ marginTop: '2rem' }}>
                        <Button variant="tertiary" onClick={() => setScreen('confirmation')}>
                            Mark as Completed
                        </Button>
                        <Button dark onClick={close}>
                            Leave as in Progress
                        </Button>
                    </div>
                </>
            )}
        </div>
    );
};

export default CsaInProgress;
