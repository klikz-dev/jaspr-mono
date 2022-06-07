import { useContext, useEffect } from 'react';
import { useHistory } from 'lib/router';
import Hamburger from 'components/Hamburger';
import CUI from 'components/ConversationalUi';
import StoreContext from 'state/context/store';
import { formatDate } from 'lib/helpers';
import styles from './index.module.scss';
import { Patient } from 'state/types';
import { getQuestions } from 'state/actions/assessment';

const Baseline = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { user, assessment } = store;
    const { activities } = assessment;
    const { firstName, lastName, dateOfBirth, ssid } = user as Patient;

    useEffect(() => {
        if (activities.length === 0) {
            getQuestions(dispatch);
        }
    }, [dispatch, activities.length]);

    return (
        <div className={styles.container}>
            <Hamburger />
            <CUI activities={activities.filter((activity) => activity.type === 'intro')} />
            <div className={styles.footer}>
                <div className={styles.patientInfo}>
                    {lastName}
                    {lastName && firstName ? ', ' : ''}
                    {ssid}
                    {firstName} {dateOfBirth && <>({formatDate(dateOfBirth)})</>}
                </div>
                <div
                    className={styles.back}
                    onClick={() => {
                        history.replace('/intro-video');
                    }}
                >
                    ‹ Back
                </div>
            </div>
        </div>
    );
};

export default Baseline;
