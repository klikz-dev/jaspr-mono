import { useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
import Segment, { AnalyticNames } from 'lib/segment';
import styles from './index.module.scss';
import Button from 'components/Button';
import iconSuccess from './success.svg';
import iconWarning from './warning.svg';
import iconError from './error.svg';
import ApiGetTest from './tests/apiGet';
import ApiHeadTest from './tests/apiHead';
import DownloadFileTest from './tests/downloadFile';
import PerformanceTest from './tests/performance';
import ApiImgProxy from './tests/apiImgProxy';
import MemoryTest from './tests/memory';
import { PostResponse } from 'state/types/api/technician/login';
import config from '../../../config';

interface TestProps {
    label: string;
    progress?: number;
    details: string;
    status: string;
}

interface Status {
    progress?: number;
    statusText: string;
    details?: string;
    rate?: number;
    timing?: number;
}

const Test = ({ label, progress, details, status }: TestProps) => {
    let statusIcon = null;
    if (status === 'SUCCESS') {
        statusIcon = iconSuccess;
    } else if (status === 'WARNING') {
        statusIcon = iconWarning;
    } else if (status === 'ERROR') {
        statusIcon = iconError;
    }
    return (
        <div className={styles.test}>
            <div>{label}</div>
            <div>
                <div className={styles.progress}>
                    <div className={styles.track} style={{ width: `${progress}%` }} />
                </div>
            </div>
            <div>{details}</div>
            <div>{Boolean(statusIcon) && <img src={statusIcon} alt={status} />}</div>
        </div>
    );
};

const detailTemplate = (status: Status): string => {
    return `${status.rate?.toFixed(1) || 0}MB/s ${status.timing?.toFixed(1) || 0}s ${
        status.details || ''
    }`;
};

const Debug = () => {
    const history = useHistory();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [credentialStatus, setCredentialStatus] = useState<Status>({} as Status);
    const [credentialError, setCredentialError] = useState('');
    const [jasprAPIStatus, setJasprAPIStatus] = useState<Status>({} as Status);
    const [mediaAPIStatus, setMediaAPIStatus] = useState<Status>({} as Status);
    const [sentryAPIStatus, setSentryAPIStatus] = useState<Status>({} as Status);
    const [segmentAPIStatus, setSegmentAPIStatus] = useState<Status>({} as Status);
    const [imageDownloadStatus, setImageDownloadStatus] = useState<Status>({} as Status);
    const [videoDownloadStatus, setVideoDownloadStatus] = useState<Status>({} as Status);
    const [performanceStatus, setPerformanceStatus] = useState<Status>({} as Status);
    const [memoryStatus, setMemoryStatus] = useState<Status>({} as Status);
    const [testsRun, setTestsRun] = useState(false);

    const login = async () => {
        const domain = window.location.hostname;
        let organization;
        if (domain.split('--').length > 1) {
            [organization] = domain.split('--');
        } else {
            [organization] = domain.split('.');
        }

        const params = {
            email,
            password,
            fromNative: false,
            longLived: false,
            organizationCode: organization,
        };
        setCredentialError('');
        try {
            await axios.post<PostResponse>(`${config.apiRoot}/technician/login`, params);
            setCredentialStatus({ statusText: 'SUCCESS' });
            if (!testsRun) {
                setTestsRun(true);
                tests();
            }
        } catch (err) {
            const { response } = err;
            const json = response?.data;
            if (response?.status === 400 || response?.status === 403) {
                if (json?.email?.length) {
                    setCredentialError(json.email);
                } else if (json?.password?.length) {
                    setCredentialError(json.password);
                } else if (json?.nonFieldErrors?.length > 0) {
                    setCredentialError(json.nonFieldErrors[0]);
                } else if (json.detail) {
                    setCredentialError(json.detail);
                } else {
                    setCredentialStatus({ statusText: 'ERROR' });
                    if (!testsRun) {
                        setTestsRun(true);
                        tests();
                    }
                }
            } else {
                setCredentialStatus({ statusText: 'ERROR' });
                if (!testsRun) {
                    setTestsRun(true);
                    tests();
                }
            }
        }
    };

    const tests = async () => {
        try {
            await new ApiGetTest(`${process.env.REACT_APP_API_ROOT}/static-media`)
                .setter(setJasprAPIStatus)
                .run();
        } catch (err) {}

        try {
            await new ApiHeadTest(`https://media.jasprhealth.com/Diana_and_Dave_Intro_Pic.jpg`)
                .setter(setMediaAPIStatus)
                .run();
        } catch (err) {}

        try {
            await new ApiImgProxy(
                `https://sentry.jasprhealth.com/_static/1631470677/sentry/images/logos/default-organization-logo.png`,
            )
                .setter(setSentryAPIStatus)
                .run();
        } catch (err) {}

        try {
            await new ApiGetTest(`https://api.segment.io/v1/p`).setter(setSegmentAPIStatus).run();
        } catch (err) {}

        try {
            await new DownloadFileTest('https://media.jasprhealth.com/Diana_and_Dave_Intro_Pic.jpg')
                .setter(setImageDownloadStatus)
                .run();
        } catch (err) {}

        try {
            await new DownloadFileTest(
                'https://media.jasprhealth.com/Intro_Video_-_Diana__Dave/jaspr_720p_Intro_Video_-_Diana__Dave.mp4',
            )
                .setter(setVideoDownloadStatus)
                .run();
        } catch (err) {}

        try {
            await new PerformanceTest().setter(setPerformanceStatus).run();
        } catch (err) {}

        try {
            await new MemoryTest().setter(setMemoryStatus).run();
        } catch (err) {}
    };

    const report = () => {
        Segment.track(AnalyticNames.DEBUG, {
            'api.jasprhealth.com': jasprAPIStatus.statusText,
            'media.jasprhealth.com': mediaAPIStatus.statusText,
            'segment.io': sentryAPIStatus.statusText,
            'sentry.jasprhealth.com': segmentAPIStatus.statusText,
            'Download image - 3 mb': imageDownloadStatus.statusText,
            'Download video - 100 mb': videoDownloadStatus.statusText,
            'Download speed': videoDownloadStatus.rate,
        });
    };

    let apiStatus = '';

    if (jasprAPIStatus.statusText === 'SUCCESS' && credentialStatus.statusText === 'SUCCESS') {
        apiStatus = 'SUCCESS';
    } else if (jasprAPIStatus.statusText === 'ERROR' || credentialStatus.statusText === 'ERROR') {
        apiStatus = 'ERROR';
    } else if (jasprAPIStatus.statusText === 'WARNING') {
        apiStatus = 'WARNING';
    }

    return (
        <div className={styles.container}>
            <div
                className={styles.back}
                onClick={() => {
                    history.replace('/');
                }}
            >
                ‹ Back
            </div>
            <div className={styles.credentials}>
                <div className={styles.row}>
                    <input
                        type="text"
                        value={email}
                        placeholder="Email"
                        onChange={({ target }) => setEmail(target.value)}
                    />
                    <input
                        type="password"
                        value={password}
                        placeholder="Password"
                        onChange={({ target }) => setPassword(target.value)}
                    />
                    <Button onClick={login}>Submit</Button>
                </div>
                {credentialError && <span style={{ color: 'red' }}>{credentialError}</span>}
            </div>
            <div className={styles.results}>
                <Test
                    label="api.jasprhealth.com"
                    progress={jasprAPIStatus.progress}
                    details={detailTemplate(jasprAPIStatus)}
                    status={apiStatus}
                />
                <Test
                    label="media.jasprhealth.com"
                    progress={mediaAPIStatus.progress}
                    details={detailTemplate(mediaAPIStatus)}
                    status={mediaAPIStatus.statusText}
                />

                <Test
                    label="segment.io"
                    progress={segmentAPIStatus.progress}
                    details={detailTemplate(segmentAPIStatus)}
                    status={segmentAPIStatus.statusText}
                />
                <Test
                    label="sentry.jasprhealth.com"
                    progress={sentryAPIStatus.progress}
                    details={detailTemplate(sentryAPIStatus)}
                    status={sentryAPIStatus.statusText}
                />

                <Test
                    label="Download image - 3 mb"
                    progress={imageDownloadStatus.progress}
                    details={detailTemplate(imageDownloadStatus)}
                    status={imageDownloadStatus.statusText}
                />
                <Test
                    label="Download video - 100 mb"
                    progress={videoDownloadStatus.progress}
                    details={detailTemplate(videoDownloadStatus)}
                    status={videoDownloadStatus.statusText}
                />
                <Test
                    label="Performance Test"
                    progress={performanceStatus.progress}
                    details={`${performanceStatus.rate || 0} primes ${
                        performanceStatus.timing?.toFixed(1) || 0
                    }s`}
                    status={performanceStatus.statusText}
                />
                <Test
                    label="Memory Test"
                    progress={memoryStatus.progress}
                    details={`${memoryStatus.details || ''} ${memoryStatus.rate || ''} ${
                        memoryStatus.rate ? 'bytes' : ''
                    }`}
                    status={memoryStatus.statusText}
                />
            </div>
            <div className={styles.buttons}>
                <Button onClick={window.print}>Print Page</Button>
                <Button onClick={report}>Report to Jaspr</Button>
            </div>
        </div>
    );
};

export default Debug;
