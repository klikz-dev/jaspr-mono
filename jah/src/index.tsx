import { registerRootComponent } from 'expo';
import Constants from 'expo-constants';
import * as Segment from 'expo-analytics-segment';
import Sentry from './lib/sentry';
import Jaspr from './jaspr';
import 'react-native-gesture-handler';

const { segmentId } = Constants.manifest.extra;
Segment.initialize({ androidWriteKey: segmentId, iosWriteKey: segmentId });

if (process.env.NODE_ENV === 'production') {
    Sentry.init({
        dsn: Constants.manifest.extra.sentryDsn,
        // @ts-ignore
        enableInExpoDevelopment: true,
        debug: false,
        release: Constants.manifest.extra.version,
        environment: Constants.manifest.extra.environment,
    });
}

registerRootComponent(Jaspr);
