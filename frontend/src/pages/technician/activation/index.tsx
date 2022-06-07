import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { useHistory } from 'lib/router';
import { useQuery } from 'lib/useQuery';
import Hamburger from 'components/Hamburger';
import logo from 'assets/logo.png';
import Button from 'components/Button';
import styles from './index.module.scss';
import StoreContext from 'state/context/store';
import { setMe, setToken } from 'state/actions/user';
import config from '../../../config';
import Segment, { AnalyticNames } from 'lib/segment';

const TechActivation = () => {
    const history = useHistory();
    const query = useQuery();
    const { hash = '' } = history.location;
    const [uidHash = '', tokenHash = ''] = hash.slice(1).split('&');
    const [, uid] = uidHash.split('=');
    const [, token] = tokenHash.split('=');
    const activateTechnicianLink = query.get('activate-technician-link');
    const [, dispatch] = useContext(StoreContext);
    const [email, setEmail] = useState('');
    const [activationCode, setActivationCode] = useState('');
    const [passwordToken, setPasswordToken] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');

    const submit = (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        if (!passwordToken) {
            axios
                .post(`${config.apiRoot}/technician/activate`, {
                    email,
                    activationCode,
                    token,
                    uid,
                })
                .then((response) => {
                    setPasswordToken(response.data?.setPasswordToken);
                    Segment.track(AnalyticNames.TECHNICIAN_ACTIVATED);
                })
                .catch((err) => {
                    const { nonFieldErrors, email, activationCode } = err.response?.data;
                    if (nonFieldErrors?.length) {
                        setError(nonFieldErrors[0]);
                    } else if (email?.length) {
                        setError(email[0]);
                    } else if (activationCode?.length) {
                        setError(activationCode[0]);
                    }
                });
        } else {
            // Set password
            if (password && password !== confirmPassword) {
                setError('Your passwords do not match');
            } else if (password.length < 8) {
                setError('Your password must be at least 8 characters in length');
            } else if (
                !password.split('').filter((character) => character.toLowerCase() === character)
                    .length
            ) {
                setError('Your password must contain at least 1 lowercase character');
            } else if (
                !password.split('').filter((character) => character.toUpperCase() === character)
                    .length
            ) {
                setError('Your password must contain at least 1 uppercase character');
            } else if (
                !password.split('').filter((character) => !Number.isNaN(+character)).length
            ) {
                setError('Your password must contain at least 1 number');
            } else {
                axios
                    .post(`${config.apiRoot}/technician/set-password`, {
                        email,
                        activationCode,
                        token,
                        uid,
                        password,
                        setPasswordToken: passwordToken,
                    })
                    .then((response) => {
                        const { token, technician } = response.data;
                        if (token) {
                            axios.defaults.headers.common['Authorization'] = `Token ${token}`;
                            setToken(dispatch, token);
                            setMe(dispatch, technician);
                            Segment.track(AnalyticNames.TECHNICIAN_SET_PASSWORD);
                            history.push('/technician/patients');
                        }
                    })
                    .catch((err) => {
                        const { nonFieldErrors, password } = err.response?.data;
                        if (nonFieldErrors?.length) {
                            setError(nonFieldErrors[0]);
                        } else if (email?.length) {
                            setError(password[0]);
                        }
                    });
            }
        }
    };

    useEffect(() => {
        if (activateTechnicianLink === 'invalid') {
            setError('Something went wrong, please contact your site admin');
            Segment.track(AnalyticNames.TECHNICIAN_FAILED_TO_ACTIVATE);
        }
    }, [activateTechnicianLink]);

    return (
        <form className={styles.techActivation} onSubmit={submit}>
            <Hamburger />
            <img className={styles.logo} src={logo} alt="" />

            <div className={styles.outer}>
                <div className={styles.header}>
                    {passwordToken ? 'Set Password' : 'Account Activation'}
                </div>
                {activateTechnicianLink !== 'invalid' && (
                    <div className={styles.container}>
                        {Boolean(!passwordToken) && (
                            <>
                                <div className={styles.row}>
                                    <label className={styles.label}>
                                        <span className={styles.formLabel}>Email</span>
                                        <input
                                            className={styles.input}
                                            placeholder="Email"
                                            value={email}
                                            onChange={({ target }) => setEmail(target.value)}
                                        />
                                    </label>
                                </div>
                                <div className={styles.row}>
                                    <label className={styles.label}>
                                        <span className={styles.formLabel}>Activation Code</span>
                                        <input
                                            className={styles.input}
                                            placeholder="Activation Code"
                                            value={activationCode}
                                            onChange={({ target }) =>
                                                setActivationCode(target.value)
                                            }
                                        />
                                    </label>
                                </div>
                            </>
                        )}
                        {Boolean(passwordToken) && (
                            <>
                                <div className={styles.row}>
                                    <label className={styles.label}>
                                        <span className={styles.formLabel}>Password</span>
                                        <input
                                            className={styles.input}
                                            type="password"
                                            autoComplete="new-password"
                                            value={password}
                                            onChange={({ target }) => setPassword(target.value)}
                                        />
                                    </label>
                                </div>
                                <div className={styles.row}>
                                    <label className={styles.label}>
                                        <span className={styles.formLabel}>Confirm Password</span>
                                        <input
                                            className={styles.input}
                                            type="password"
                                            autoComplete="new-password"
                                            value={confirmPassword}
                                            onChange={({ target }) =>
                                                setConfirmPassword(target.value)
                                            }
                                        />
                                    </label>
                                </div>
                                <div className={styles.requirements}>
                                    Password Requirements
                                    <ul>
                                        <li>Minimum 8 characters</li>
                                        <li>At least one uppercase and one lowercase character</li>
                                        <li>At least one number</li>
                                    </ul>
                                </div>
                            </>
                        )}
                    </div>
                )}
                <div className={styles.error}>{error}</div>
                {activateTechnicianLink !== 'invalid' && (
                    <div className={styles.buttons}>
                        <Button onClick={submit}>Submit</Button>
                    </div>
                )}
            </div>
        </form>
    );
};

export default TechActivation;
