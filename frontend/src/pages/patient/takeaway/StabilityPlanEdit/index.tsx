import { useContext, useEffect, useState } from 'react';
import Modal, { Styles } from 'react-modal';
import StoreContext from 'state/context/store';
import { NavLink, useHistory, Route, Switch, useRouteMatch } from 'lib/router';
import { getQuestions, saveAnswers } from 'state/actions/assessment';
import { logout } from 'state/actions/user';
import ConfirmLogoutModal from 'components/ConfirmLogoutModal';
import Menu from 'components/Menu';
import MakeHomeSafer from './Tabs/MakeHomeSafer';
import SupportivePeople from './Tabs/SupportivePeople';
import ReasonsForLiving from './Tabs/ReasonsForLiving';
import WarningSigns from './Tabs/WarningSigns';
import CopingSkills from './Tabs/CopingSkills';
import AtHome from './Tabs/AtHome';
import ConfirmDiscard from './Components/ConfirmDiscard';
import { AssessmentAnswers, Patient } from 'state/types';
import styles from './index.module.scss';
import toast from 'lib/toast';
import Segment, { AnalyticNames } from 'lib/segment';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(0,0,0,0.48)',
        padding: 0,
    },
    content: {
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 36,
        inset: 0,
        width: '400px',
        margin: 'auto',
        minHeight: '187px',
        background: '#FFFFFF',
        border: '1px solid #979797',
        borderRadius: '6px',
    },
};

