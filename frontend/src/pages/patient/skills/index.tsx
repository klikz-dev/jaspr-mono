import { useContext, useEffect, useState } from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import StoreContext from 'state/context/store';
import Segment, { AnalyticNames } from 'lib/segment';
import Modal, { Styles } from 'react-modal';
import Menu from 'components/Menu';
import zIndexHelper from 'lib/zIndexHelper';
import styles from './index.module.scss';
import Skill from './skill';
import Video from 'components/Videos';
import Button from 'components/Button';

interface SkillsProps {
    inCRP?: boolean;
    back?: () => void;
}

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'space-evenly',
        backgroundColor: 'rgba(45, 44, 63, 0.85)',
        zIndex: zIndexHelper('patient.skill'),
    },
    content: {
        position: 'absolute',
        top: 0,
        bottom: 0,
        right: 0,
        left: 0,
        padding: 0,
        borderRadius: 0,
    },
};

const Skills = ({ back, inCRP }: SkillsProps) => {
    const location = useLocation<{ from?: string }>();
    const history = useHistory();

    const [store] = useContext(StoreContext);
    const { skills, stories } = store;
    const { videoRatings } = stories;

    const [selectedVideoActivityId, setSelectedVideoActivityId] = useState<number | null>(null);
    const selectedVideoActivity = skills.find((skill) => skill.id === selectedVideoActivityId);

    const goBack = () => {
        if (location.state?.from) {
            history.replace(location.state.from);
        } else {
            history.goBack();
        }
    };

    useEffect(() => {
        if (!selectedVideoActivityId) {
            Segment.track(AnalyticNames.VIDEO_PLAYER_CLOSED);
        }
    }, [selectedVideoActivityId]);

    return (
        <div className={`${styles.container} ${styles.inCRP}`}>
            <Modal isOpen={Boolean(selectedVideoActivity)} style={modalStyle}>
                {selectedVideoActivity && (
                    <Video
                        video={selectedVideoActivity.video}
                        skill={selectedVideoActivity}
                        type="skill"
                        back={() => setSelectedVideoActivityId(null)}
                        autoplay
                    />
                )}
            </Modal>

            {!selectedVideoActivity && (
                <>
                    {!inCRP && <Menu selectedItem="skills" />}

                    <div className={styles.inner} style={{ overflowX: 'hidden' }}>
                        <div
                            className={`${styles.titleControls} ${
                                location.state?.from ? styles.back : ''
                            }`}
                        >
                            {inCRP && back && (
                                <div
                                    className={styles.back}
                                    onClick={back}
                                    style={{ cursor: 'pointer' }}
                                >
                                    ‹ Back
                                </div>
                            )}
                            {location.state?.from && (
                                <Button variant="tertiary" onClick={goBack}>
                                    Back
                                </Button>
                            )}
                            <h2
                                className={`typography--h4 ${styles.onlyNotMobile} ${styles.title}`}
                            >
                                Comfort &amp; Skills
                            </h2>
                        </div>

                        <div className={`${styles.skills} ${inCRP ? styles.small : ''}`}>
                            {skills.map((skill) => (
                                <Skill
                                    {...skill}
                                    key={skill.id}
                                    inCRP={inCRP}
                                    videoRatings={videoRatings}
                                    setSelectedVideoActivityId={setSelectedVideoActivityId}
                                />
                            ))}
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default Skills;
