import Sentry from 'lib/sentry';
import { useEffect } from 'react';

const manifest = {
    name: 'JASPR',
    short_name: 'JASPR',
    description: 'Emergency Department Suicide Prevention for Patients & Providers',
    icons: [
        {
            src: '/android-chrome-192x192.png',
            sizes: '192x192',
            type: 'image/png',
        },
        {
            src: '/android-chrome-256x256.png',
            sizes: '256x256',
            type: 'image/png',
        },
    ],
    start_url: '/start-patient-session',
    scope: '/',
    orientation: 'landscape',
    display: 'standalone',
    theme_color: '#383c58',
    background_color: '#383c58',
};

const useManifest = (code: string = null, codeType: 'department' | 'system' = null) => {
    useEffect(() => {
        const securityCheck = () => {
            const isSecurePort = window.location.protocol === 'https:';
            const isCorrectTld = window.location.hostname.endsWith(
                process.env.REACT_APP_FRONTEND_TLD,
            );

            if (isSecurePort && isCorrectTld) {
                return true;
            }
            Sentry.captureException(
                `Attempting to set manifest from an invalid location ${window.location.href}`,
            );
            return false;
        };

        if (codeType && code && securityCheck()) {
            const customManifest = {
                ...manifest,
                start_url: `/start-patient-session/${codeType}/${code}`,
                scope: `${window.location.origin}/`,
            };
            const stringManifest = JSON.stringify(customManifest);
            const blob = new Blob([stringManifest], { type: 'application/json' });
            const manifestUrl = URL.createObjectURL(blob);
            document.querySelector('#manifest').setAttribute('href', manifestUrl);
        }
    }, [code, codeType]);
};

export default useManifest;
