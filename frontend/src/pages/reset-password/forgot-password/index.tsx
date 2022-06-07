import { useState } from 'react';
import { useHistory } from 'lib/router';
import config from '../../../config';
import logo from 'assets/logo.png';
import FormField from 'pages/activation/formField';
import Button from 'components/Button';
import check from 'assets/check.svg';
import styles from './index.module.scss';

export interface ViewProps {
    complete: boolean;
    email: string;
    setError: (error: string) => void;
    setEmail: (email: string) => void;
    error: string;
    submit: () => void;
}

const ForgotPassword = () => {
    const history = useHistory();
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [complete, setComplete] = useState(false);

    const submit = async () => {
        if (!email || !email.includes('@')) {
            return setError('Enter a valid email address.');
        }

        const result = await fetch(`${config.apiRoot}/reset-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email }),
        });

        if (result.ok) {
            setComplete(true);
        } else {
            const json = await result.json();
            if (json.email) {
                setError(json.email[0]);
            }
        }
    };

    return (
        <div className={styles.container}>
            <header className={`${styles.header} ${styles.headerText}`}>
                <div
                    className={styles.back}
                    onClick={() => {
                        history.replace('/login');
                    }}
                >
                    ‹ Back
                </div>
                <img className={styles.headerImg} src={logo} alt="Jaspr Health" />
            </header>
            <div className={styles.box}>
                {!complete && (
                    <>
                        <h1 className={styles.h1}>
                            Jaspr Health Account
                            <br />
                            Password Reset
                        </h1>
                        <p className={styles.p}>
                            Enter the email associated with your account to receive instructions to
                            reset your password.
                        </p>
                        <FormField
                            label="Email"
                            value={email}
                            onChange={(e) => {
                                setError('');
                                setEmail(e.target.value);
                            }}
                        />
                        <div className={styles.error}>{error}</div>
                        <Button onClick={submit}>Submit</Button>
                    </>
                )}
                {complete && (
                    <>
                        <h1 className={styles.h1}>
                            Jaspr Health Account
                            <br />
                            Password Reset
                        </h1>
                        <p className={styles.p}>
                            If the email address entered corresponds with an existing account, an
                            email with reset instructions has been sent.
                        </p>

                        <img src={check} alt="Success" />
                    </>
                )}
            </div>
        </div>
    );
};

export default ForgotPassword;
