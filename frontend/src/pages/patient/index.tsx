import { useContext, useEffect, useState } from 'react';

import { useHistory, Switch, Route } from 'react-router-dom';
import StoreContext from 'state/context/store';
import { getSkills } from 'state/actions/skills';
import { getStoriesVideos, getVideoRatings } from 'state/actions/stories';
import { getAnswers, getQuestions } from 'state/actions/assessment';

import PatientHome from './home';
import Breathe from './breathe';
import Stories from './stories';
import Skills from './skills';
import Question from './question';
import TakeawayKit from './takeaway';
import { Patient } from 'state/types';

const PatientRouter = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { assessment, device, skills, stories, user } = store;
    const { loaded } = device;
    const { ratingsFetched, storiesFetched } = stories;
    const { authenticated, sessionLocked, technicianOperated } = user as Patient;
    const { activities } = assessment;
    const [checkedForActiveActivity, setCheckedForActiveActivity] = useState(false);

    const hasActiveActivity = activities.some(
        (activity) =>
            !activity.locked &&
            ['suicide_assessment', 'lethal_means', 'stability_plan'].includes(activity.type),
    );

    useEffect(() => {
        if (
            !checkedForActiveActivity &&
            !history.location.pathname.startsWith('/start-patient-session') &&
            hasActiveActivity
        ) {
            if (technicianOperated) {
                history.replace('/takeaway/stability-plan/safer');
            } else {
                history.replace('/question');
            }
            setCheckedForActiveActivity(true);
        }
    }, [
        history.location.pathname,
        checkedForActiveActivity,
        hasActiveActivity,
        history,
        technicianOperated,
    ]);

    // Get patient data
    useEffect(() => {
        if (!storiesFetched && !sessionLocked) {
            getStoriesVideos(dispatch);
        }
        if (!ratingsFetched && !sessionLocked) {
            getVideoRatings(dispatch);
        }
        if (skills.length === 0 && !sessionLocked) {
            getSkills(dispatch);
        }
    }, [dispatch, sessionLocked, storiesFetched, skills.length, ratingsFetched]);

    useEffect(() => {
        if (activities.length === 0) {
            getQuestions(dispatch);
        }
    }, [dispatch, activities.length]);

    useEffect(() => {
        if (!sessionLocked) {
            getAnswers(dispatch);
        }
    }, [dispatch, sessionLocked]);

    if (loaded && !authenticated) {
        history.push({
            pathname: '/',
        });
    }

    return (
        <Switch>
            <Route exact path={'/'} component={PatientHome} />

            <Route exact path={'/breathe'} component={Breathe} />
            <Route exact path="/stories" component={Stories} />
            <Route exact path="/skills" component={Skills} />

            <Route exact path="/question" component={Question} />

            <Route path="/takeaway" component={TakeawayKit} />
        </Switch>
    );
};

export default PatientRouter;
