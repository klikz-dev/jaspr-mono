import { useContext } from 'react';
import { useHistory } from 'lib/router';
import StoreContext from 'state/context/store';
import styles from './skill.module.scss';
import { ReactComponent as Heart } from 'assets/heart.svg';
import { saveSkillForLater } from 'state/actions/skills';
import { VideoRatings, Skill as SkillType } from 'state/types';

type SkillProps = SkillType & {
    inCRP?: boolean;
    setSelectedVideoActivityId: (videoActiviyId: number) => void;
    videoRatings: VideoRatings;
};

const Skill = ({
    id,
    patientActivity,
    saveForLater,
    targetUrl,
    name,
    thumbnailImage,
    labelColor,
    inCRP,
    video,
    setSelectedVideoActivityId,
    videoRatings,
}: SkillProps) => {
    const history = useHistory();
    const [, dispatch] = useContext(StoreContext);

    const progress = video
        ? videoRatings.find((rating) => rating.video === video.id)?.progress || 0
        : 0;

    const goToSkill = () => {
        if (video) {
            setSelectedVideoActivityId(id);
        } else if (targetUrl) {
            // TODO FIX return to previous
            /*const params = new URLSearchParams(
                history.location ? props.history.location.search : '',
            );
            const prevReturnUrl = params.get('return');
            const inReview = params.get('review');
            if (inReview) {
                history.push({
                    pathname: targetUrl,
                    search: `?return=${props.history.location.pathname}&crp=skills${
                        prevReturnUrl ? '&prevReturn=' + prevReturnUrl : ''
                    }${inReview ? '&review=true' : ''}`,
                });
            } else {
                history.push({
                    pathname: targetUrl,
                    search: `?return=${props.history.location.pathname}`,
                });
            }*/

            // TODO Make history stack for both web and native so we can easily pop back to the previous view
            history.push({
                pathname: targetUrl,
            });
        }
    };

    const addToPlan = () => {
        saveSkillForLater(dispatch, patientActivity, id, true);
    };

    const removeFromPlan = () => {
        saveSkillForLater(dispatch, patientActivity, id, false);
    };

    return (
        <div
            className={`${styles.container} ${inCRP ? styles.small : ''}`}
            style={{ minHeight: '300px' }}
        >
            <div className={styles.inner} style={{ boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.1)' }}>
                <div
                    className={`${styles.save} ${saveForLater ? styles.saved : ''}`}
                    onClick={saveForLater ? removeFromPlan : addToPlan}
                    style={{ cursor: 'pointer' }}
                >
                    <span className={styles.saveText}>
                        {saveForLater ? 'Remove from favorites' : 'Add to favorites'}
                    </span>
                    <Heart />
                </div>
                {Boolean(video) && (
                    <div className={styles.progress}>
                        <div className={styles.track} style={{ width: `${progress}%` }} />
                    </div>
                )}

                <img className={styles.thumb} src={thumbnailImage} onClick={goToSkill} alt={name} />
                <div
                    className={`${styles.banner} ${styles.bannerText}`}
                    onClick={goToSkill}
                    style={{ backgroundColor: labelColor }}
                >
                    {name}
                </div>
            </div>
        </div>
    );
};

export default Skill;
