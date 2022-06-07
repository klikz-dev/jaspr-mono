import { useState } from 'react';
import config from '../../../config';
import { useHistory } from 'lib/router';
import logo from 'assets/logo.png';
import FormField from '../formField';
import Button from 'components/Button';
import styles from './index.module.scss';

const Code = (): JSX.Element => {
    const history = useHistory();
    const { hash } = history.location;
    const [uidHash, tokenHash] = hash.slice(1).split('&');
    const [, uid] = uidHash.split('=');
    const [, token] = tokenHash.split('=');
    const [code, setCode] = useState('');
    const [error, setError] = useState('');
    const isReset = history.location.pathname.includes('reset-password');

    const submit = async () => {
        if (!code) {
            return setError('please enter the code your received on your mobile phone');
        }

        // TODO Switch to Axios
        const result = await fetch(
            `${config.apiRoot}/${
                isReset
                    ? 'patient/reset-password/check-phone-number-code'
                    : 'patient/check-phone-number-code'
            }`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code, uid, token }),
            },
        );
        const json = await result.json();
        if (result.ok) {
            // TODO Validate state works!
            history.push({
                pathname: isReset ? '/reset-password/set-password' : '/set-password',
                hash,
                state: {
                    setupToken: token,
                    setupUid: uid,
                    setPasswordToken: json.setPasswordToken,
                },
            });
        }

        if (
            (json &&
                json.nonFieldErrors &&
                json.nonFieldErrors.includes('Invalid verification code.')) ||
            (json &&
                json.code &&
                json.code.length > 0 &&
                json.code[0] === 'This value does not match the required pattern.')
        ) {
            setError('The activation code you entered was incorrect');
        } else if (
            json &&
            json.nonFieldErrors &&
            json.nonFieldErrors.includes(
                'We ran into an issue verifying your phone number. Double check the code and try again after a few seconds. If this message keeps showing up, please contact support.',
            )
        ) {
            setError(
                'We ran into an issue verifying your phone number. Double check the code and try again after a few seconds. If this message keeps showing up, please contact support.',
            );
        } else if (!result.ok) {
            return setError(
                'We ran into an issue verifying your phone number. Please go back and re-enter your phone number',
            );
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
                <p>We sent you an activation code via SMS text message. Enter the code below.</p>
                <FormField
                    label="Activation code"
                    value={code}
                    onChange={(e) => {
                        setError('');
                        setCode(e.target.value);
                    }}
                    autoComplete="one-time-code"
                />
                <div className={styles.error}>{error}</div>
                <Button onClick={submit}>Submit</Button>
            </div>
        </div>
    );
};

export default Code;
