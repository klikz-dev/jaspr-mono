interface configType {
    apiRoot: string;
    frontendTld: string;
    version: string;
    buildNumber: string;
    sentryDsn: string;
    environment: string;
    segmentId: string;
}

const config: configType = {
    apiRoot: process.env.REACT_APP_API_ROOT || '',
    frontendTld: process.env.REACT_APP_FRONTEND_TLD || '',
    version: process.env.REACT_APP_VERSION || '',
    buildNumber: process.env.REACT_APP_BUILD_NUMBER,
    sentryDsn: process.env.REACT_APP_SENTRY_DSN || '',
    environment: process.env.REACT_APP_ENVIRONMENT || '',
    segmentId: process.env.REACT_APP_SEGMENT_ID || '',
};

export default config;
