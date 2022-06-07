import Sentry from 'lib/sentry';

const modalNames = [
    // Values further down the list will appear over values nearer the beginning of the list
    'technician.edit-patient',
    'technician.set-path',
    'technician.tablet-activation',
    'technician.update-app-banner',
    'patient.summaries',
    'patient.assessment-unlock-banner',
    'patient.checkin-banner',
    'patient.hamburger',
    'patient.skill',
    'patient.skill-item',
    'patient.shared-story-item',
    'patient.story-video',
    'patient.jah-signup',
    'patient.offline',
    'patient.loading',
    'patient.lockout',
    'patient.lockout-help',
    'patient.confirm-logout',
];

const getIndex = (name: string): number => {
    const index = modalNames.findIndex((modalName) => modalName === name);
    if (index === -1) {
        Sentry.captureException(`No z-index for ${name}`);
        return 10;
    }
    // default z-index is 1, so we want to start at 2
    return 2 + index;
};

export default getIndex;
