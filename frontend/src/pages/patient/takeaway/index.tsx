import { useEffect, useState, useContext, useCallback } from 'react';
import Modal, { Styles } from 'react-modal';
import { useHistory, Switch, Route, useRouteMatch } from 'react-router-dom';
import { Patient, Skill, Video } from 'state/types';
import { saveSkillForLater } from 'state/actions/skills';
import { saveStoryForLater } from 'state/actions/stories';

import StoreContext from 'state/context/store';
import Menu from 'components/Menu';
import StabilityPlan from 'components/StabilityPlan';
import StabilityPlanPage from 'pages/patient/takeaway/StabilityPlanEdit';

import EditModeArea from 'components/EditModeArea';
import SavedSkillsList from 'components/Skills/savedSkillsList';
import SavedSharedStoriesList from 'components/SharedStories/savedSharedStoriesList';
import Skills from '../skills';
import Banner from './setupAccount/banner';
import Step0 from './setupAccount/step0';
import Step1 from './setupAccount/step1';
import Step2 from './setupAccount/step2';
import Step3 from './setupAccount/step3';
import styles from './index.module.scss';
import Pencil from 'assets/icons/Pencil';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'space-evenly',
        backgroundColor: 'rgba(45, 44, 63, 0.85)',
    },
    content: {
        position: 'static',
        display: 'flex',
        alignSelf: 'center',
        backgroundColor: 'transparent',
        border: 'none',
        borderRadius: '5px',
        padding: 0,
    },
};

interface TakeawayKitProps {
    printMode?: boolean;
}