const StabilityPlan = () => {
    const history = useHistory();
    const match = useRouteMatch();
    const [store, dispatch] = useContext(StoreContext);
    const { assessment, user } = store;
    const { answers, assessmentLocked, activities } = assessment;
    const { authenticated, technicianOperated, userType } = user as Patient;
    const [isDirty, setIsDirty] = useState(false);
    const [editedPlan, setEditedPlan] = useState<Partial<AssessmentAnswers>>({});
    const [isSaving, setIsSaving] = useState(false);
    const [showDiscard, setShowDiscard] = useState<string | false>(false);
    const [confirmLogoutModal, setConfirmLogoutModal] = useState(false);
    const [errors, setErrors] = useState({
        safer: '',
        people: '',
        reasons: '',
        warnings: '',
        skills: '',
    });

    const questions = activities.map((activity) => activity.questions).flat();

    const setAnswers = (
        answers: AssessmentAnswers | ((answers: AssessmentAnswers) => AssessmentAnswers),
    ) => {
        setIsDirty(true);
        setEditedPlan(answers);
    };

    useEffect(() => {
        setEditedPlan(answers);
        setIsDirty(false);
    }, [answers]);

    const preValidate = (): boolean => {
        let valid = true;
        const newErrors = {
            safer: '',
            people: '',
            reasons: '',
            warnings: '',
            skills: '',
        };

        // Check coping skills for duplicates
        const allCopingStrategies = [
            'copingBody',
            'copingDistract',
            'copingHelpOthers',
            'copingCourage',
            'copingSenses',
        ]
            .map((answerKey) => editedPlan[answerKey])
            .flat()
            .filter((strategy) => strategy);

        if (allCopingStrategies.length !== new Set(allCopingStrategies).size) {
            valid = false;
            newErrors.skills =
                'Looks like you already selected one of the options earlier. Please select a different choice.';
        }

        setErrors(newErrors);

        return valid;
    };

    const cleanAnswers = () => {
        const cleanedAnswers = { ...editedPlan };
        cleanedAnswers['reasonsLive'] = (cleanedAnswers.reasonsLive || []).filter(
            (reason) => reason,
        );
        cleanedAnswers.supportivePeople = (cleanedAnswers.supportivePeople || []).filter(
            (person) => person.name || person.phone,
        );
        return cleanedAnswers;
    };

    const save = async () => {
        const valid = preValidate();

        if (valid) {
            setIsSaving(true);
            const cleanedAnswers = cleanAnswers();
            const response = await saveAnswers(dispatch, cleanedAnswers, true);
            setIsDirty(false);

            if (response?.status === 200) {
                Segment.track(AnalyticNames.STABILITY_PLAN_EDITED_TAKEAWAY, {
                    technician_operated: true,
                });
                toast.success('Your edits have been successfully saved.', {
                    title: 'Saved',
                    dark: true,
                });
            } else {
                setIsSaving(false);
                toast.error('There was an error saving your stability plan', {
                    title: 'Unable to Save Changes',
                    dark: true,
                });
            }
        } else {
            toast.error(
                'Please address the error(s) we identified before saving your Stability Plan',
                {
                    title: 'Unable to Save Changes',
                    dark: true,
                },
            );
        }
    };

    const cancel = () => {
        if (technicianOperated) {
            setConfirmLogoutModal(true);
        } else {
            history.push('/takeaway');
        }
    };

    const doLogout = () => {
        Segment.track(AnalyticNames.LOG_OUT_BY_USER);
        logout(dispatch, userType, true);
        history.push('/');
    };

    useEffect(() => {
        // @ts-ignore // This needs to be reviewed.  https://github.com/ReactTraining/history/issues/690
        let unblock = history.block((location) => {
            if (!isSaving && isDirty && !showDiscard) {
                // Navigation was blocked! Let's show a confirmation dialog
                // so the user can decide if they actually want to navigate
                // away and discard changes they've made in the current page.
                let url = location.pathname;
                if (!url.startsWith('/takeaway/stability-plan/')) {
                    setShowDiscard(url);
                    unblock();
                    return false;
                }
                // if location not part of stability plan, show confirmation
                return true;
            }
        });

        return unblock;
    }, [showDiscard, isSaving, isDirty, history]);

    useEffect(() => {
        if (questions.length === 0 && authenticated) {
            getQuestions(dispatch);
        }
    }, [questions.length, authenticated, dispatch]);

    return (
        <div className={styles.page}>
            {!technicianOperated && <Menu selectedItem="takeaway" />}

            <div className={styles.container}>
                <div className={styles.header}>
                    <button id="cancel" className={styles.button} onClick={cancel}>
                        {technicianOperated ? 'Log Out' : 'Cancel'}
                    </button>
                    <div className={styles.title}>Edit Stability Plan</div>
                    <button
                        id="save"
                        className={styles.button}
                        disabled={assessmentLocked}
                        onClick={save}
                    >
                        Save
                    </button>
                </div>
                <div className={styles.tabs}>
                    <NavLink
                        className={`${styles.tab} ${errors?.safer ? styles.error : ''}`}
                        activeClassName={styles.active}
                        data-testid="tab-safer"
                        to="/takeaway/stability-plan/safer"
                    >
                        Make Home Safer
                    </NavLink>
                    <NavLink
                        className={`${styles.tab} ${errors?.people ? styles.error : ''}`}
                        activeClassName={styles.active}
                        data-testid="tab-people"
                        to="/takeaway/stability-plan/people"
                    >
                        Supportive People
                    </NavLink>
                    <NavLink
                        className={`${styles.tab} ${errors?.reasons ? styles.error : ''}`}
                        activeClassName={styles.active}
                        data-testid="tab-reasons"
                        to="/takeaway/stability-plan/reasons"
                    >
                        Reasons for Living
                    </NavLink>
                    <NavLink
                        className={`${styles.tab} ${errors?.warnings ? styles.error : ''}`}
                        activeClassName={styles.active}
                        data-testid="tab-warnings"
                        to="/takeaway/stability-plan/warnings"
                    >
                        Warning Signs
                    </NavLink>
                    <NavLink
                        className={`${styles.tab} ${errors?.skills ? styles.error : ''}`}
                        activeClassName={styles.active}
                        data-testid="tab-skills"
                        to="/takeaway/stability-plan/skills"
                    >
                        Coping Strategies
                    </NavLink>
                    {technicianOperated && (
                        <NavLink
                            className={`${styles.tab} ${errors?.skills ? styles.error : ''}`}
                            activeClassName={styles.active}
                            data-testid="tab-home"
                            to="/takeaway/stability-plan/at-home"
                        >
                            At Home
                        </NavLink>
                    )}
                </div>

                <div className={styles.content}>
                    <Switch>
                        <Route path={`${match.path}/safer`}>
                            <MakeHomeSafer
                                questions={questions}
                                answers={editedPlan}
                                setAnswers={setAnswers}
                                //error={errors?.safer}
                            />
                        </Route>

                        <Route path={`${match.path}/people`}>
                            <SupportivePeople
                                answers={editedPlan}
                                setAnswers={setAnswers}
                                // error={errors?.people}
                            />
                        </Route>

                        <Route path={`${match.path}/reasons`}>
                            <ReasonsForLiving
                                answers={editedPlan}
                                setAnswers={setAnswers}
                                // error={errors?.reasons}
                            />
                        </Route>

                        <Route path={`${match.path}/warnings`}>
                            <WarningSigns
                                questions={questions}
                                answers={editedPlan}
                                setAnswers={setAnswers}
                                error={errors?.warnings || ''}
                            />
                        </Route>

                        <Route path={`${match.path}/skills`}>
                            <CopingSkills
                                questions={questions}
                                answers={editedPlan}
                                setAnswers={setAnswers}
                                error={errors?.skills || ''}
                            />
                        </Route>
                        <Route path={`${match.path}/at-home`}>
                            <AtHome />
                        </Route>
                    </Switch>
                </div>
                <Modal isOpen={Boolean(showDiscard)} style={modalStyle}>
                    {showDiscard && (
                        <ConfirmDiscard
                            cancel={() => setShowDiscard(false)}
                            confirm={() => history.push(showDiscard)}
                        />
                    )}
                </Modal>
                <ConfirmLogoutModal
                    goBack={() => setConfirmLogoutModal(false)}
                    logout={doLogout}
                    confirmLogoutOpen={confirmLogoutModal}
                />
            </div>
        </div>
    );
};

export default StabilityPlan;
