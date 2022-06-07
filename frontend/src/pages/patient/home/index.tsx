import { useContext } from 'react';
import { formatDate } from 'lib/helpers';
import Menu from 'components/Menu';
import { useHistory } from 'lib/router';
import StoreContext from 'state/context/store';
import { addAction } from 'state/actions/analytics';
import Skills from 'assets/icons/Skills';
import Interview from 'assets/icons/Interview';
import Heart from 'assets/icons/Heart';
import Stories from 'assets/icons/Stories';

import Bookmark from './bookmark';
import styles from './index.module.scss';
import { routeToMenuAction } from 'components/Menu';
import Path3Home from './path3';

import { Patient } from 'state/types';

const PatientHome = () => {
    const history = useHistory();
    const [store] = useContext(StoreContext);
    const { user } = store;
    const { firstName, lastName, dateOfBirth, ssid, activities } = user as Patient;
    const isPath3 = !activities.csa && !activities.csp;

    const navigateTo = (route: keyof typeof routeToMenuAction) => {
        addAction(routeToMenuAction[route]);
        history.push(route);
    };

    if (isPath3) {
        return <Path3Home />;
    }

    return (
        <div className={styles.container} style={{ overflowY: 'auto' }}>
            <Menu selectedItem="home" dark />
            <div id="home" className={styles.home}>
                <span className={styles.header}>Welcome to Jaspr.</span>
                <hr className={styles.rule} />
                <div className={styles.description}>
                    People need different things. You can try some of these activities and see what
                    works best for you.
                </div>
                <div className={styles.bookmarks}>
                    {activities.skills && (
                        <Bookmark
                            navigateTo={() => navigateTo('/stories')}
                            title="Shared Stories"
                            description="Hear the stories of other people who have experienced feeling suicidal."
                            Icon={Stories}
                        />
                    )}
                    {activities.skills && (
                        <Bookmark
                            navigateTo={() => navigateTo('/skills')}
                            title="Comfort &amp; Skills"
                            description="This area has things that could help you feel better and make waiting easier."
                            Icon={Skills}
                        />
                    )}

                    <Bookmark
                        navigateTo={() => navigateTo('/question')}
                        title="Suicide Status Interview"
                        description="Answer questions about what you are going through to help you get the help you need."
                        Icon={Interview}
                    />

                    {activities.csp && (
                        <Bookmark
                            navigateTo={() => navigateTo('/takeaway')}
                            title="Takeaway Kit"
                            description="Save your favorite activities and your plan so you stay safe after you leave."
                            Icon={Heart}
                        />
                    )}
                </div>
                <div className={styles.copyright}>
                    &#xA9; {new Date().getFullYear()} Jaspr Health
                </div>
                <div className={styles.patientInfo}>
                    {lastName}
                    {lastName && firstName ? ', ' : ''}
                    {ssid}
                    {firstName} {dateOfBirth && <>({formatDate(dateOfBirth)})</>}
                </div>
            </div>
        </div>
    );
};

export default PatientHome;