const TakeawayKit = ({ printMode = false }: TakeawayKitProps) => {
    const history = useHistory();
    const match = useRouteMatch();
    const [store, dispatch] = useContext(StoreContext);
    const { assessment, stories, skills } = store;
    const user = store.user as Patient;
    const { activities } = user;

    const [showSkills, setShowSkills] = useState(false);
    const [, setQuestionDisableAudio] = useState(false);
    const [email, setEmail] = useState(user.email || '');
    const [mobilePhone, setMobilePhone] = useState(user.mobilePhone || '');
    const [showAccountSetupModal, setShowAccountSetupModal] = useState(false);
    const [accountSetupStep, setAccountSetupStep] = useState<0 | 1 | 2 | 3>(0);
    const [accountSetupError, setAccountSetupError] = useState('');
    const { assessmentLocked, answers } = assessment;
    const { toolsToGoStatus } = user as Patient;

    const questions = assessment?.activities.map((activity) => activity.questions).flat();

    useEffect(() => {
        setEmail(user.email || '');
    }, [user.email]);

    useEffect(() => {
        setMobilePhone(user.mobilePhone || '');
    }, [user.mobilePhone]);

    const removeVideo = useCallback(
        (video: Video) => {
            const videoRating = stories.videoRatings.find((rating) => rating.video === video.id);
            saveStoryForLater(dispatch, videoRating?.id || null, video.id, false);
        },
        [dispatch, stories.videoRatings],
    );

    const removeSkill = useCallback(
        (skill: Skill) => {
            const { id, patientActivity } = skill;
            saveSkillForLater(dispatch, patientActivity || null, id, false);
        },
        [dispatch],
    );

    // Account setup functions
    const openAccountSetup = () => {
        setAccountSetupStep(0);
        setShowAccountSetupModal(true);
    };

    const nextAccountSetupStep = () => {
        if (accountSetupStep < 3) {
            // Max step number
            // @ts-ignore // TODO How do I type this properly
            setAccountSetupStep(accountSetupStep + 1);
        }
    };

    const prevAccountSetupStep = () => {
        if (accountSetupStep > 0) {
            // @ts-ignore // TODO How do I type this properly
            setAccountSetupStep(accountSetupStep - 1);
        }
    };

    // End account setup functions

    return (
        <Switch>
            <Route exact path={match.path}>
                <div className={styles.container}>
                    {!printMode && <Menu selectedItem="takeaway" />}

                    <div className={styles.area}>
                        <h1 className={styles.title}>Takeaway Kit</h1>
                        {showSkills && <Skills inCRP back={() => setShowSkills(false)} />}
                        <div
                            className={styles.mainLayout}
                            style={{ display: showSkills ? 'none' : undefined }}
                        >
                            <div className={styles.leftColumn}>
                                <div className={styles.titleBar}>My Stability Plan</div>
                                <StabilityPlan
                                    answers={answers}
                                    edit={!assessmentLocked && activities.csp}
                                    questions={questions}
                                />
                            </div>
                            <div className={styles.centerColumn} />
                            {activities.skills && (
                                <div className={styles.rightColumn}>
                                    <div className={styles.titleBar}>My Favorites</div>
                                    <EditModeArea
                                        render={({ editMode, toggleEditMode }) => (
                                            <div className={styles.savedActivities}>
                                                <div className={styles.savedSectionHeader}>
                                                    <div />
                                                    <div className={styles.savedSubtitle}>
                                                        Your Saved Comfort &amp; Skill Activities
                                                    </div>
                                                    <div
                                                        className={
                                                            editMode
                                                                ? styles.doneButton
                                                                : styles.editButton
                                                        }
                                                        onClick={toggleEditMode}
                                                    >
                                                        {editMode ? (
                                                            'Done'
                                                        ) : (
                                                            <>
                                                                <span className={styles.editLabel}>
                                                                    Edit
                                                                </span>
                                                                <Pencil
                                                                    color="#000000"
                                                                    height={13}
                                                                />
                                                            </>
                                                        )}
                                                    </div>
                                                </div>
                                                <SavedSkillsList
                                                    skills={skills.filter(
                                                        (skill) =>
                                                            Boolean(skill.patientActivity) &&
                                                            skill.saveForLater,
                                                    )}
                                                    onAdd={
                                                        editMode
                                                            ? () => setShowSkills(true)
                                                            : undefined
                                                    }
                                                    onRemove={editMode ? removeSkill : undefined}
                                                    setQuestionDisableAudio={
                                                        setQuestionDisableAudio
                                                    }
                                                />
                                            </div>
                                        )}
                                    />
                                    <EditModeArea
                                        render={({ editMode, toggleEditMode }) => (
                                            <div className={styles.savedStories}>
                                                <div className={styles.savedSectionHeader}>
                                                    <div />
                                                    <div className={styles.savedSubtitle}>
                                                        Your Saved Shared Stories
                                                    </div>
                                                    <div
                                                        className={
                                                            editMode
                                                                ? styles.doneButton
                                                                : styles.editButton
                                                        }
                                                        onClick={toggleEditMode}
                                                    >
                                                        {editMode ? (
                                                            'Done'
                                                        ) : (
                                                            <>
                                                                <span className={styles.editLabel}>
                                                                    Edit
                                                                </span>
                                                                <Pencil
                                                                    color="#000000"
                                                                    height={13}
                                                                />
                                                            </>
                                                        )}
                                                    </div>
                                                </div>
                                                <SavedSharedStoriesList
                                                    videos={stories.videoRatings
                                                        .filter((story) => story.saveForLater)
                                                        .map((story) => {
                                                            return stories.videos.find(
                                                                (vid) => vid.id === story.video,
                                                            );
                                                        })
                                                        .filter((video) => video !== undefined)}
                                                    onAdd={
                                                        editMode
                                                            ? () => history.push('/stories')
                                                            : undefined
                                                    }
                                                    onRemove={editMode ? removeVideo : undefined}
                                                    setQuestionDisableAudio={
                                                        setQuestionDisableAudio
                                                    }
                                                />
                                            </div>
                                        )}
                                    />
                                </div>
                            )}
                            {toolsToGoStatus === 'Not Started' && activities.csp && (
                                <Banner openAccountSetup={openAccountSetup} />
                            )}
                            {toolsToGoStatus !== 'Not Started' && (
                                <>
                                    <div className={styles.setupSuccessBanner}>
                                        Jaspr at Home set up complete!
                                        <div
                                            className={styles.setupEditButton}
                                            onClick={openAccountSetup}
                                        >
                                            Edit
                                        </div>
                                    </div>
                                </>
                            )}
                            <Modal isOpen={showAccountSetupModal} style={modalStyle}>
                                {accountSetupStep === 0 && (
                                    <Step0
                                        close={() => {
                                            setShowAccountSetupModal(false);
                                        }}
                                        nextAccountSetupStep={nextAccountSetupStep}
                                    />
                                )}
                                {accountSetupStep === 1 && (
                                    <Step1
                                        email={email}
                                        setEmail={setEmail}
                                        prevAccountSetupStep={prevAccountSetupStep}
                                        setMobilePhone={setMobilePhone}
                                        mobilePhone={mobilePhone}
                                        nextAccountSetupStep={nextAccountSetupStep}
                                        error={accountSetupError}
                                    />
                                )}
                                {accountSetupStep === 2 && (
                                    <Step2
                                        close={() => {
                                            setShowAccountSetupModal(false);
                                        }}
                                        nextAccountSetupStep={nextAccountSetupStep}
                                        prevAccountSetupStep={prevAccountSetupStep}
                                        email={email}
                                        mobilePhone={mobilePhone}
                                        setError={setAccountSetupError}
                                    />
                                )}
                                {accountSetupStep === 3 && (
                                    <Step3
                                        close={() => {
                                            setShowAccountSetupModal(false);
                                        }}
                                    />
                                )}
                            </Modal>
                        </div>
                    </div>
                </div>
            </Route>
            <Route path={`${match.path}/stability-plan`} component={StabilityPlanPage}></Route>
        </Switch>
    );
};

export default TakeawayKit;
