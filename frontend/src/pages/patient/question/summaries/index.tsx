import { useContext, useEffect, useRef, useState } from 'react';
import Modal, { Styles } from 'react-modal';
import { actionNames, addAction } from 'state/actions/analytics';
import Button from 'components/Button';
import zIndexHelper from 'lib/zIndexHelper';
import styles from './index.module.scss';
import CrossedPlus from 'components/CrossedPlus';
import ProviderSummary from 'pages/technician/providerSummary';
import CamsSummary from 'pages/patient/takeaway/camsSummary';
import StabilityPlan from 'components/StabilityPlan';
import StoreContext from 'state/context/store';
import { getSkills } from 'state/actions/skills';
import { getStoriesVideos } from 'state/actions/stories';
import { Patient } from 'state/types';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-evenly',
        zIndex: zIndexHelper('patient.summaries'),
        backgroundColor: 'rgba(255, 255, 255, 1)',
        left: '148px',
        top: '56px',
        right: '24px',
        borderTopRightRadius: '30px',
        borderTopLeftRadius: '30px',
    },
    content: {
        position: 'static',
        display: 'flex',
        alignSelf: 'center',
        backgroundColor: 'transparent',
        border: 'none',
        borderRadius: 0,
        padding: 0,
    },
};

type Props = {
    toggleSummaries: () => void;
};

const Summaries = ({ toggleSummaries }: Props) => {
    const [store, dispatch] = useContext(StoreContext);
    const { assessment, skills, stories, user } = store;
    const { videoRatings } = stories;
    const { answers, activities } = assessment;
    const { storiesFetched } = stories;
    const { sessionLocked } = user as Patient;

    const [openModal, setOpenModal] = useState(null);
    const prevModal = useRef<string | null>(null);

    const questions = activities.map((activity) => activity.questions).flat();

    useEffect(() => {
        if (!storiesFetched && !sessionLocked) {
            getStoriesVideos(dispatch);
        }
        if (skills.length === 0 && !sessionLocked) {
            getSkills(dispatch);
        }
    }, [dispatch, sessionLocked, storiesFetched, skills.length]);

    useEffect(() => {
        if (openModal === 'summary') {
            addAction(actionNames.CARE_PLANNING_REPORT_OPEN);
        } else if (openModal === 'stability') {
            addAction(actionNames.STABILITY_PLAN_OPEN);
        } else if (openModal === 'cams') {
            addAction(actionNames.INTERVIEW_SUMMARY_OPEN);
        } else if (!openModal && prevModal.current === 'summary') {
            addAction(actionNames.CARE_PLANNING_REPORT_CLOSED);
        } else if (!openModal && prevModal.current === 'stability') {
            addAction(actionNames.STABILITY_PLAN_CLOSED);
        } else if (!openModal && prevModal.current === 'cams') {
            addAction(actionNames.INTERVIEW_SUMMARY_CLOSED);
        }
        prevModal.current = openModal;
    }, [openModal]);

    return (
        <div className={styles.popup}>
            <div className={styles.top}>
                <div className={styles.topSpacer} />
                <h3 className={styles.title}>Summaries</h3>
                <CrossedPlus className={styles.crossedPlus} size={48} onClick={toggleSummaries} />
            </div>
            <div className={styles.tiles}>
                <div className={styles.tile}>
                    <h5 className={styles.tileTitle}>Care Planning Report</h5>
                    <p className={styles.tileDescription}>
                        Clinical summary to review with your provider
                    </p>
                    <Button onClick={() => setOpenModal('summary')}>Open</Button>
                </div>
                <div className={styles.tile}>
                    <h5 className={styles.tileTitle}>Interview Summary</h5>
                    <p className={styles.tileDescription}>
                        Review and edit your answers to the Suicide Status Interview
                    </p>
                    <Button onClick={() => setOpenModal('cams')}>Open</Button>
                </div>
                <div className={styles.tile}>
                    <h5 className={styles.tileTitle}>Stability Plan</h5>
                    <p className={styles.tileDescription}>
                        When you're ready, take a look at the plan you made to keep yourself safe
                    </p>
                    <Button onClick={() => setOpenModal('stability')}>Open</Button>
                </div>
            </div>
            <Modal isOpen={Boolean(openModal)} style={modalStyle}>
                {openModal === 'stability' && (
                    <>
                        <div className={styles.modalTitle}>My Stability Plan</div>
                        <div className={styles.back} onClick={() => setOpenModal(null)}>
                            ‹ Summaries
                        </div>
                        <div style={{ marginTop: '84px', overflowY: 'scroll' }}>
                            <StabilityPlan answers={answers} questions={questions} />
                        </div>
                    </>
                )}
                {openModal === 'summary' && (
                    <>
                        <div className={styles.modalTitle}>Care Planning Report</div>
                        <div className={styles.back} onClick={() => setOpenModal(null)}>
                            ‹ Summaries
                        </div>
                        <div style={{ marginTop: '84px', overflowY: 'scroll' }}>
                            <ProviderSummary
                                answers={answers}
                                skills={skills}
                                patientVideos={videoRatings}
                            />
                        </div>
                    </>
                )}
                {openModal === 'cams' && (
                    <>
                        <div className={styles.modalTitle}>Interview Summary</div>
                        <div className={styles.back} onClick={() => setOpenModal(null)}>
                            ‹ Summaries
                        </div>
                        <div style={{ marginTop: '84px', overflowY: 'scroll' }}>
                            <CamsSummary printMode answers={answers} />
                        </div>
                    </>
                )}
            </Modal>
        </div>
    );
};

export default Summaries;
