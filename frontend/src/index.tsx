import 'react-app-polyfill/ie11';
import 'react-app-polyfill/stable';
import React from 'react';
import ReactDOM from 'react-dom';
import Segment, { AnalyticNames } from './lib/segment';
import Sentry from './lib/sentry';
import './index.scss';
import Jaspr from './jaspr';
import smoothscroll from 'smoothscroll-polyfill';
import 'typeface-source-sans-pro';
import './animations.css';

// Smooth scrolling polyfill
smoothscroll.polyfill();

if (process.env.NODE_ENV === 'production') {
    Sentry.init({
        dsn: process.env.REACT_APP_SENTRY_DSN,
        debug: process.env.NODE_ENV !== 'production',
        release: process.env.REACT_APP_VERSION,
        environment: process.env.REACT_APP_ENVIRONMENT,
    });
}

const root = document.getElementById('root');

Segment.track(AnalyticNames.APP_LOADED, {
    version: process.env.REACT_APP_VERSION,
    buildNumber: process.env.REACT_APP_BUILD_NUMBER,
});

if (root) {
    ReactDOM.render(
        <React.StrictMode>
            <Jaspr />
        </React.StrictMode>,
        root,
    );
}
