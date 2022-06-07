import actionNames from 'state/actions/actionNames';
import * as ExpoSegment from 'expo-analytics-segment';

export const track = (event: string, properties?: Object) => {
    if (properties) {
        ExpoSegment.trackWithProperties(event, properties);
    } else {
        ExpoSegment.track(event);
    }
};

export const page = (name: string, properties?: Object) => {
    if (properties) {
        ExpoSegment.screenWithProperties(name, properties);
    } else {
        ExpoSegment.screen(name);
    }
};

export const identify = (userId: string, properties?: Object) => {
    if (properties) {
        ExpoSegment.identifyWithTraits(userId, properties);
    } else {
        ExpoSegment.identify(userId);
    }
};

export const reset = () => {
    ExpoSegment.reset();
};

export const AnalyticNames = {
    ACCOUNT_ACTIVATION: 'account-activation',
    ACCOUNT_CODE: 'account-code',
    PRIVACY_POLICY_ACCEPTED: 'patient accepted privacy policy in JAH',
    SET_PASSWORD: 'set-password',
    LOG_OUT_BY_USER: 'LogOutByUser',
    VIDEO_PLAYER_CLOSED: 'Video player closed',
    VIDEO_BUFFER_STARTED: 'Video Playback Buffer Started',
    VIDEO_BUFFER_COMPLETED: 'Video Playback Buffer Completed',
    VIDEO_PLAYBACK_STARTED: 'Video playback Started',
    VIDEO_PLAYBACK_PAUSED: 'Video Playback Paused',
    VIDEO_PLAYBACK_COMPLETED: 'Video Playback Completed',
    VIDEO_PLAYBACK_INTERRUPTED: 'Video Playback Interrupted',
    JAH_STATE_CHANGE: 'jah-state-change',
    APP_LOADED: 'APP_LOADED',
    STABILITY_PLAN_EDITED: 'stability plan edited from JAH',
    JAH_ONBOARDING_COMPLETE: 'JAH Onboarding Complete',
    CONNECTION_RESTORED: 'connection-restored',
    EMAIL_UPDATED: 'Email updated',
    ...actionNames,
};

const Segment = {
    track,
    page,
    identify,
    reset,
};

export default Segment;
