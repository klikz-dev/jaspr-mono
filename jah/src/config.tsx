import Constants from 'expo-constants';

interface configType {
    apiRoot: string;
    version: string;
    sentryDsn: string;
    environment: string;
    segmentId: string;
}

const config: configType = {
    apiRoot: Constants.manifest.extra.apiRoot,
    version: Constants.manifest.extra.version,
    sentryDsn: Constants.manifest.extra.sentryDsn,
    environment: Constants.manifest.extra.environment,
    segmentId: Constants.manifest.extra.segmentId,
};

export default config;
