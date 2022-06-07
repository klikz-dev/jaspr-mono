import { useEffect, useState } from 'react';
import config from '../../../config';
import { useLocation } from 'react-router';
import logo from 'assets/logo.png';
import FormField from '../formField';
import Button from 'components/Button';
import styles from './index.module.scss';
import { useHistory } from 'lib/router';

interface LocationState {
    setPasswordToken: string;
    setupToken: string;
    setupUid: string;
}

const Account = () => {
    const history = useHistory();
    const location = useLocation<LocationState>();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showErrors, setShowErrors] = useState(false);
    const alreadySetUp = history.location.pathname.includes('reset-password');

    useEffect(() => {
        setShowErrors(false);
    }, [password, confirmPassword]);

    let error = '';
    if (!password) {
        error = 'Please provide a password.';
    } else if (!confirmPassword) {
        error = 'Please confirm your password.';
    } else if (password !== confirmPassword) {
        error = 'The two passwords do not match.';
    }

    const submit = async (): Promise<void> => {
        if (error) {
            setShowErrors(true);
            return;
        }

        let result;
        const { hash = '' } = history.location;
        if (hash.includes('&userType=Technician')) {
            const [uidHash = '', tokenHash = ''] = hash.slice(1).split('&');
            const [, uid] = uidHash.split('=');
            const [, token] = tokenHash.split('=');
            const payload = {
                password,
                token,
                uid,
            };

            result = await fetch(
                `${config.apiRoot}/${
                    alreadySetUp
                        ? 'technician/reset-password/set-password'
                        : 'technician/activate/set-password$'
                }`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload),
                },
            );
        } else {
            const { setPasswordToken, setupToken, setupUid } = location.state;
            const payload = {
                password,
                token: setupToken,
                uid: setupUid,
                setPasswordToken,
            };

            result = await fetch(
                `${config.apiRoot}/${
                    alreadySetUp ? 'patient/reset-password/set-password' : 'patient/set-password'
                }`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload),
                },
            );
        }

        if (result.ok) {
            if (!alreadySetUp) {
                history.push('/');
            } else {
                history.push('/password-reset/success');
            }
        } else {
            console.log('error', result);
        }
    };

    return (
        <div className={styles.container}>
            <header>
                <img src={logo} alt="Jaspr Health" /> Jaspr Health
            </header>
            <div className={styles.box}>
                <h1>{alreadySetUp ? 'Reset Password' : 'Account Details'}</h1>
                <FormField
                    label="Password"
                    value={password}
                    type="password"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <FormField
                    label="Confirm Password"
                    value={confirmPassword}
                    type="password"
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                {showErrors && <div className={styles.error}>{error}</div>}
                <Button onClick={submit}>Submit</Button>
                {!alreadySetUp && (
                    <p className={styles.disclaimer}>
                        By setting up an account you agree to our{' '}
                        <a
                            href="https://jasprhealth.com/terms-of-service/"
                            rel="noopener noreferrer"
                            target="_blank"
                        >
                            Terms and Conditions
                        </a>{' '}
                        and{' '}
                        <a
                            href="https://jasprhealth.com/privacy-policy/"
                            rel="noopener noreferrer"
                            target="_blank"
                        >
                            Privacy Policy
                        </a>
                    </p>
                )}
            </div>
        </div>
    );
};

export default Account;
