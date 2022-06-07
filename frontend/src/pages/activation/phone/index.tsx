import { useState } from 'react';
import { useHistory, useLocation } from 'lib/router';
import config from '../../../config';
import logo from 'assets/logo.png';
import FormField from '../formField';
import Button from 'components/Button';
import styles from './index.module.scss';

const ActivatePhone = () => {
    const history = useHistory();
    const location = useLocation();
    const [mobilePhone, setMobilePhone] = useState('');
    const { hash = '' } = location;
    const [uidHash = '', tokenHash = ''] = hash.slice(1).split('&');
    const [, uid] = uidHash.split('=');
    const [, token] = tokenHash.split('=');
    const [error, setError] = useState('');
    const isReset = location.pathname.includes('reset-password');

    const submit = async () => {
        if (!mobilePhone) {
            return setError(
                'please enter your mobile phone number used when you setup your Jaspr account',
            );
        }
        const result = await fetch(
            `${config.apiRoot}/${
                isReset
                    ? 'patient/reset-password/verify-phone-number'
                    : 'patient/verify-phone-number'
            }`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    mobilePhone,
                    uid,
                    token,
                }),
            },
        );

        const json = await result.json();

        if (result.status >= 200 && result.status < 300 && json && json.sent) {
            history.push({
                pathname: isReset ? '/reset-password/activate-code' : '/activate-code',
                hash,
            });
        } else if (result.status >= 400 && result.status < 500 && json.mobilePhone) {
            setError(json.mobilePhone[0]);
        } else if (result.status >= 400 && result.status < 500 && json.nonFieldErrors) {
            setError(json.nonFieldErrors[0]);
        } else {
            setError('There was an unknown error.  Please contact JASPR Support');
        }
    };

    return (
        <div className={styles.container}>
            <header>
                <img src={logo} alt="Jaspr Health" /> Jaspr Health
            </header>
            <div className={styles.box}>
                <h1>
                    Jaspr at Home
                    <br />
                    {isReset ? 'Password Reset' : 'Account Activation'}
                </h1>
                <p>
                    Enter the phone number on your account, and we'll send you an activation code to
                    get started.
                </p>

                <FormField
                    label="Phone number"
                    value={mobilePhone}
                    onChange={(e) => {
                        setError('');
                        setMobilePhone(e.target.value);
                    }}
                />
                <div className={styles.error}>{error}</div>
                <Button onClick={submit}>Get Activation Code</Button>
            </div>
        </div>
    );
};

export default ActivatePhone;
