import Segment, { AnalyticNames } from 'lib/segment';
import { useContext } from 'react';
import { useHistory } from 'react-router-dom';
import StoreContext from 'state/context/store';
import { Patient } from 'state/types';
import styles from './index.module.scss';

const Consent = () => {
    const history = useHistory();
    const [store] = useContext(StoreContext);
    const { user } = store;
    const { consentLanguage } = user as Patient;
    const activities = (user as Patient).activities ?? { csa: false, csp: false };

    const next = () => {
        Segment.track(AnalyticNames.PATIENT_CONSENTED_DURING_ONBOARDING);
        if (!activities.csp && !activities.csa) {
            // Path 3 is an abridged onboarding
            history.push('/baseline');
        } else {
            history.push('/intro-video');
        }
    };

    return (
        <div className={styles.container}>
            <h1>Before we begin, please note:</h1>
            <div className={styles.consent}>{consentLanguage}</div>

            <button onClick={next}>I understand and agree to take part in this research</button>
        </div>
    );
};

export default Consent;
