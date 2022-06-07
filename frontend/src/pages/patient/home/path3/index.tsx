import React, { useContext, useEffect, useState } from 'react';
import Modal, { Styles } from 'react-modal';
import { useHistory } from 'react-router-dom';
import { formatDate } from 'lib/helpers';
import zIndexHelper from 'lib/zIndexHelper';
import StoreContext from 'state/context/store';
import { getSkills } from 'state/actions/skills';
import { getStoriesVideos, getVideoRatings } from 'state/actions/stories';
import Video from 'components/Videos';
import Menu from 'components/Menu';
import styles from './index.module.scss';

import { Patient, Skill } from 'state/types';
import Button from 'components/Button';

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

const Path3Home = () => {
    const history = useHistory();
    const [store, dispatch] = useContext(StoreContext);
    const { skills, stories, user } = store;
    const { storiesFetched, ratingsFetched } = stories;
    const { firstName, lastName, dateOfBirth, ssid, sessionLocked } = user as Patient;
    const [selectedSkillId, setSelectedSkillId] = useState<number | null>(null);
    const [selectedStoryId, setSelectedStoryId] = useState<number | null>(null);

    useEffect(() => {
        if (!storiesFetched && !sessionLocked) {
            getStoriesVideos(dispatch);
        }
        if (skills.length === 0 && !sessionLocked) {
            getSkills(dispatch);
        }
    }, [dispatch, skills.length, sessionLocked, storiesFetched]);

    useEffect(() => {
        if (!ratingsFetched) {
            getVideoRatings(dispatch);
        }
    }, [dispatch, ratingsFetched]);

    const goToSkill = (skill: Skill) => {
        if (skill.video) {
            setSelectedSkillId(skill.id);
        } else if (skill.targetUrl) {
            history.push({
                pathname: skill.targetUrl,
                state: {
                    from: '/',
                },
            });
        }
    };

    return (
        <div className={styles.container}>
            <Menu selectedItem="home" dark />
            <div id="home" className={styles.home}>
                <h4>
                    People need different things. You can try watching some of these shared stories
                    or activities and see what works best for you.
                </h4>
                <hr className={styles.rule} />
                <div className={styles.sections}>
                    <section>
                        <h6>Shared Stories</h6>
                        <div className={styles.items}>
                            {stories.videos
                                .sort((a, b) => {
                                    // Hardcoding top videos because we will likely be changing this
                                    // component significanltly in the near future.
                                    const priority = [
                                        'Thai - My Wish For You',
                                        "Ashley - When I'm in Distress",
                                        'Kelechi - Relationship to Suicide',
                                    ];
                                    if (priority.includes(a.name)) {
                                        return -1;
                                    } else if (priority.includes(b.name)) {
                                        return 1;
                                    }
                                    return 0;
                                })
                                .slice(0, 3)
                                .map((video) => (
                                    <figure
                                        key={video.id}
                                        role="button"
                                        aria-label={`Watch ${video.name} video`}
                                        tabIndex={0}
                                        onClick={() => setSelectedStoryId(video.id)}
                                    >
                                        <img src={video.thumbnail} alt={video.name} />
                                        <figcaption className="typography--caption">
                                            {video.name}
                                        </figcaption>
                                    </figure>
                                ))}
                        </div>
                        <div style={{ marginTop: 'auto' }}>
                            <Button
                                variant="tertiary"
                                dark
                                onClick={() =>
                                    history.push({ pathname: '/stories', state: { from: '/' } })
                                }
                            >
                                Explore All
                            </Button>
                        </div>
                    </section>

                    <section>
                        <h6>Comfort &amp; Skill Activities</h6>
                        <div className={styles.items}>
                            {skills
                                .sort((a, b) => {
                                    const priority = [
                                        'Paced Breathing',
                                        'Puppies',
                                        'Distract: Name Things',
                                    ];
                                    if (priority.includes(a.name)) {
                                        return -1;
                                    } else if (priority.includes(b.name)) {
                                        return 1;
                                    }
                                    return 0;
                                })
                                .slice(0, 3)
                                .map((skill) => (
                                    <figure
                                        key={skill.id}
                                        role="button"
                                        aria-label={`Go to ${skill.name} skill`}
                                        tabIndex={0}
                                        onClick={() => goToSkill(skill)}
                                        onKeyDown={(e) => {
                                            if (
                                                e.key === ' ' ||
                                                e.key === 'Enter' ||
                                                e.key === 'Spacebar'
                                            ) {
                                                goToSkill(skill);
                                            }
                                        }}
                                    >
                                        <img src={skill.thumbnailImage} alt={skill.name} />
                                        <figcaption className="typography--caption">
                                            {skill.name}
                                        </figcaption>
                                    </figure>
                                ))}
                        </div>
                        <div style={{ marginTop: 'auto' }}>
                            <Button
                                variant="tertiary"
                                dark
                                onClick={() =>
                                    history.push({ pathname: '/skills', state: { from: '/' } })
                                }
                            >
                                Explore All
                            </Button>
                        </div>
                    </section>
                </div>
                <div className={styles.copyright}>&#xA9; 2021 Jaspr Health</div>
                <div className={styles.patientInfo}>
                    {lastName}
                    {lastName && firstName ? ', ' : ''}
                    {ssid}
                    {firstName} {dateOfBirth && <>({formatDate(dateOfBirth)})</>}
                </div>
            </div>

            <Modal isOpen={Boolean(selectedStoryId)} style={modalStyle}>
                {Boolean(selectedStoryId) && (
                    <Video
                        video={stories.videos.find((video) => video.id === selectedStoryId)}
                        type="story"
                        back={() => setSelectedStoryId(null)}
                        autoplay
                    />
                )}
            </Modal>
            <Modal isOpen={Boolean(selectedSkillId)} style={modalStyle}>
                {Boolean(selectedSkillId) && (
                    <Video
                        video={skills.find((skill) => skill.id === selectedSkillId)?.video}
                        skill={skills.find((skill) => skill.id === selectedSkillId)}
                        type="skill"
                        back={() => setSelectedSkillId(null)}
                        autoplay
                    />
                )}
            </Modal>
        </div>
    );
};

export default Path3Home;
