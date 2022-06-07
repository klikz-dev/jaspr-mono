import { useContext, useEffect, useRef } from 'react';
import StoreContext from 'state/context/store';
import { getVideoRatings, saveStoryForLater, rateVideo } from 'state/actions/stories';
import { rateSkill, saveSkillForLater } from 'state/actions/skills';
import Player from './player';
import Heart from 'assets/icons/Heart';
import Star from 'assets/StarBlueOutline.png';
import StarFilled from 'assets/StarFilled.png';
import styles from './index.module.scss';
import { Skill, Patient, Video as VideoType } from 'state/types';

type VideoProps = {
    video: VideoType;
    back: () => void;
    autoplay?: boolean;
} & (
    | {
          type: 'story';
          skill?: undefined;
      }
    | {
          type: 'skill';
          skill: Skill;
      }
);

const Video = ({ video, skill, back, autoplay = false, type }: VideoProps): JSX.Element => {
    const ccButtonNodeRef = useRef();
    const [store, dispatch] = useContext(StoreContext);
    const { stories, user } = store;
    const { ratingsFetched, videoRatings } = stories;
    const { sessionLocked } = user as Patient;

    useEffect(() => {
        if (!ratingsFetched && !sessionLocked) {
            getVideoRatings(dispatch);
        }
    }, [dispatch, ratingsFetched, sessionLocked]);

    const videoRating = videoRatings.find((rating) => rating.video === video.id);

    const save = () => {
        const saveForLater = videoRating ? videoRating.saveForLater : false;
        if (ratingsFetched) {
            if (type === 'story') {
                saveStoryForLater(dispatch, videoRating?.id || null, video.id, !saveForLater);
            } else if (type === 'skill') {
                saveSkillForLater(dispatch, skill.patientActivity, skill.id, !skill.saveForLater);
            }
        }
    };

    const rate = (rating: number) => {
        if (ratingsFetched && rating <= 5) {
            const newRating = rating as 1 | 2 | 3 | 4 | 5;
            if (type === 'story') {
                rateVideo(dispatch, videoRating?.id || null, video.id, newRating);
            } else if (type === 'skill') {
                rateSkill(dispatch, skill.patientActivity, skill.id, newRating);
            }
        }
    };

    let saved: boolean;
    let rating: 1 | 2 | 3 | 4 | 5 | null;

    if (type === 'story') {
        saved = videoRating?.saveForLater ?? false;
        rating = videoRating?.rating ?? null;
    } else if (type === 'skill') {
        saved = skill.saveForLater ?? false;
        rating = skill.rating ?? null;
    }

    return (
        <div
            className={styles.container}
            style={{ background: 'linear-gradient(90deg, #383c58 0%, #343245 100%)' }}
        >
            <div className={styles.controls}>
                <div
                    className={styles.back}
                    onClick={back}
                    onKeyDown={(e) => {
                        if (e.key === ' ' || e.key === 'Enter' || e.key === 'Spacebar') {
                            back();
                        }
                    }}
                    tabIndex={0}
                    style={{ cursor: 'pointer' }}
                    role="button"
                    aria-label="Exit the video player"
                >
                    ‹ Back
                </div>

                <span className={styles.title} style={{ lineHeight: '36px' }}>
                    {video.name}
                </span>

                <div className={styles.rate}>
                    {[...Array(5)].map((_, i: 0 | 1 | 2 | 3 | 4) => {
                        return (
                            <img
                                key={i}
                                className={styles.star}
                                style={{ cursor: 'pointer', opacity: ratingsFetched ? 1 : 0.5 }}
                                src={i + 1 <= rating ? StarFilled : Star}
                                role="button"
                                aria-label={`Rate this video ${i + 1} stars. ${
                                    rating
                                        ? `You have currently rated this video ${rating} stars`
                                        : 'You have not yet rated this video'
                                }`}
                                onClick={() => rate(i + 1)}
                                onKeyDown={(e) => {
                                    if (
                                        e.key === ' ' ||
                                        e.key === 'Enter' ||
                                        e.key === 'Spacebar'
                                    ) {
                                        rate(i + 1);
                                    }
                                }}
                                tabIndex={0}
                                alt={
                                    rating
                                        ? `You rated the video ${rating} stars`
                                        : 'You have not yet rated this video'
                                }
                            />
                        );
                    })}
                </div>
            </div>
            <Player
                videoId={video.id}
                poster={video.poster || undefined}
                fpm4Transcode={video.fpm4Transcode}
                hlsPlaylist={video.hlsPlaylist}
                mp4Transcode={video.mp4Transcode}
                name={video.name}
                autoplay={autoplay}
                ccButtonNodeRef={ccButtonNodeRef}
            />

            <div className={styles.controls}>
                <div
                    className={styles.saveForLater}
                    style={{ cursor: 'pointer' }}
                    onClick={save}
                    onKeyDown={(e) => {
                        if (e.key === ' ' || e.key === 'Enter' || e.key === 'Spacebar') {
                            save();
                        }
                    }}
                    role="button"
                    tabIndex={0}
                    aria-label={saved ? 'Remove from favorites' : 'Add to favorites'}
                >
                    <Heart
                        color={
                            saved
                                ? 'rgba(255,59,0,1)'
                                : `rgba(255,255,255,${ratingsFetched ? 1 : 0.5})`
                        }
                        fill={
                            saved
                                ? 'rgba(255,59,0,1)'
                                : `rgba(255,255,255,${ratingsFetched ? 1 : 0.5})`
                        }
                    />
                    {saved ? 'Remove from favorites' : 'Add to favorites'}
                </div>

                <div className={styles.ccButtonContainer} ref={ccButtonNodeRef} />
            </div>
        </div>
    );
};

export default Video;
