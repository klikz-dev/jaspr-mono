import { useState } from 'react';
import { useHistory } from 'lib/router';
import styles from './index.module.scss';
import Modal, { Styles } from 'react-modal';
import Video from 'components/Videos';
import CrossedPlus from 'components/CrossedPlus';
import zIndexHelper from 'lib/zIndexHelper';
import { Skill } from 'state/types';

const modalStyle: Styles = {
    overlay: {
        display: 'flex',
        justifyContent: 'space-evenly',
        backgroundColor: 'rgba(45, 44, 63, 0.85)',
        zIndex: zIndexHelper('patient.skill-item'),
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

type SavedSkillsListItemProps = {
    skill: Skill;
    onRemove?: (skill: Skill) => void;
    setQuestionDisableAudio?: (disabled: boolean) => void;
};

const SavedSkillsListItem = (props: SavedSkillsListItemProps) => {
    const history = useHistory();
    const { skill, onRemove, setQuestionDisableAudio } = props;
    const { video } = skill;

    const [showVideo, setShowVideo] = useState(false);

    const onClickRemove = () => {
        if (onRemove) {
            onRemove(skill);
        }
    };

    const goToSkill = () => {
        if (onRemove) return;
        if (video) {
            setShowVideo(true);
            if (setQuestionDisableAudio) {
                setQuestionDisableAudio(true);
            }
        } else if (skill.targetUrl) {
            const params = new URLSearchParams(history.location ? history.location.search : '');
            const prevReturnUrl = params.get('return');
            const inReview = params.get('review');

            if (inReview) {
                // TODO REVIEW
                history.push({
                    pathname: skill.targetUrl,
                    search: `?return=${history.location.pathname}${
                        prevReturnUrl ? '&prevReturn=' + prevReturnUrl : ''
                    }${inReview ? '&review=true' : ''}`,
                });
            } else {
                history.push({
                    pathname: skill.targetUrl,
                    state: {
                        from: history.location.pathname,
                    },
                });
            }
        }
    };

    return (
        <li className={styles.item}>
            {onRemove && <CrossedPlus onClick={onClickRemove} size={24} />}
            <div
                className={styles.name}
                onClick={goToSkill}
                style={{ cursor: video ? 'pointer' : 'default' }}
            >
                {skill.name}
            </div>
            <img
                src={skill.thumbnailImage}
                alt={skill.name}
                className={styles.image}
                onClick={goToSkill}
                style={{ cursor: video ? 'pointer' : 'default' }}
            />
            {video && (
                <Modal isOpen={showVideo} style={modalStyle}>
                    <Video
                        video={video}
                        type="skill"
                        skill={skill}
                        autoplay
                        back={() => {
                            setShowVideo(false);
                            if (setQuestionDisableAudio) {
                                setQuestionDisableAudio(false);
                            }
                        }}
                    />
                </Modal>
            )}
        </li>
    );
};

export default SavedSkillsListItem;
