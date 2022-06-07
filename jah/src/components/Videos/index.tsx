import React, { useContext } from 'react';
import { StatusBar } from 'expo-status-bar';
import Player from './Player';
import Styled from 'styled-components/native';
import styles from './index.module.scss';
import Heart from 'assets/heart.svg';
import HeartFilled from 'assets/heartFilled.svg';
import Star from 'assets/StarBlueOutline.png';
import StarFilled from 'assets/StarFilled.png';
import StoreContext from 'state/context/store';
import { VideoRating, Skill } from 'state/types';

const StyledContainer = Styled.View<{ isFullScreen?: boolean }>`${
    styles.container
}; background-color:${({ isFullScreen }) => (isFullScreen ? 'black' : 'white')}`;
const StyledControls = Styled.View`${styles.controls}`;
const StyledBack = Styled.TouchableOpacity`${styles.back}`;
const Text = Styled.Text``;
const TouchableOpacity = Styled.TouchableOpacity``;
const StyledTitle = Styled.Text`${styles.title}; line-height: 36px;`;
const StyledSaveForLater = Styled.TouchableOpacity`${styles.saveForLater}`;
const StyledRemoveFromPlan = Styled.TouchableOpacity`${styles.removeFromPlan}`;
const StyledRate = Styled.View`flex-direction: row;`;
const StyledStar = Styled.Image`${styles.star}`;

interface VideoProps {
    id?: number;
    poster?: string | null;
    mp4Transcode?: string;
    hlsPlaylist: string;
    fpm4Transcode: string;
    back: () => void;
    name: string;
    rate: (rating: 1 | 2 | 3 | 4 | 5) => void;
    save: () => void;
    object?: VideoRating | Skill;
    autoplay?: boolean;
}

const Video = ({
    id,
    poster,
    fpm4Transcode,
    hlsPlaylist,
    mp4Transcode,
    object,
    name,
    save,
    rate,
    back,
    autoplay,
}: VideoProps): JSX.Element => {
    const [store] = useContext(StoreContext);
    const { media } = store;
    const { isFullScreen } = media;
    return (
        <StyledContainer isFullScreen={isFullScreen}>
            <StatusBar hidden />
            {!isFullScreen && (
                <StyledControls>
                    <StyledBack onPress={back} hitSlop={{ top: 10, bottom: 10 }}>
                        <Text>‹ Back</Text>
                    </StyledBack>
                    <StyledTitle numberOfLines={1}>{name}</StyledTitle>
                    <StyledBack>
                        <Text style={{ opacity: 0 }}>‹ Back</Text>
                        {/* This hidden element ensures the same width is on the right side so the title is centered.  We could do this by calcualting onLayout the width and setting a margin */}
                    </StyledBack>
                </StyledControls>
            )}

            <Player
                videoId={id}
                poster={poster || undefined}
                fpm4Transcode={fpm4Transcode}
                hlsPlaylist={hlsPlaylist}
                mp4Transcode={mp4Transcode}
                name={name}
            />

            {!isFullScreen && Boolean(id) && (
                <StyledControls>
                    {object?.saveForLater && (
                        <StyledSaveForLater onPress={save}>
                            <HeartFilled />
                            <Text style={{ marginLeft: 5 }}>Remove from favorites</Text>
                        </StyledSaveForLater>
                    )}
                    {(!object || !object.saveForLater) && (
                        <StyledRemoveFromPlan onPress={save}>
                            <Heart />
                            <Text>Add to favorites</Text>
                        </StyledRemoveFromPlan>
                    )}
                    <StyledRate>
                        {[...Array(5)].map((e, i: 0 | 1 | 2 | 3 | 4) => {
                            if (object && object.rating != null && i + 1 <= object.rating) {
                                return (
                                    // @ts-ignore
                                    <TouchableOpacity key={i} onPress={() => rate(i + 1)}>
                                        <StyledStar source={StarFilled} />
                                    </TouchableOpacity>
                                );
                            } else {
                                return (
                                    // @ts-ignore
                                    <TouchableOpacity key={i} onPress={() => rate(i + 1)}>
                                        <StyledStar source={Star} />
                                    </TouchableOpacity>
                                );
                            }
                        })}
                    </StyledRate>
                </StyledControls>
            )}
        </StyledContainer>
    );
};

export default Video;
