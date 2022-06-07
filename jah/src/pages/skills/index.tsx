import React, { useContext, useEffect, useState } from 'react';
import StoreContext from 'state/context/store';
import Segment from 'lib/segment';
import { Modal } from 'react-native';
import Styled from 'styled-components/native';
import Menu from 'components/HamburgerMenu';
import JahMenu from 'components/Menu';
import styles from './index.module.scss';
import Skill from './skill';
import Video from 'components/Videos';
import { saveSkillForLater, rateSkill } from 'state/actions/skills';
import { getSkills } from 'state/actions/skills';
import { getVideoRatings } from 'state/actions/stories';
import { Patient } from 'state/types';

const StyledContainer = Styled.ScrollView`${styles.container}`;
const StyledInner = Styled.View`${styles.inner}`;
const StyledBack = Styled.TouchableOpacity`${styles.back}`;
const StyledSkills = Styled.View`
    ${styles.skills}
    background-color: #2F3251;
    padding-top: 0;
`;

interface SkillsProps {
    back?: () => void;
}

const Skills = ({ back }: SkillsProps) => {
    const [store, dispatch] = useContext(StoreContext);
    const { skills, stories, user } = store;
    const { ratingsFetched, videoRatings } = stories;
    const { sessionLocked } = user as Patient;

    const [selectedVideoActivityId, setSelectedVideoActivityId] = useState<number | null>(null);
    const selectedVideoActivity = skills.find((skill) => skill.id === selectedVideoActivityId);

    useEffect(() => {
        if (skills.length === 0 && !sessionLocked) {
            getSkills(dispatch);
        }
    }, [dispatch, skills.length, sessionLocked]);

    useEffect(() => {
        if (!ratingsFetched) {
            getVideoRatings(dispatch);
        }
    }, [dispatch, ratingsFetched]);

    useEffect(() => {
        if (!selectedVideoActivityId) {
            Segment.track('Video player closed');
        }
    }, [selectedVideoActivityId]);

    // TODO: For these two functions below, we might want to check if the
    // patient activities have been fully loaded first.
    const saveVideoActivity = () => {
        if (selectedVideoActivity) {
            const { patientActivity, id, saveForLater } = selectedVideoActivity;
            saveSkillForLater(dispatch, patientActivity || null, id, !saveForLater);
        }
    };

    const rateVideoActivity = (rating: 0 | 1 | 2 | 3 | 4 | 5) => {
        if (selectedVideoActivity) {
            const { patientActivity, id } = selectedVideoActivity;
            rateSkill(dispatch, patientActivity || null, id, rating);
        }
    };

    return (
        <>
            <StyledContainer>
                <Menu selectedItem="skills" hideLogo />
                <Modal
                    visible={Boolean(selectedVideoActivity)}
                    animationType="slide"
                    supportedOrientations={['portrait', 'landscape']}
                >
                    {selectedVideoActivity && (
                        <Video
                            {...selectedVideoActivity.video}
                            // @ts-ignore review this type and data
                            object={selectedVideoActivity}
                            save={saveVideoActivity}
                            rate={rateVideoActivity}
                            back={() => setSelectedVideoActivityId(null)}
                            autoplay
                        />
                    )}
                </Modal>

                {!Boolean(selectedVideoActivity) && (
                    <>
                        <StyledInner>
                            {back && <StyledBack onPress={back}>‹ Back</StyledBack>}
                            <StyledSkills>
                                {skills.map((skill) => (
                                    <>
                                        {/*@ts-ignore // TODO Review skill props */}
                                        <Skill
                                            {...skill}
                                            key={skill.id}
                                            setSelectedVideoActivityId={setSelectedVideoActivityId}
                                            videoRatings={videoRatings}
                                        />
                                    </>
                                ))}
                            </StyledSkills>
                        </StyledInner>
                    </>
                )}
            </StyledContainer>
            <JahMenu selected="skills" />
        </>
    );
};

export default Skills;
