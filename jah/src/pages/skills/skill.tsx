import React, { useContext } from 'react';
import { useHistory } from 'lib/router';
import StoreContext from 'state/context/store';
import Styled from 'styled-components/native';
import styles from './skill.module.scss';
import Heart from 'assets/heart.svg';
import HeartFilled from 'assets/heartFilled.svg';
import { saveSkillForLater } from 'state/actions/skills';
import { Video as VideoType, VideoRatings } from 'state/types';

const StyledContainer = Styled.View`${styles.container}`;
const StyledInner = Styled.View`${styles.inner}`;
const StyledSave = Styled.TouchableOpacity`${styles.save}`;
const StyledSaveText = Styled.Text`${styles.saveText} margin-right: auto;`;
const StyledImageContainer = Styled.TouchableOpacity`width: 100%; height: 170px;`;
const StyledImage = Styled.Image`${styles.thumb}; width: 100%;`;
const BannerText = Styled.Text`${styles.bannerText}`;
const StyledBanner = Styled.TouchableOpacity<{ labelColor: string }>`${
    styles.banner
} background-color: ${({ labelColor }) => labelColor}`;
const Progress = Styled.View`${styles.progress}`;
const Track = Styled.View<{ progress: number }>`${styles.track} width: ${({ progress }) =>
    progress ? `${progress}%` : '0'}`;

interface SkillProps {
    id: number;
    patientActivity: number;
    saveForLater: boolean;
    thumbnailImage: string;
    name: string;
    targetUrl: string;
    labelColor: string;
    setSelectedVideoActivityId: (videoActiviyId: number) => void;
    video: VideoType;
    videoRatings: VideoRatings;
}

const Skill = ({
    id,
    patientActivity,
    saveForLater,
    targetUrl,
    name,
    thumbnailImage,
    labelColor,
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
        <StyledContainer>
            <StyledInner>
                <StyledSave onPress={Boolean(saveForLater) ? removeFromPlan : addToPlan}>
                    <StyledSaveText>
                        {Boolean(saveForLater) ? 'Remove from favorites' : 'Add to favorites'}
                    </StyledSaveText>
                    {saveForLater && <HeartFilled width="13px" />}
                    {!saveForLater && <Heart width="13px" />}
                </StyledSave>
                {Boolean(video) && (
                    <Progress>
                        <Track progress={progress} />
                    </Progress>
                )}
                <StyledImageContainer onPress={goToSkill}>
                    {Boolean(thumbnailImage) && (
                        <StyledImage
                            source={{ uri: thumbnailImage, cache: 'force-cache' }}
                            resizeMode="cover"
                        />
                    )}
                </StyledImageContainer>

                <StyledBanner onPress={goToSkill} labelColor={labelColor}>
                    <BannerText>{name}</BannerText>
                </StyledBanner>
            </StyledInner>
        </StyledContainer>
    );
};

export default Skill;
