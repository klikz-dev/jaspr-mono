import 'dotenv/config';
const config = ({ config }) => {
    return {
        ...config,
        extra: {
            version: process.env.npm_package_version,
            apiRoot: process.env.REACT_APP_API_ROOT,
            sentryDsn: process.env.REACT_APP_SENTRY_DSN,
            environment: process.env.REACT_APP_ENVIRONMENT,
            segmentId: process.env.REACT_APP_EXPO_SEGMENT_ID,
        },
    };
};
export default config;
